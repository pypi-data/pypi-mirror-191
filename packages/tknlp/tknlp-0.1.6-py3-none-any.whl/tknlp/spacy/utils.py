"""
Set of small utility functions that take Spacy objects as input.
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import itertools
import re


from spacy.symbols import NOUN, PROPN, VERB
from spacy.tokens import Doc, Span, Token
from spacy import Language, util
from transformers import pipeline

from wasabi import msg

from tknlp.spacy import constant as C
from tknlp.typing_ import Iterable, List


def subject_verb_object_triples(doc):
    """
    Extract an ordered sequence of subject-verb-object (SVO) triples from a
    spacy-parsed doc. Note that this only works for SVO languages.
    Args:
        doc (``textacy.Doc`` or ``spacy.Doc`` or ``spacy.Span``)
    Yields:
        Tuple[``spacy.Span``, ``spacy.Span``, ``spacy.Span``]: The next 3-tuple
        of spans from ``doc`` representing a (subject, verb, object) triple,
        in order of appearance.
    """
    if isinstance(doc, Span): sents = [doc]
    else:  sents = doc.sents

    for sent in sents:
        start_i = sent[0].i
        verbs = get_main_verbs_of_sent(sent)
        for verb in verbs:
            subjs = get_subjects_of_verb(verb)
            if not subjs: continue
            objs = get_objects_of_verb(verb)
            if not objs: continue
            # ---- further processing: add adj/compound and combine them with verb
            verb_span = get_span_for_verb_auxiliaries(verb)
            verb = sent[verb_span[0] - start_i: verb_span[1] - start_i + 1]
            for subj in subjs:
                subj = sent[get_span_for_compound_noun(subj)[0] - start_i: subj.i - start_i + 1]
                for obj in objs:
                    if obj.pos == NOUN:
                        span = get_span_for_compound_noun(obj)
                    elif obj.pos == VERB:
                        span = get_span_for_verb_auxiliaries(obj)
                    else:
                        span = (obj.i, obj.i)
                    obj = sent[span[0] - start_i: span[1] - start_i + 1]
                    yield (subj, verb, obj)


def is_plural_noun(token):
    """
    Returns True if token is a plural noun, False otherwise.
    Args:
        token (``spacy.Token``): parent document must have POS information
    Returns:
        bool
    """
    if token.doc.is_tagged is False:
        raise ValueError('token is not POS-tagged')
    if token.pos == NOUN and token.lemma != token.lower:
        return True
    else:
        return False


def is_negated_verb(token):
    """
    Returns True if verb is negated by one of its (dependency parse) children,
    False otherwise.
    Args:
        token (``spacy.Token``): parent document must have parse information
    Returns:
        bool
    """
    if token.doc.is_parsed is False:
        raise ValueError('token is not parsed')
    if token.pos == VERB and any(c.dep_ == 'neg' for c in token.children):
        return True
    else:
        return False


def preserve_case(token):
    """
    Returns True if `token` is a proper noun or acronym, False otherwise.
    Args:
        token (``spacy.Token``): parent document must have POS information
    Returns:
        bool
    """
    if token.doc.is_tagged is False:
        raise ValueError('token is not POS-tagged')
    if token.pos == PROPN or is_acronym(token.text):
        return True
    else:
        return False


def normalized_str(token):
    """
    Return as-is text for tokens that are proper nouns or acronyms, lemmatized
    text for everything else.
    Args:
        token (``spacy.Token`` or ``spacy.Span``)
    Returns:
        str
    """
    if isinstance(token, Token):
        return token.text if preserve_case(token) else token.lemma_
    elif isinstance(token, Span):
        return ' '.join(subtok.text if preserve_case(subtok) else subtok.lemma_
                        for subtok in token)
    else:
        raise TypeError(
            'Input must be a spacy Token or Span, not {}.'.format(type(token))
            )


def merge_spans(spans):
    """
    Merge spans *in-place* within parent doc so that each takes up a single token.
    Args:
        spans (Iterable[``spacy.Span``])
    """
    for span in spans:
        try:
            span.merge(span.root.tag_, span.text, span.root.ent_type_)
        except IndexError as e:
            msg.fail('Unable to merge span "%s"; skipping...'%span.text)


def get_main_verbs_of_sent(sent):
    """Return the main (non-auxiliary) verbs in a sentence."""
    return [tok for tok in sent
            if tok.pos == VERB and tok.dep_ not in {'aux', 'auxpass'}]


def get_subjects_of_verb(verb):
    """Return all subjects of a verb according to the dependency parse."""
    subjs = [tok for tok in verb.lefts
             if tok.dep_ in C.SUBJ_DEPS]
    # get additional conjunct subjects
    subjs.extend(tok for subj in subjs for tok in _get_conjuncts(subj))
    return subjs


def get_objects_of_verb(verb):
    """
    Return all objects of a verb according to the dependency parse,
    including open clausal complements.
    """
    objs = [tok for tok in verb.rights if tok.dep_ in C.OBJ_DEPS]
    # get open clausal complements (xcomp)
    objs.extend(tok for tok in verb.rights if tok.dep_ == 'xcomp')
    # get additional conjunct objects
    objs.extend(tok for obj in objs for tok in _get_conjuncts(obj))
    return objs


def _get_conjuncts(tok):
    """
    Return conjunct dependents of the leftmost conjunct in a coordinated phrase,
    e.g. "Burton, [Dan], and [Josh] ...".
    """
    return [right for right in tok.rights
            if right.dep_ == 'conj']


def get_span_for_compound_noun(noun):
    """
    Return document indexes spanning all (adjacent) tokens
    in a compound noun.
    """
    min_i = noun.i - sum(1 for _ in itertools.takewhile(lambda x: x.dep_ == 'compound',
                                                        reversed(list(noun.lefts))))
    return (min_i, noun.i)


def get_span_for_verb_auxiliaries(verb):
    """
    Return document indexes spanning all (adjacent) tokens
    around a verb that are auxiliary verbs or negations.
    """
    min_i = verb.i - sum(1 for _ in itertools.takewhile(lambda x: x.dep_ in C.AUX_DEPS,
                                                        reversed(list(verb.lefts))))
    max_i = verb.i + sum(1 for _ in itertools.takewhile(lambda x: x.dep_ in C.AUX_DEPS,
                                                        verb.rights))
    return (min_i, max_i)

    
def is_acronym(token, exclude=None):
    """
    Pass single token as a string, return True/False if is/is not valid acronym.
    Args:
        token (str): single word to check for acronym-ness
        exclude (Set[str]): if technically valid but not actually good acronyms
            are known in advance, pass them in as a set of strings; matching
            tokens will return False
    Returns:
        bool
    """
    # exclude certain valid acronyms from consideration
    if exclude and token in exclude:
        return False
    # don't allow empty strings
    if not token:
        return False
    # don't allow spaces
    if ' ' in token:
        return False
    # 2-character acronyms can't have lower-case letters
    if len(token) == 2 and not token.isupper():
        return False
    # acronyms can't be all digits
    if token.isdigit():
        return False
    # acronyms must have at least one upper-case letter or start/end with a digit
    if (not any(char.isupper() for char in token) and
            not (token[0].isdigit() or token[-1].isdigit())):
        return False
    # acronyms must have between 2 and 10 alphanumeric characters
    if not 2 <= sum(1 for char in token if char.isalnum()) <= 10:
        return False
    # only certain combinations of letters, digits, and '&/.-' allowed
    if not C.ACRONYM_REGEX.match(token):
        return False
    return True


def keyword_in_context(text, keyword, ignore_case=True, window_width=50, print_only=True):
    """
    Search for ``keyword`` in ``text`` via regular expression, return or print strings
    spanning ``window_width`` characters before and after each occurrence of keyword.
    Args:
        text (str): text in which to search for ``keyword``
        keyword (str): technically, any valid regular expression string should work,
            but usually this is a single word or short phrase: "spam", "spam and eggs";
            to account for variations, use regex: "[Ss]pam (and|&) [Ee]ggs?"
            N.B. If keyword contains special characters, be sure to escape them!!!
        ignore_case (bool): if True, ignore letter case in `keyword` matching
        window_width (int): number of characters on either side of
            `keyword` to include as "context"
        print_only (bool): if True, print out all results with nice
            formatting; if False, return all (pre, kw, post) matches as generator
            of raw strings
    Returns:
        generator(Tuple[str, str, str]), or None
    """
    flags = re.IGNORECASE if ignore_case is True else 0
    if print_only is True:
        for match in re.finditer(keyword, text, flags=flags):
            line = '{pre} {kw} {post}'.format(
                pre=text[max(0, match.start() - window_width): match.start()].rjust(window_width),
                kw=match.group(),
                post=text[match.end(): match.end() + window_width].ljust(window_width))
            print(line)
    else:
        return ((text[max(0, match.start() - window_width): match.start()],
                 match.group(),
                 text[match.end(): match.end() + window_width])
                for match in re.finditer(keyword, text, flags=flags))


def clean_terms(terms):
    """
    Clean up a sequence of single- or multi-word strings: strip leading/trailing
    junk chars, handle dangling parens and odd hyphenation, etc.
    Args:
        terms (Iterable[str]): sequence of terms such as "presidency", "epic failure",
            or "George W. Bush" that may be _unclean_ for whatever reason
    Yields:
        str: next term in `terms` but with the cruft cleaned up, excluding terms
        that were _entirely_ cruft
    Warning:
        Terms with (intentionally) unusual punctuation may get "cleaned"
        into a form that changes or obscures the original meaning of the term.
    """
    # get rid of leading/trailing junk characters
    terms = (C.LEAD_TAIL_CRUFT_TERM_RE.sub('', term)
             for term in terms)
    terms = (C.LEAD_HYPHEN_TERM_RE.sub(r'\1', term)
             for term in terms)
    # handle dangling/backwards parens, don't allow '(' or ')' to appear without the other
    terms = ('' if term.count(')') != term.count('(') or term.find(')') < term.find('(')
             else term if '(' not in term
             else C.DANGLING_PARENS_TERM_RE.sub(r'\1\2\3', term)
             for term in terms)
    # handle oddly separated hyphenated words
    terms = (term if '-' not in term
             else C.NEG_DIGIT_TERM_RE.sub(r'\1\2', C.WEIRD_HYPHEN_SPACE_TERM_RE.sub(r'\1', term))
             for term in terms)
    # handle oddly separated apostrophe'd words
    terms = (C.WEIRD_APOSTR_SPACE_TERM_RE.sub(r'\1\2', term)
             if "'" in term else term
             for term in terms)
    # normalize whitespace
    terms = (C.NONBREAKING_SPACE_REGEX.sub(' ', term).strip()
             for term in terms)
    for term in terms:
        if re.search(r'\w', term):
            yield term


# dependency markers for subjects
SUBJECTS = {"nsubj", "nsubjpass", "csubj", "csubjpass", "agent", "expl"}
# dependency markers for objects
OBJECTS = {"dobj", "dative", "attr", "oprd"}
# POS tags that will break adjoining items
BREAKER_POS = {"CCONJ", "VERB"}
# words that are negations
NEGATIONS = {"no", "not", "n't", "never", "none"}


# does dependency set contain any coordinating conjunctions?
def contains_conj(depSet):
    return "and" in depSet or "or" in depSet or "nor" in depSet or \
           "but" in depSet or "yet" in depSet or "so" in depSet or "for" in depSet


# get subs joined by conjunctions
def _get_subs_from_conjunctions(subs):
    more_subs = []
    for sub in subs:
        # rights is a generator
        rights = list(sub.rights)
        rightDeps = {tok.lower_ for tok in rights}
        if contains_conj(rightDeps):
            more_subs.extend([tok for tok in rights if tok.dep_ in SUBJECTS or tok.pos_ == "NOUN"])
            if len(more_subs) > 0:
                more_subs.extend(_get_subs_from_conjunctions(more_subs))
    return more_subs


# get objects joined by conjunctions
def _get_objs_from_conjunctions(objs):
    more_objs = []
    for obj in objs:
        # rights is a generator
        rights = list(obj.rights)
        rightDeps = {tok.lower_ for tok in rights}
        if contains_conj(rightDeps):
            more_objs.extend([tok for tok in rights if tok.dep_ in OBJECTS or tok.pos_ == "NOUN"])
            if len(more_objs) > 0:
                more_objs.extend(_get_objs_from_conjunctions(more_objs))
    return more_objs


# find sub dependencies
def _find_subs(tok):
    head = tok.head
    while head.pos_ != "VERB" and head.pos_ != "NOUN" and head.head != head:
        head = head.head
    if head.pos_ == "VERB":
        subs = [tok for tok in head.lefts if tok.dep_ == "SUB"]
        if len(subs) > 0:
            verb_negated = _is_negated(head)
            subs.extend(_get_subs_from_conjunctions(subs))
            return subs, verb_negated
        elif head.head != head:
            return _find_subs(head)
    elif head.pos_ == "NOUN":
        return [head], _is_negated(tok)
    return [], False


# is the tok set's left or right negated?
def _is_negated(tok):
    parts = list(tok.lefts) + list(tok.rights)
    for dep in parts:
        if dep.lower_ in NEGATIONS:
            return True
    return False


# get all the verbs on tokens with negation marker
def _find_svs(tokens):
    svs = []
    verbs = [tok for tok in tokens if tok.pos_ == "VERB"]
    for v in verbs:
        subs, verbNegated = _get_all_subs(v)
        if len(subs) > 0:
            for sub in subs:
                svs.append((sub.orth_, "!" + v.orth_ if verbNegated else v.orth_))
    return svs


# get grammatical objects for a given set of dependencies (including passive sentences)
def _get_objs_from_prepositions(deps, is_pas):
    objs = []
    for dep in deps:
        if dep.pos_ == "ADP" and (dep.dep_ == "prep" or (is_pas and dep.dep_ == "agent")):
            objs.extend([tok for tok in dep.rights if tok.dep_  in OBJECTS or
                         (tok.pos_ == "PRON" and tok.lower_ == "me") or
                         (is_pas and tok.dep_ == 'pobj')])
    return objs


# get objects from the dependencies using the attribute dependency
def _get_objs_from_attrs(deps, is_pas):
    for dep in deps:
        if dep.pos_ == "NOUN" and dep.dep_ == "attr":
            verbs = [tok for tok in dep.rights if tok.pos_ == "VERB"]
            if len(verbs) > 0:
                for v in verbs:
                    rights = list(v.rights)
                    objs = [tok for tok in rights if tok.dep_ in OBJECTS]
                    objs.extend(_get_objs_from_prepositions(rights, is_pas))
                    if len(objs) > 0:
                        return v, objs
    return None, None


# xcomp; open complement - verb has no suject
def _get_obj_from_xcomp(deps, is_pas):
    for dep in deps:
        if dep.pos_ == "VERB" and dep.dep_ == "xcomp":
            v = dep
            rights = list(v.rights)
            objs = [tok for tok in rights if tok.dep_ in OBJECTS]
            objs.extend(_get_objs_from_prepositions(rights, is_pas))
            if len(objs) > 0:
                return v, objs
    return None, None


# get all functional subjects adjacent to the verb passed in
def _get_all_subs(v):
    verb_negated = _is_negated(v)
    subs = [tok for tok in v.lefts if tok.dep_ in SUBJECTS and tok.pos_ != "DET"]
    if len(subs) > 0:
        subs.extend(_get_subs_from_conjunctions(subs))
    else:
        foundSubs, verb_negated = _find_subs(v)
        subs.extend(foundSubs)
    return subs, verb_negated


# find the main verb - or any aux verb if we can't find it
def _find_verbs(tokens):
    verbs = [tok for tok in tokens if _is_non_aux_verb(tok)]
    if len(verbs) == 0:
        verbs = [tok for tok in tokens if _is_verb(tok)]
    return verbs


# is the token a verb?  (excluding auxiliary verbs)
def _is_non_aux_verb(tok):
    return tok.pos_ == "VERB" and (tok.dep_ != "aux" and tok.dep_ != "auxpass")


# is the token a verb?  (excluding auxiliary verbs)
def _is_verb(tok):
    return tok.pos_ == "VERB" or tok.pos_ == "AUX"


# return the verb to the right of this verb in a CCONJ relationship if applicable
# returns a tuple, first part True|False and second part the modified verb if True
def _right_of_verb_is_conj_verb(v):
    # rights is a generator
    rights = list(v.rights)

    # VERB CCONJ VERB (e.g. he beat and hurt me)
    if len(rights) > 1 and rights[0].pos_ == 'CCONJ':
        for tok in rights[1:]:
            if _is_non_aux_verb(tok):
                return True, tok

    return False, v


# get all objects for an active/passive sentence
def _get_all_objs(v, is_pas):
    # rights is a generator
    rights = list(v.rights)

    objs = [tok for tok in rights if tok.dep_ in OBJECTS or (is_pas and tok.dep_ == 'pobj')]
    objs.extend(_get_objs_from_prepositions(rights, is_pas))

    #potentialNewVerb, potentialNewObjs = _get_objs_from_attrs(rights)
    #if potentialNewVerb is not None and potentialNewObjs is not None and len(potentialNewObjs) > 0:
    #    objs.extend(potentialNewObjs)
    #    v = potentialNewVerb

    potential_new_verb, potential_new_objs = _get_obj_from_xcomp(rights, is_pas)
    if potential_new_verb is not None and potential_new_objs is not None and len(potential_new_objs) > 0:
        objs.extend(potential_new_objs)
        v = potential_new_verb
    if len(objs) > 0:
        objs.extend(_get_objs_from_conjunctions(objs))
    return v, objs


# return true if the sentence is passive - at he moment a sentence is assumed passive if it has an auxpass verb
def _is_passive(tokens):
    for tok in tokens:
        if tok.dep_ == "auxpass":
            return True
    return False


# resolve a 'that' where/if appropriate
def _get_that_resolution(toks):
    for tok in toks:
        if 'that' in [t.orth_ for t in tok.lefts]:
            return tok.head
    return None


# print information for displaying all kinds of things of the parse tree
def printDeps(toks):
    for tok in toks:
        print(tok.orth_, tok.dep_, tok.pos_, tok.head.orth_, [t.orth_ for t in tok.lefts], [t.orth_ for t in tok.rights])


# expand an obj / subj np using its chunk
def expand(item, tokens, visited):
    if item.lower_ == 'that':
        temp_item = _get_that_resolution(tokens)
        if temp_item is not None:
            item = temp_item

    parts = []

    if hasattr(item, 'lefts'):
        for part in item.lefts:
            if part.pos_ in BREAKER_POS:
                break
            if not part.lower_ in NEGATIONS:
                parts.append(part)

    parts.append(item)

    if hasattr(item, 'rights'):
        for part in item.rights:
            if part.pos_ in BREAKER_POS:
                break
            if not part.lower_ in NEGATIONS:
                parts.append(part)

    if hasattr(parts[-1], 'rights'):
        for item2 in parts[-1].rights:
            if item2.pos_ == "DET" or item2.pos_ == "NOUN":
                if item2.i not in visited:
                    visited.add(item2.i)
                    parts.extend(expand(item2, tokens, visited))
            break

    return parts


# convert a list of tokens to a string
def to_str(tokens):
    if isinstance(tokens, Iterable):
        return ' '.join([item.text for item in tokens])
    else:
        return ''


# find verbs and their subjects / objects to create SVOs, detect passive/active sentences
PR = [{'DEP':'nsubjpass'},{'DEP':'aux','OP':'*'},{'DEP':'auxpass'},{'TAG':'VBN'}]
class SVO:
    """Extract an ordered sequence of subject-verb-object (SVO) triplets
    
    """
    def __init__(self, passive=True):
        self.consider_passive = passive
        if passive:
            pass

    def __call__(doc):
        pass


def extract_triplets(text: str) -> List[str]:
    """
    parses the text to triplets
    1. Split the text into tokens
    2. If the token is <triplet>, <subj>, or <obj>, then set the current variable to the appropriate value
    3. If the token is not one of the above, then append it to the appropriate variable
    4. If the current variable is <subj>, then append the triplet to the list of triplets
    :param text: str - the text to be parsed
    :type text: str
    :return: A list of dictionaries.
    """
    triplets = []
    relation, subject, relation, object_ = "", "", "", ""
    text = text.strip()
    current = "x"
    for token in text.replace("<s>", "").replace("<pad>", "").replace("</s>", "").split():
        if token == "<triplet>":
            current = "t"
            if relation != "":
                triplets.append(
                    {"head": subject.strip(), "type": relation.strip(), "tail": object_.strip()}
                )
                relation = ""
            subject = ""
        elif token == "<subj>":
            current = "s"
            if relation != "":
                triplets.append(
                    {"head": subject.strip(), "type": relation.strip(), "tail": object_.strip()}
                )
            object_ = ""
        elif token == "<obj>":
            current = "o"
            relation = ""
        else:
            if current == "t":
                subject += " " + token
            elif current == "s":
                object_ += " " + token
            elif current == "o":
                relation += " " + token
    if subject != "" and relation != "" and object_ != "":
        triplets.append(
            {"head": subject.strip(), "type": relation.strip(), "tail": object_.strip()}
        )

    return triplets


@Language.factory(
    "rebel", requires=["doc.sents"], assigns=["doc._.rel"], 
    default_config={ "model_name": "Babelscape/rebel-large", "device": 0, },
)
class RebelComponent:
    def __init__(
        self, nlp, name, model_name: str, device: int,
    ):
        assert model_name is not None, ""
        self.triplet_extractor = pipeline(
            "text2text-generation", model=model_name, tokenizer=model_name, device=device
        )
        # Register custom extension on the Doc
        if not Doc.has_extension("rel"):
            Doc.set_extension("rel", default={})

    def _generate_triplets(self, sents: List[Span]) -> List[List[dict]]:
        """
        1. We pass the text of the sentence to the triplet extractor.
        2. The triplet extractor returns a list of dictionaries.
        3. We extract the token ids from the dictionaries.
        4. We decode the token ids into text.
        5. We extract the triplets from the text.
        6. We return the triplets.
        The triplet extractor is a model that takes a sentence as input and returns a list of dictionaries.
        Each dictionary contains the token ids of the extracted triplets.
        The token ids are the numbers that represent the words in the sentence.
        For example, the token id of the word "the" is 2.
        The token ids are decoded into text using the tokenizer.
        The tokenizer is a model that takes a list of token ids as input and returns a list of words.
        :param sents: List[Span]
        :type sents: List[Span]
        :return: A list of lists of dicts.
        """
        sents = list(sents)
        output_ids = self.triplet_extractor(
            [sent.text for sent in sents], return_tensors=True, return_text=False
        )  # [0]["generated_token_ids"]
        extracted_texts = self.triplet_extractor.tokenizer.batch_decode(
            [out["generated_token_ids"] for out in output_ids]
        )
        extracted_triplets = []
        for text in extracted_texts:
            extracted_triplets.extend(extract_triplets(text))
        return extracted_triplets

    def set_annotations(self, doc: Doc, triplets: List[dict]):
        """
        The function takes a spacy Doc object and a list of triplets (dictionaries) as input.
        For each triplet, it finds the substring in the Doc object that matches the head and tail of the triplet.
        It then creates a spacy span object for each of the head and tail.
        Finally, it creates a dictionary of the relation type, head span and tail span and adds it to the Doc object
        :param doc: the spacy Doc object
        :type doc: Doc
        :param triplets: List[dict]
        :type triplets: List[dict]
        """
        for triplet in triplets:
            # get substring to spacy span
            head_span = re.search(triplet["head"], doc.text)
            tail_span = re.search(triplet["tail"], doc.text)
            # get spacy span
            if head_span is not None:
                head_span = doc.char_span(head_span.start(), head_span.end())
            else:
                head_span = triplet["head"]
            if tail_span is not None:
                tail_span = doc.char_span(tail_span.start(), tail_span.end())
            else:
                tail_span = triplet["tail"]
            offset = (head_span.start, tail_span.start)
            if offset not in doc._.rel:
                doc._.rel[offset] = {
                    "relation": triplet["type"],
                    "head_span": head_span,
                    "tail_span": tail_span,
                }

    def __call__(self, doc: Doc) -> Doc:
        """
        The function takes a doc object and returns a doc object
        :param doc: Doc
        :type doc: Doc
        :return: A Doc object with the sentence triplets added as annotations.
        """
        sentence_triplets = self._generate_triplets(doc.sents)
        self.set_annotations(doc, sentence_triplets)
        return doc

    def pipe(self, stream, batch_size=128):
        """
        It takes a stream of documents, and for each document,
        it generates a list of sentence triplets,
        and then sets the annotations for each sentence in the document
        :param stream: a generator of Doc objects
        :param batch_size: The number of documents to process at a time, defaults to 128 (optional)
        """
        for docs in util.minibatch(stream, size=batch_size):
            sents = []
            for doc in docs:
                sents += doc.sents
            sentence_triplets = self._generate_triplets(sents)
            index = 0
            for doc in docs:
                n_sent = len(list(doc.sents))
                self.set_annotations(doc, sentence_triplets[index : index + n_sent])
                index += n_sent
                yield doc
            