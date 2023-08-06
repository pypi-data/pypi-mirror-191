from tknlp.utils import import_file, oreplace
from spacy.tokens import Span, Doc, Token
from tknlp.spacy.covid_rule import (
    concept_tag_rules, preprocess_rules, section_rules, context_rules, target_rules, postprocess_rules
)
from spacy.language import Language

DEFAULT_PIPENAMES = [
    "preprocessor",
    "tagger",
    "parser",
    "concept_tagger",
    "target_matcher",
    "sectionizer",
    "context",
    "postprocessor",
    "document_classifier"
]

CONTEXT_MAPPING = {
    "NEGATED_EXISTENCE": {"is_negated": True},
    "FUTURE/HYPOTHETICAL": {"is_future": True},
    "HISTORICAL": {"is_historical": True},
    "DEFINITE_POSITIVE_EXISTENCE": {"is_positive": True},
    "ADMISSION": {"is_positive": True},
    "NOT_RELEVANT": {"is_not_relevant": True},
    "UNCERTAIN": {"is_uncertain": True},
    "UNLIKELY": {"is_uncertain": True},
    "SCREENING": {"is_screening": True},
    "OTHER_EXPERIENCER": {"is_other_experiencer": True},
    "CONTACT": {"is_other_experiencer": True},
    "PATIENT_EXPERIENCER": {"is_other_experiencer": False, "is_positive": True},
}

SECTION_ATTRS = {
    "diagnoses": {"is_positive": True},
    "observation_and_plan": {"is_positive": True},
    "past_medical_history": {"is_positive": True},
    "problem_list": {"is_positive": True},
}

def _set_attributes():
    Span.set_extension("is_future", default=False, force=True)
    Span.set_extension("is_historical", default=False, force=True)
    Span.set_extension(
        "is_positive", default=False, force=True
    )  # Explicitly has a positive indicator
    Span.set_extension(
        "is_not_relevant", default=False, force=True
    )  # News reports, etc..
    Span.set_extension("is_negated", default=False, force=True)
    Span.set_extension("is_uncertain", default=False, force=True)
    Span.set_extension("is_screening", default=False, force=True)
    Span.set_extension("is_other_experiencer", default=False, force=True)
    Span.set_extension("concept_tag", default="", force=True)
    Doc.set_extension("cov_classification", default=None, force=True)


@Language.factory("document_classifier")
class DocumentClassifier:
    """Classify a document as either 'POS', 'UNK', or 'NEG'.
        - 'POS': there is at least one mention of COVID-19
            with a positive status and no excluding modifiers.
            Examples:
                - "The patient is positive for COVID-19"
                - "Her SARS-COV-2 results came back as DETECTED"
                - "Pt admitted to hospital for COVID-19"
        - 'UNK': There is are no positive mentions of COVID-19
            and at least one non-excluded or uncertain mention.
            Examples:
                - "Patient with suspicion for COVID-19."
                - "Patient tested for COVID-19, results pending."
                - "Cancelled appt due to COVID-19"
        - 'NEG': There are no positive, uncertain, or unasserted mentions.
            Examples:
                - "The patient tested negative for SAS-COV-2"
                - "He does not have novel coronavirus"
                - "Patient presents for routine follow-up."
                - "Visit done via telephone due to COVID-19 precautions"
    """
    def __init__( self, nlp, name: str = "medspacy_doc_consumer" ):
        self.nlp = nlp
        self.name = name
                 
    def classify(self, doc):
        excluded_ents = set(); positive_ents = set(); unasserted_ents = set()
        for ent in doc.ents:
            if ent.label_ != "COVID-19":
                continue
            # If the entity is negated, experienced by someone else, Future/hypothetical, or marked as not relevant, considered this entity to be 'excluded'
            if any([ 
                ent._.is_negated, ent._.is_other_experiencer, ent._.is_future, ent._.is_not_relevant, 
            ]):
                excluded_ents.add(ent)
            # If it is 'positive' and not uncertain, consider it to be a 'positive' ent
            elif ent._.is_positive and not ent._.is_uncertain:
                positive_ents.add(ent)
            # If either there are no excluding modifiers or it is marked as 'uncertain', consider it 'unasserted
            else:
                unasserted_ents.add(ent)

        if positive_ents: doc_classification = "POS"
        elif unasserted_ents: doc_classification = "UNK"
        else: doc_classification = "NEG"
        return doc_classification

    def __call__(self, doc):
        doc._.cov_classification = self.classify(doc)
        return doc

        
def load(model="default", enable=None, disable=None, load_rules=True, set_attributes=True):
    """Load a spaCy language object with cov_bsv pipeline components.
    By default, the base model will be 'en_core_web_sm' with the 'tagger'
    and 'parser' pipeline components, supplemented with the following custom
    components:
        - preprocessor (set to be nlp.tokenizer): Modifies the preprocessed text and returns
            a tokenized Doc. Preprocess rules are defined in cov_bsv.knowledge_base.preprocess_rules
        - concept_tagger: Assigns a semantic tag in a custom attribute "token._.concept_tag"
            to each Token in a Doc, which helps with concept extraction and normalization.
            Concept tag rules are defined in cov_bsv.knowledge_base.concept_tag_rules.
        - target_matcher: Extracts spans to doc.ents using extended rule-based matching.
            Target rules are defined in cov_bsv.knowledge_base.target_rules.
        - sectionizer: Identifies note section headers in the text and assigns section titles to
            entities and tokens contained in that section. Section patterns are defined in
            cov_bsv.knowledge_base.section_patterns.
        - context: Identifies semantic modifiers of entities and asserts attributes such as
            positive status, negation, and other experiencier. Context rules are defined in
            cov_bsv.knowledge_base.context_rules.
        - postprocessor: Modifies or removes the entity based on business logic. This handles
            special cases or complex logic using the results of earlier entities. Postprocess rules
            are defined in cov_bsv.knowledge_base.postprocess_rules.
        - document_classifier: Assigns a label of "POS", "UNK", or "NEG" to the doc._.cov_classification.
            A document will be classified as positive if it has at least one positive, non-excluded entity.
    Args:
        model: The name of the base spaCy model to load. If "default" will load the tagger and parser
            from "en_core_web_sm".
        enable (iterable or None): A list of component names to include in the pipeline.
        If None, will include all pipeline components listed above.
        disable (iterable or None): A list of component names to exclude.
            Cannot be set if `enable` is not None.
        load_rules (bool): Whether or not to include default rules for custom components. Default True.
        set_attributes (bool): Whether or not to register custom attributes to spaCy classes. If load_rules is True,
            this will automatically be set to True because the rules in the knowledge base rely on these custom attributes.
            The following extensions are registered (all defaults are False unless specified):
                Span._.is_future
                Span._.is_historical
                Span._.is_positive
                Span._.is_not_relevant
                Span._.is_negated
                Span._.is_uncertain
                Span._.is_screening
                Span._.is_other_experiencer
                Span._.concept_tag (default "")
    Returns:
        nlp: a spaCy Language object
    """
    if enable is not None and disable is not None:
        raise ValueError("Either `enable` or `disable` must be None.")
    if disable is not None:
        # If there's a single pipe name, nest it in a set
        if isinstance(disable, str):
            disable = {disable}
        else:
            disable = set(disable)
        enable = set(DEFAULT_PIPENAMES).difference(set(disable))
    elif enable is not None:
        if isinstance(enable, str):
            enable = {enable}
        else:
            enable = set(enable)
        disable = set(DEFAULT_PIPENAMES).difference(enable)
    else:
        enable = DEFAULT_PIPENAMES
        disable = set()

    if model == "default":
        model = "en_core_web_sm"
        disable.add("ner")

    if set_attributes:
        _set_attributes()

    import spacy
    nlp = spacy.load(model, disable=disable)

    if "preprocessor" in enable:
        from medspacy.preprocess import Preprocessor

        preprocessor = Preprocessor(nlp.tokenizer)
        if load_rules:
            preprocessor.add(preprocess_rules)
        nlp.tokenizer = preprocessor

    if "concept_tagger" in enable:
        concept_tagger = nlp.add_pipe("medspacy_concept_tagger")
        if load_rules:
            for (_, rules) in concept_tag_rules.items():
                concept_tagger.add(rules)

    if "target_matcher" in enable:
        target_matcher = nlp.add_pipe("medspacy_target_matcher")
        if load_rules:
            for (_, rules) in target_rules.items():
                target_matcher.add(rules)

    if "sectionizer" in enable:
        sectionizer = nlp.add_pipe("medspacy_sectionizer", config={'rules':None, 'span_attrs':SECTION_ATTRS})
        if load_rules:
            sectionizer.add(section_rules)

    if "context" in enable:
        context = nlp.add_pipe("medspacy_context", config=dict(span_attrs=CONTEXT_MAPPING, rules=None, prune_on_modifier_overlap=True))
        if load_rules: 
            context.add(context_rules)

    if "postprocessor" in enable:
        postprocessor = nlp.add_pipe("medspacy_postprocessor", config={'debug':False})
        if load_rules:
            postprocessor.add(postprocess_rules)

    if "document_classifier" in enable:
        nlp.add_pipe("document_classifier")

    return nlp