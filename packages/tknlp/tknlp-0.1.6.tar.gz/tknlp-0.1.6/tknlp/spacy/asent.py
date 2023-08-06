from spacy.language import Language
from spacy.tokens import Doc, Span, Token

from typing import Dict, Iterable, Optional, Callable
from tknlp.spacy.asent_rule import lexicons



class Asent:
    """spaCy v.3.0 component for adding an asent sentiment models to `Doc`
    objects.
    Ading the Token extentions 'valence', 'intensifier', 'is_negation',
    'is_negated', 'is_contrastive_conj' and 'polarity' as well as the
    Span and Doc extension 'polarity'.
    """
    def __init__( 
        self, nlp: Language, lexicon: Dict[str, float], name: str = "asent",
        intensifiers: Dict[str, float] = {}, negations: Iterable[str] = set(), contrastive_conjugations: Iterable[str] = set(),
        lowercase: bool = True, lemmatize: bool = False, force: bool = False,
    ):
        """Initialize component.
        Args:
            nlp (Language): A spaCy language pipeline for which to add the component to
            name (str): The name of the component
            lexicon (Dict[str, float]): The lexicion used to look up the valence scores of a word.
            intensifiers (Dict[str, float]): A dictionary of intensifiers (e.g. {"very": 0.293}). Defaults to {}, indicating no intensifiers is used.
            negations (Iterable[str]): A list of negations (e..g "not"). Defaults to an empty set indicatin no negations will be used.
            contrastive_conjugations (Iterable[str]): A list of contrastive conjugations (e.g. "but"). Defaults to empty set indicating no contrastive conjugations will be used.
            lowercase (bool): Should be text be lowercases before looking up in the lexicons? Defaults to True.
            lemmatize (bool): Should be text be lemmatized before looking up in the lexicons? Defaults to False.
            force (bool): Should existing extensions be overwritten? Defaults to False.
        """
        self.name = name

        if (not Token.has_extension("valence")) or (force is True):
            Token.set_extension(
                "valence",
                getter=make_valance_getter(
                    lexicon=lexicon,
                    lowercase=lowercase,
                    lemmatize=lemmatize,
                ),
                force=force,
            )

        if (not Token.has_extension("intensifier")) or (force is True):
            Token.set_extension(
                "intensifier",
                getter=make_intensifier_getter(
                    intensifiers=intensifiers,
                    lemmatize=lemmatize,
                    lowercase=lowercase,
                ),
                force=force,
            )

        if (not Token.has_extension("is_negation")) or (force is True):
            Token.set_extension(
                "is_negation",
                getter=make_is_negation_getter(
                    negations=negations,
                    lemmatize=lemmatize,
                    lowercase=lowercase,
                ),
                force=force,
            )

        if (not Token.has_extension("is_negated")) or (force is True):
            Token.set_extension(
                "is_negated",
                getter=make_is_negated_getter(),
                force=force,
            )

        if (not Token.has_extension("is_contrastive_conj")) or (force is True):
            Token.set_extension(
                "is_contrastive_conj",
                getter=make_is_contrastive_conj_getter(
                    contrastive_conjugations=contrastive_conjugations,
                    lemmatize=lemmatize,
                    lowercase=lowercase,
                ),
                force=force,
            )

        if (not Token.has_extension("polarity")) or (force is True):
            Token.set_extension(
                "polarity",
                getter=make_token_polarity_getter(
                    valence_getter=None,
                    is_negation_getter=None,
                    intensifier_getter=None,
                ),
                force=force,
            )

        if (not Span.has_extension("polarity")) or (force is True):
            Span.set_extension(
                "polarity", force=force,
                getter=make_span_polarity_getter( 
                    polarity_getter=None, contrastive_conj_getter=None,
                ),
            )


@Language.factory("asent_en_v1")
def create_en_sentiment_component(nlp: Language, name: str) -> Language:
    """
    Allows the English sentiment to be added to a spaCy pipe using nlp.add_pipe("asent_en_v1").
    """
    return Asent(nlp, 
        lexicon = lexicons.get('lexicon_en_v1'),
        intensifiers = lexicons.get('intensify_en_v1'),
        negations = lexicons.get('negation_en_v1'),
        contrastive_conjugations = lexicons.get('contrast_en_v1'),
        lowercase =True, lemmatize =False
    )

