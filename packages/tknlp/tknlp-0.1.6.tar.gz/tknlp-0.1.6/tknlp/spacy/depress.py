from spacy.language import Language
from spacy.tokens import Span, Token, Doc

from medspacy.common.medspacy_matcher import MedspacyMatcher, BaseRule
from medspacy.context import ConTextRule, ConText, ConTextGraph, ConTextModifier
from medspacy._extensions import _token_extensions, _span_extensions, _doc_extensions
from dataclasses import dataclass
from typing import Optional, List, Union
from collections import defaultdict
from .constant import SUBJ_DEPS, OBJ_DEPS, FIRST_PERSON, NEGATION_WORDS

DEFAULT_ATTRIBUTES = {
    "NEGATION": {"is_negate": True},
    "OTHER_EXPERIENCE": {"is_other": True},
    "HYPOTHETICAL": {"is_hypothetical": True},
}

C_RULES = [
    ConTextRule(
        literal="hypothesis", category="HYPOTHETICAL", direction='FORWARD', pattern = [{'DEP': 'aux', 'OP': '{2}'}]
    ),
]
V_RULES = [
    BaseRule('auxilary verb', 'VERB', pattern=[{"POS": "AUX"}, {"POS": "VERB"}]),
    BaseRule('auxilary verb phrase', 'VERB', pattern=[{"POS": "AUX"}]),
    BaseRule('verb phrase', 'VERB', pattern=[{"POS": "VERB"}])
]
def install_extensions(type: Union[Span, Doc, Token], ext:str, default=None, force=True) -> None:
    if not type.has_extension(ext):
        type.set_extension(ext, default=default, force=force)

@Language.component('remove_transformer')
def remove_transformer(doc):
    if doc.has_extension('trf_data'):
        doc.remove_extension('trf_data')


def extract_span_from_entity(token, exclude=['aux', 'det'], add_exclude=[]):
    exclude += add_exclude
    ent_subtree = sorted([c for c in token.subtree if c.dep_ not in exclude], key=lambda x: x.i)
    if not ent_subtree: return None
    return Span(token.doc, start=ent_subtree[0].i, end=ent_subtree[-1].i + 1)

def find_verb_subject(v):
    """
    Returns the nsubj, nsubjpass of the verb. If it does not exist and the root is a head,
    find the subject of that verb instead.
    """
    def f(r):
        if r.dep_ in SUBJ_DEPS: 
            return r
        elif r.dep_ in ["advcl", "acl"] and r.head.dep_ != "ROOT": 
            return f(r.head)
        for c in r.children:
            if c.dep_ in SUBJ_DEPS:
                return c
            elif c.dep_ in ["advcl", "acl"] and r.head.dep_ != "ROOT":
                return f(r.head)
    return f(v)

def find_match_child(root, allowed_dep=[], allowed_pos=[]):
    if allowed_pos:
        children = {c.dep_: c for c in root.children if c.pos_ in allowed_pos}
    else:
        children = {c.dep_: c for c in root.children}
    for dep in allowed_dep:
        if (o:=children.get(dep, None)):
            return o
            return extract_span_from_entity(children.get(dep))
    return None

def _get_negate_verb(span):
    def exception(token, i=0, j=0, target=''):
        cur = token.i-span.start
        return span[cur-i:cur+1+j].text.lower() == target
    verb_pos = ['AUX','VERB','VB','VBD','VBG','VBG','VBN','VBP','VBZ']
    visited = defaultdict(bool) # verb: is_negate
    for neg in span:
        flag = False
        if neg.dep_ == 'neg' or neg.text.lower() in NEGATION_WORDS:
            if exception(neg,1,0,'if not') or exception(neg,-1,2,'help with'):
                continue
            while neg != neg.head:
                neg = neg.head
                if neg.pos_ in verb_pos:
                    flag = True; break
            visited[neg] ^= flag
    return visited
        
    
def _get_verbs(span, matches):
    visited = set()
    for match in [span[start:end] for _, start, end in matches]:
        if (i := match.root.i) not in visited:
            visited.add(i)
            yield match

def _get_subject(verb):
    """
    direct subject
    --------------
        nsubj: subject
        nsubjpass: passive sense, e.g., A was defeated by B, here A is the nsubjpass of verb defeated
    indirect subject
    ----------------
    when there involves clause, we should carry out some further investigation:
        coordinating conjunction (conj): I went to the store [and] bought some milk.
        conjunction/punctuation (cc): I went to the store[, but] I didn't buy anything
        adverbial clause modifier (advcl): I was so excited [that I started dancing]
        clausal modifier of noun (acl): The teacher, [who was wearing a green dress], was talking to the students.
        clausal complement (comp): He asked me [to go home].
    """
    def get_subject_helper(root, subj_type=["nsubj", "nsubjpass", "csubj", "csubjpass", "agent", "expl"]):
        for c in root.children:
            if c.dep_ in subj_type:
                return extract_span_from_entity(c)
        while root.dep_ in ["conj", "cc", "advcl", "acl", "ccomp", "ROOT"]:
            for c in root.children:
                if c.dep_ in ["nsubj", "nsubjpass"]:
                    return extract_span_from_entity(c)
                if c.dep_ in ["acl", "advcl"]:
                    subject = find_verb_subject(c)
                    return extract_span_from_entity(subject) if subject else None
            # Break cycles
            if root == root.head: break
            else: root = root.head
        for c in root.children:
            if c.dep_ in subj_type:
                return extract_span_from_entity(c)
        return None
    subject = get_subject_helper(verb.root)
    if subject:
        for c in subject.root.children:
            if c.dep_ == 'appos':  #my sisiter, sarah
                return extract_span_from_entity(c) 
    if subject and not any(c.dep_=='cc' for c in subject):
        return extract_span_from_entity(subject.root)
    return subject

def is_negated_verb(verb, doc):
    token = verb.root
    if token.doc.is_parsed is False:
        raise ValueError('token is not parsed')
    if token.pos_ == 'VERB' and any(c.dep_ == 'neg' for c in token.children):
        return True
    else:
        return False

f = lambda i: i or ''

@dataclass
class Clause:
    subject: Optional[Span] = None
    verbal:  Optional[Span] = None
    object:  Optional[Span] = None
    negate:  bool = False

    def __repr__(self):
        negate = '!' if self.negate else ''
        return f'<{f(self.subject)}, {negate}{f(self.verbal)}, {f(self.object)}>'

    def __str__(self):
        negate = '!' if self.negate else ''
        return f'{negate} {f(self.subject)} {f(self.verbal)} {f(self.object)}'.lower().strip()

    def __contains__(self, span: str):
        if span.lower() in str(self): return True
    
    def contains(self, type = 'subject', span: str = 'i'):
        return span.lower() in getattr(self, type).text.lower()
    
    @property
    def valid(self): return self.object and self.subject

class Clauses:

    def __init__(self):
        self.clauses = []
        self.n = 0

    def __repr__(self):
        return ' | '.join(repr(x) for x in self.clauses)

    def get_helper(self, query: str, fetch_all=False):
        result = []
        for clause in self.clauses:
            if query in clause:
                if fetch_all: result.append(clause)
                else: return clause
        return result

    def get(self, span: Span):
        """return first-person and negation"""
        clause = self.get_helper(span.root.text, fetch_all=True)
        if clause: return clause
        span_clause = RE.extract_clauses(span)
        clauses = []
        for sc in span_clause:
            clauses.append(self.get_helper(str(sc)))
        return list(filter(None, clauses))

    def add(self, *clauses: Clause):
        if isinstance(clauses, Clause):
            clauses = [clauses]
        for clause in clauses:
            self.clauses.append(clause)
            self.n += 1

    def __iter__(self):
        yield from self.clauses
    
    def __getitem__(self, i): 
        return self.clauses[i]
        

@Language.factory(
    'relation_extract', requires=["doc.sents"], assigns=["doc._.clauses", "span._.clauses"]
)
class RE:
    verb_matcher = None

    def __init__(self, nlp, name):
        self.name = name
        self.prepare_everything(nlp)
        RE.verb_matcher = MedspacyMatcher(nlp)
        RE.verb_matcher.add(V_RULES)
    
    def prepare_everything(self, nlp):
        install_extensions(Span, 'clauses', None)
        install_extensions(Span, 'negates', defaultdict(bool))
        install_extensions(Doc, 'clauses', Clauses())

    @classmethod
    def extract_clauses(cls, span: Span):
        """
        - we first match the verb
        - then we obtain subject associated to the verb
        - indirect object: e.g., he gave [her] the book
        - direct object: e.g., i read [the book]
        """
        subject = None
        for verb in _get_verbs(span, cls.verb_matcher(span)):
            subject = _get_subject(verb) or subject
            object = find_match_child(verb.root, OBJ_DEPS, allowed_pos=['NOUN','ADJ'])
            is_negate = span._.negates.get(verb.root, False)
            for c in verb.root.children:
                if c.dep_ in ("prep", "advmod", "agent"):
                    # excluding 
                    if (adv := extract_span_from_entity(c, add_exclude=['advmod'])):
                        yield Clause(subject, verb, adv, is_negate)
            yield Clause(subject, verb, object, is_negate)
                
    def __call__(self, doc): 
        # if doc.has_extension('trf_data'):
        #     doc.remove_extension('trf_data')
        for sent in doc.sents:
            clauses = Clauses()
            sent._.negates = _get_negate_verb(sent)
            for clause in self.extract_clauses(sent):
                if clause.valid: clauses.add(clause)
            sent._.clauses = clauses
            doc._.clauses.add(*clauses)
        return doc

@Language.factory(
    'relation_final', requires=["doc.sents", "doc.ents"], assigns=["span._.is_self", "span._.is_neg"]
)
class RF:

    def __init__(self,nlp, name):
        self.name = name
        install_extensions(Span, 'is_self', False)
        install_extensions(Span, 'is_neg', False)

    def __call__(self, doc): 
        for e in doc.ents:
            clauses = e.sent._.clauses
            e_clause = clauses.get(e)
            self_clause, other_clause = _split_self_clause(e_clause)
            e._.is_self = len(self_clause) > 0
            e._.is_neg = _get_negate_ent((self_clause or other_clause), e)
        return doc

def _split_self_clause(clauses: Clauses):
    # split clauses by the standard of whether it includes first-person
    fp_clauses, other_clauses = [], []
    for clause in clauses:
        if set(clause.subject.text.split(' ')) & FIRST_PERSON:
            fp_clauses.append(clause)
        else:
            other_clauses.append(clause)
    return fp_clauses, other_clauses
    
def _get_negate_ent(clauses: Clauses, entity: Clause):
    # special case: target (entity) clause contains negation 
    ent_verb = _get_negate_verb(entity)
    is_neg = False
    for clause in clauses:
        is_neg = clause.negate
        is_neg ^= ent_verb.get(clause.verbal.root, False)
        if is_neg: break
    return is_neg


def remove_extensions():
    for obj, ext in [
        (Token, _token_extensions), (Span, _span_extensions), (Doc, _doc_extensions)
    ]:
        [obj.remove_extension(k) for k in ext]

remove_extensions()

@Language.factory('depress_context')
class DepressContext(ConText):
    """
    The ConText for entity postprocessing. This componnt will match modifiers in docs, define their scope and identifies edge between entities and modifiers:
        - Span._.modifiers: a list of `ConTextModifier` objects which modify an entity
        - Doc._.context_graph: a ConTextGraph object which contains entities, modifiers and edges between them

    Args:
        rules: either a path to a json file or `default`
        span_attrs: either an attribute dictionary (change ._.is_xxx) or `default`
        terminating_types: e.g., {"NEGATED_EXISTENCE": ["POSITIVE_EXISTENCE", "UNCERTAIN"]} will terminate negate with positive or uncertain
    """
    def __init__(
        self, nlp: Language, name='depress_context', 
        rules='default', span_attrs='default',
        max_scope=None, max_targets=None, allowed_types=None, excluded_types=None, terminating_types=None,
    ):
        self.nlp = nlp
        self.name = name
        self.prune_on_modifier_overlap = True
        self.prune_on_target_overlap = False
        self.context_attributes_mapping = None
        self.__matcher = MedspacyMatcher(
            nlp, name=name, phrase_matcher_attr='LOWER', prune=True,
        )
        self.input_span_type = 'ents'
        self.span_group_name = 'custom_context'
        self.max_scope = None
        self.allowed_types = None
        self.excluded_types = None
        self.max_targets = None
        self.rules_attr = dict(
            max_scope=max_scope, excluded_types=excluded_types,
            allowed_types=allowed_types, max_targets=max_targets
        )
        # ---- suppose "positive for flu, negative for RSV"
        # ---- here want positive to modify only flu not RSV
        # ---- we can add Rule(positive, terminated_by={'negative'})
        self.terminating_types = dict()
        if terminating_types:
            self.terminating_types = {k.upper(): v for (k,v) in terminating_types.items()}
        # ---- globally set Span/Doc/Token attributes
        self.span_attrs(span_attrs)
        self.graph_attrs()
        if rules != 'default':
            self.add(ConTextRule.from_json(rules))
        else:
            self.add(C_RULES)
        

    def span_attrs(self, tag='default'):
        all_attrs = set(k for v in DEFAULT_ATTRIBUTES.values() for k in v)
        if tag == 'default':
            self.context_attributes_mapping = DEFAULT_ATTRIBUTES
            for attr in all_attrs:
                try:
                    Span.set_extension(attr, default=False)
                except ValueError:
                    pass
        elif tag:
            for _, attr_dict in tag.items():
                for attr in attr_dict:
                    if not Span.has_extension(attr):
                        raise ValueError(
                            f"Custom extension {attr} has not been set. Please ensure Span.set_extension is "
                            f"called for your pipeline's custom extensions."
                        )
            self.context_attributes_mapping = tag
    
    def graph_attrs(self):
        Span.set_extension("modifiers", default=(), force=True)
        Doc.set_extension("context_graph", default=None, force=True)
    
    
    def add(self, rules):
        """
        add context rules to context
        """
        if isinstance(rules, ConTextRule):
            rules = [rules]
        for rule in rules:
            if not isinstance(rule, ConTextRule):
                raise TypeError(f"Rules must type ConTextRule, not {type(rule)}.")
            # ---- update rule attribute with global if not set
            for attr, val in self.rules_attr.items():
                if val is None: continue
                if getattr(rule, attr) is None:
                    setattr(rule, attr, val)
            cat = rule.category.upper()
            if cat in self.terminating_types:
                for other_cat in self.terminating_types[cat]:
                    rule.terminated_by.add(other_cat.upper())
        self.__matcher.add(rules)

    def __call__(self, doc, targets: str = None) -> Doc:
        if not targets: targets = doc.ents
        if isinstance(targets, str): targets = getattr(doc._, targets)
        cg = ConTextGraph(
            prune_on_modifier_overlap=self.prune_on_target_overlap
        )
        cg.targets, cg.modifiers = targets, []
        matches = self.__matcher(doc)
        for (match_id, start, end) in matches:
            rule = self.__matcher.rule_map[self.nlp.vocab[match_id].text]
            modifier = ConTextModifier(rule, start, end, doc, max_scope=self.max_scope)
            cg.modifiers.append(modifier)
        cg.update_scopes()
        cg.apply_modifiers()
        for target, modifier in cg.edges:
            target._.modifiers += (modifier,)
        if self.context_attributes_mapping:
            self.set_context_attributes(cg.edges)
        doc._.context_graph = cg
        return doc

        
    




