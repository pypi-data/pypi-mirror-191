from medspacy.preprocess import PreprocessingRule
from medspacy.target_matcher import TargetRule
from medspacy.section_detection import SectionRule
from medspacy.context import ConTextRule
from medspacy.postprocess import postprocessing_functions as F, PostprocessingRule, PostprocessingPattern
import re

# ----------------------- utility function: remove if match ----------------------------


def disambiguate_confirmed(matcher, doc, i, matches):
    """Disambiguate the phrase 'confirmed' 
    to avoid ambiguity of 'confirmed for appointment' vs. 'confirmed COVID-19'. """
    (_, start, end) = matches[i]
    span = doc[start:end]
    try:
        next_token = doc[i + 1]
        if next_token.lower_ in ["coronavirus", "covid-19", "covid", "sars-cov2"]:
            return
        if next_token.lower_ in ["that"]:
            matches.pop(i)
            return
    except IndexError:
        pass
    for text in ["appointment", "appt", "schedule", "phone", "telephone", "called", "ident", ]:
        if text in span.sent.lower_:
            matches.pop(i)
            return


def disambiguate_positive(matcher, doc, i, matches):
    """Check if mental health phrases occur with 'positive' """
    (_, start, end) = matches[i]
    span = doc[start:end]

    mh_terms = ["outlet", "attitude", "encourage", "feedback", "reinforcement",
                "outlook", "mood", "mindset", "coping", "cope", "behavior", "reinforce", "esteem", ]
    if F.is_preceded_by(span, ["if"], 5) or F.is_preceded_by(span, ["stay", "staying", "remain", "keep"]) or F.is_followed_by(span, ["about", "experience"]) or F.sentence_contains(span, mh_terms, regex=False):
        matches.pop(i)
        return


def disambiguate_active(matcher, doc, i, matches):
    def in_parens(span):
        doc = span.doc
        start, end = span.start, span.end
        if doc[start - 1].text == "(" and doc[end].text == ")":
            return True
        return False
    (_, start, end) = matches[i]
    span = doc[start:end]
    if in_parens(span):
        matches.pop(i)
        return
    if start > 0:
        for text in ["stay", "physical"]:
            if text in doc[start - 1].lower_:
                matches.pop(i)
                return


def check_no_x_detected(matcher, doc, i, matches):
    """If the modifier 'detected' is preceded by 'no' within a certain window, remove it to avoid a false positive.
    Example: 'No flu, pneumonia, or covid-19 detected.'
    """
    # Get the entire sentence before the span
    (_, start, end) = matches[i]
    span = doc[start:end]
    left_start = start
    while True:
        left_start -= 1
        if left_start < 0:
            break
        if doc[left_start].sent != span.sent:
            break
    left_span = doc[left_start:start]
    if "no" in left_span.text.lower():
        matches.pop(i)


def disambiguate_contact(matcher, doc, i, matches):
    exclude_terms = ["droplet", "precaution", "isolat"]
    (_, start, end) = matches[i]
    span = doc[start:end]
    if F.sentence_contains(span, exclude_terms, regex=True) is True:
        matches.pop(i)
        return


def disambiguate_exposure(matcher, doc, i, matches):
    (_, start, end) = matches[i]
    span = doc[start:end]
    if F.sentence_contains(span, ["tracing", "trace"]):
        matches.pop(i)
        return


def family_speaker(matcher, doc, i, matches):
    (_, start, end) = matches[i]
    span = doc[start:end]
    phrases = ["explained", "told", "informed", "reports", "reported"]
    if span.end != span.sent.end:
        following_end = max(span.end + 2, span.sent.end)
        following_span = doc[span.end: following_end]
        if F.span_contains(following_span, phrases):
            matches.pop(i)
            return
    communication_phrases = ["speak with", "spoke ", "explain", "brought in", "discussed with",
                             "per\b", "decision", "contact", "contacted", "report", "\bcall\b", "telephone", "inform", ]
    # Check if this is the main subject of the sentence, in which case they probably tested positive
    if "nsubj" in span.root.dep_:
        return
    # Otherwise, see if they are preceded by a communication verb from the preceding window up to the beginning of the sentence
    if span.sent.start != span.start:
        precede_start = max(span.sent.start, span.start - 6)
        precede_span = doc[precede_start: span.start]
        if F.span_contains(precede_span, communication_phrases):
            matches.pop(i)
            return


def has_tag(ent, target):
    target = target.lower()
    for token in ent:
        if token._.concept_tag.lower() == target:
            return True
    return False


def has_positive(ent):
    if ent._.is_positive is True or F.is_modified_by_category(ent, "DEFINITE_POSITIVE_EXISTENCE") or has_positive_tag(ent):
        return True
    return False


def get_next_sentence(ent):
    try:
        return ent.doc[ent.sent.end].sent
    except IndexError:
        return None


def next_sentence_contains(ent, target):
    next_sent = get_next_sentence(ent)
    if next_sent is None:
        return False
    return F.span_contains(next_sent, target)


def next_sentence_starts_with(ent, target, max_dist=None, window=1):
    next_sent = get_next_sentence(ent)
    if next_sent is None or (max_dist is not None and next_sent.start - ent.end > max_dist):
        return False
    if not isinstance(target, str):
        target = "|".join(target)
    return re.search(target, next_sent[:window].text, re.IGNORECASE) is not None


def ent_is_sent_start(ent):
    "Returns True if a span contains a token which is a sentence start."
    for token in ent:
        if token.is_sent_start:
            return True
    return False


def get_preceding_span(ent, window):
    if ent.start - window < 0:
        return ent.doc[: ent.start]
    return ent.doc[ent.start - window: ent.start]


def has_positive_tag(ent): return has_tag(ent, "positive")
def set_is_positive(ent, i, *args, value=True): ent._.is_positive = value
def set_is_future(ent, i, *args, value=True): ent._.is_future = value
def set_is_uncertain(ent, i, *args, value=True): ent._.is_future = value
# -----------------------------------------------------------------------------------------------


preprocess_rules = [
    PreprocessingRule(
        "Has the patient been diagnosed with COVID-19\? Y/N",
        desc="Remove template questionnaire (pseudo example)",
    ),
]

concept_tag_rules = {
    # coronavirus, positive, associated_diagnosis, diagnosis, screening, patient, family, timex, other_experiencer
    "coronavirus": [
        TargetRule(
            literal="coronavirus", category="COVID-19",
            pattern=[{"LOWER": {"REGEX": "coronavirus|hcov|ncov$"}}],
        ),
        TargetRule(
            literal="covid", category="COVID-19",
            pattern=[{"LOWER": {"REGEX": "^covid"}}],
        ),
        TargetRule(literal="Novel Coronavirus (COVID-19)",
                   category="COVID-19"),
        TargetRule(literal="novel coronavirus", category="COVID-19"),
        TargetRule(
            literal="[{'LOWER': {'REGEX': '^covid-19'}}]", category="COVID-19",
            pattern=[{"LOWER": {"REGEX": "^covid-19"}}],
        ),
        TargetRule(
            literal="[{'LOWER': 'sars'}, {'LOWER': '-', 'OP': '?'}, {'LOWER': 'cov-2'}]", category="COVID-19",
            pattern=[{"LOWER": "sars"}, {
                "LOWER": "-", "OP": "?"}, {"LOWER": "cov-2"}],
        ),
        TargetRule(literal="2019-cov", category="COVID-19"),
        TargetRule(literal="cov2", category="COVID-19"),
        TargetRule(literal="ncov-19", category="COVID-19"),
        TargetRule(literal="novel coronavirus 2019", category="COVID-19"),
        TargetRule(literal="novel corona", category="COVID-19"),
        TargetRule(literal="covid-10", category="COVID-19"),
        TargetRule(literal="corona 2019", category="COVID-19"),
        TargetRule(literal="coronavirus 19", category="COVID-19"),
        TargetRule(literal="covd-19", category="COVID-19"),
        TargetRule(literal="COVID-19", category="COVID-19"),
        TargetRule(
            literal="COVID- [\s]+19", category="COVID-19",
            pattern=[{"LOWER": "covid-"}, {"IS_SPACE": True,
                                           "OP": "+"}, {"LOWER": {"REGEX": "19"}}, ],
        ),  # covid- [\s]+19
        TargetRule(literal="covd 19", category="COVID-19"),
        TargetRule(literal="covid", category="COVID-19"),
        TargetRule(literal="SARS-CoV-2", category="COVID-19"),
        TargetRule(literal="SARS-CoV2", category="COVID-19"),
        TargetRule(literal="SARS-CoVID-2", category="COVID-19"),
        TargetRule(literal="SARS CoV", category="COVID-19"),
        TargetRule(literal="SARS-CoV-19", category="COVID-19"),
        TargetRule(literal="no-cov", category="COVID-19"),
        TargetRule(
            literal="coivid", category="COVID-19",
            pattern=[{"LOWER": {"REGEX": "^coivid"}}],
        ),
    ],
    "positive": [
        TargetRule("+", "positive", pattern=[{"LOWER": {"REGEX": "\+$"}}]),
        TargetRule("(+)", "positive"),
        TargetRule("+ve", "positive"),
        TargetRule("+ ve", "positive"),
        TargetRule("positive", "positive"),
        TargetRule("active", "positive"),
        TargetRule("confirmed", "positive"),
        TargetRule("results positive", "positive",
                   pattern=[{"LOWER": "results"}, {"LEMMA": "be", "OP": "?"}, {
                       "LOWER": {"IN": ["pos", "positive"]}}, ],
                   ),  # results positive
    ],
    "associated_diagnosis": [
        TargetRule(
            literal="pneumonia", category="associated_diagnosis",
            pattern=[{"LOWER": {"IN": ["pneumonia", "pneum", "pna"]}}],
        ),
        TargetRule(literal="ards", category="associated_diagnosis"),
        TargetRule(
            literal="ards", category="associated_diagnosis",
            pattern=[{"LOWER": "ards"}, {"LOWER": "(", "OP": "?"}, {
                "LOWER": {"REGEX": "[12]/2"}}, {"LOWER": ")", "OP": "?"}, ],
        ),  # ards
        # Taking this for out now as it may be too imprecise
        # TargetRule(literal="infection", category="associated_diagnosis"),
        # TargetRule(literal="illness", category="associated_diagnosis"),
        TargetRule(
            literal="respiratory failure", category="associated_diagnosis",
            pattern=[{"LOWER": {"REGEX": "resp"}}, {"LOWER": "failure"},],
        ),
        TargetRule(
            "respiratory failure 2/2", "associated_diagnosis",
            pattern=[
                {"LOWER": {"IN": ["hypoxemic", "acute", "severe"]}, "OP": "+"},
                {"LOWER": {"REGEX": "resp"}},
                {"LOWER": "failure"},
                {"LOWER": "(", "OP": "?"},
                {"LOWER": {"REGEX": "[12]/2"}},
                {"LOWER": ")", "OP": "?"},
            ],
        ),
        TargetRule("hypoxia", "associated_diagnosis"),
        TargetRule("septic shock", "associated_diagnosis"),
        # TargetRule("sepsis", "associated_diagnosis"),
    ],
    "diagnosis": [
        TargetRule("diagnosis", "diagnosis",
                   pattern=[{"LOWER": {"IN": ["diagnosis", "dx", "dx."]}}, {
                       "LOWER": "of", "OP": "?"}, ],
                   ),
        TargetRule(
            "diagnosed with", "diagnosis",
            pattern=[{"LOWER": {"IN": ["diagnosed", "dx", "dx.", "dx'd"]}}, {
                "LOWER": "with"}, ],
        ),
    ],
    "screening": [
        TargetRule("screen", "screening", pattern=[
                   {"LOWER": {"REGEX": "^screen"}}]),
    ],
    "patient": [
        TargetRule(
            "patient", category="patient", pattern=[{"LOWER": {"IN": ["patient", "pt"]}}],
        ),
        TargetRule(
            "veteran", category="patient", pattern=[{"LOWER": {"IN": ["veteran", "vet"]}}],
        ),
    ],
    # These rules are meant to capture mentions of other family members,
    # Sometimes this will be referring to a family member who tested positive
    "family": [
        TargetRule(
            "family member",
            category="family",
            pattern=[
                {
                    "POS": {"IN": ["NOUN", "PROPN", "PRON"]},
                    "LOWER": {
                        "IN": ["wife", "husband", "spouse", "family", "member", "girlfriend", "boyfriend", "mother", "father", "nephew", "niece", "grandparent", "grandparents", "granddaughter", "grandchild", "grandson", "cousin", "grandmother", "grandfather", "parent", "son", "daughter", "mom", "dad", "brother", "sister", "aunt", "uncle", "child", "children", "sibling", "siblings", "relative", "relatives", "caregiver", ]
                    },
                }
            ],
        )
    ],
    "timex": [
        TargetRule(
            "<NUM> <TIME> <AGO>", category="timex",
            pattern=[{"LIKE_NUM": True}, {"LOWER": {"IN": ["days", "day", "weeks",
                                                           "week", "month", "months"]}}, {"LOWER": {"IN": ["ago", "prior"]}}, ],
        ),
    ],
    # These rules are meant capture mentions of COVID-19 + individuals
    # other than the patient and family members.
    "other_experiencer": [
        TargetRule(
            "other experiencer",
            category="other_experiencer",
            pattern=[
                {
                    "POS": {"IN": ["NOUN", "PROPN", "PRON", "ADJ"]},
                    "LOWER": {
                        "IN": ["someone", "somebody", "person", "anyone", "anybody", "people", "individual", "individuals", "teacher", "anybody", "employees", "employer", "customer", "client", "residents", "resident(s", "pts", "patients", "coworker", "coworkers", "workers", "colleague", "captain", "captains", "pilot", "pilots", "wife", "husband", "spouse", "family", "member", "girlfriend", "boyfriend", "persons", "person(s", "church", "convention", "guest", "party", "attendee", "conference", "roommate", "friend", "friends", "coach", "player", "neighbor", "manager", "boss", "cashier", "landlord", "worked", "works", "nobody", "mate", "mates", "housemate", "housemates", "hotel", "soldier", "airport", "tsa", "lady", "ladies", "lobby", "staffer", "staffers", "staff", "sailor", "sailors", "meeting", ]
                    },
                }
            ],
        ),
        TargetRule(
            "the women", "other_experiencer", pattern=[{"LOWER": {"IN": ["the", "a"]}}, {"LEMMA": "woman"}],
        ),
        TargetRule(
            "the men", "other_experiencer", pattern=[{"LOWER": {"IN": ["the", "a"]}}, {"LEMMA": "man"}],
        ),
        TargetRule("in contact with", "other_experiencer"),
        TargetRule("any one", "other_experiencer"),
        TargetRule("co-worker", "other_experiencer"),
        TargetRule("at work", "other_experiencer"),
        TargetRule(
            "another patient", "other_experiencer",
            pattern=[{"LOWER": "another"}, {
                "LOWER": {"IN": ["pt", "patient", "pt."]}}],
        ),
        TargetRule(
            "a patient", "other_experiencer",
            pattern=[{"LOWER": "a"}, {
                "LOWER": {"IN": ["pt", "patient", "pt."]}}],
        ),
    ],
}


target_rules = {
    # this will add attribute to target, COVID-19, antibody_test, OTHER_CORONAVIRUS, coronavirus screening，
    # IGNORE, OTHER_PERSON
    "COVID-19": [
        TargetRule("<COVID-19>", "COVID-19",
                   pattern=[{"_": {"concept_tag": "COVID-19"}, "OP": "+"}],),
        # These will match more complex constructs
        TargetRule(
            literal="<POSITIVE> <COVID-19>", category="COVID-19",
            pattern=[
                {"_": {"concept_tag": "positive"}, "OP": "+"},
                {"IS_SPACE": True, "OP": "*"},
                {"_": {"concept_tag": "coronavirus"}, "OP": "+"},
            ],
            attributes={"is_positive": True},
        ),
        # "COVID-19 Positive"
        TargetRule(
            literal="<COVID-19> <POSITIVE>", category="COVID-19",
            pattern=[
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"IS_SPACE": True, "OP": "*"},
                {"_": {"concept_tag": "positive"}, "OP": "+"},
            ],
            attributes={"is_positive": True},
        ),
        # If COVID-19 is stated along with a specific diagnosis,
        # such as respiratory distress and pneumonia,
        # we'll count that to be positive
        # "COVID-19 + pneumonia"
        TargetRule(
            "<COVID-19> (<POSITIVE>)? <ASSOCIATED_DIAGNOSIS>", "COVID-19",
            pattern=[
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"IS_SPACE": True, "OP": "*"},
                {"_": {"concept_tag": "positive"}, "OP": "*"},
                {"IS_SPACE": True, "OP": "*"},
                {"_": {"concept_tag": "associated_diagnosis"}, "OP": "+"},
            ],
            attributes={"is_positive": True},
        ),
        # "COVID-19 pneumonia"
        TargetRule(
            "<ASSOCIATED_DIAGNOSIS> <COVID-19>", "COVID-19",
            pattern=[
                {"_": {"concept_tag": "associated_diagnosis"}, "OP": "+"},
                {"IS_SPACE": True, "OP": "*"},
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
            ],
            attributes={"is_positive": True},
        ),
        # "Respiratory Distress with Pneumonia COVID-19"
        TargetRule(
            "<ASSOCIATED_DIAGNOSIS> with <ASSOCIATED_DIAGNOSIS> <COVID-19>", "COVID-19",
            pattern=[
                {"_": {"concept_tag": "associated_diagnosis"}, "OP": "+"},
                {"LOWER": {"IN": ["with", "w", "w/", "from"]}},
                {"_": {"concept_tag": "associated_diagnosis"}, "OP": "*"},
                {"IS_SPACE": True, "OP": "*"},
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
            ],
            attributes={"is_positive": True},
        ),
        # "COVID-19 positive patient"
        TargetRule(
            "<COVID-19> positive <PATIENT>", "COVID-19",
            pattern=[
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"IS_SPACE": True, "OP": "*"},
                {"_": {"concept_tag": "positive"}, "OP": "+"},
                {"_": {"concept_tag": "patient"}, "OP": "+"},
            ],
            attributes={"is_positive": True},
        ),
        # "COVID-19 + precautions"
        TargetRule(
            literal="<COVID-19> <POSITIVE> precautions", category="COVID-19",
            pattern=[
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"IS_SPACE": True, "OP": "*"},
                {"_": {"concept_tag": "positive"}, "OP": "+"},
                {"LOWER": {"REGEX": "^precaution"}},
            ],
            attributes={"is_positive": True},
        ),
        TargetRule(
            literal="coronavirus positive screening", category="positive coronavirus screening",
            pattern=[
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"IS_SPACE": True, "OP": "*"},
                {"_": {"concept_tag": "positive"}, "OP": "+"},
                {"IS_SPACE": True, "OP": "*"},
                {"_": {"concept_tag": "screening"}, "OP": "+"},
            ],
        ),
        TargetRule(
            literal="positive coronavirus screening", category="positive coronavirus screening",
            pattern=[
                {"_": {"concept_tag": "positive"}, "OP": "+"},
                {"IS_SPACE": True, "OP": "*"},
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"IS_SPACE": True, "OP": "*"},
                {"_": {"concept_tag": "screening"}, "OP": "+"},
            ],
        ),
        TargetRule(
            literal="screening coronavirus positive", category="positive coronavirus screening",
            pattern=[
                {"_": {"concept_tag": "screening"}, "OP": "+"},
                {"IS_SPACE": True, "OP": "*"},
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"IS_SPACE": True, "OP": "*"},
                {"_": {"concept_tag": "positive"}, "OP": "+"},
            ],
        ),
        TargetRule(
            literal="screening positive coronavirus", category="positive coronavirus screening",
            pattern=[
                {"_": {"concept_tag": "screening"}, "OP": "+"},
                {"IS_SPACE": True, "OP": "*"},
                {"_": {"concept_tag": "positive"}, "OP": "+"},
                {"IS_SPACE": True, "OP": "*"},
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
            ],
        ),
        # "Pneumonia due to COVID-19"
        TargetRule(
            literal="<ASSOCIATED_DIAGNOSIS> due to covid", category="COVID-19",
            pattern=[
                {"_": {"concept_tag": "associated_diagnosis"}, "OP": "+"},
                {"LOWER": {"IN": ["due", "secondary"]}},
                {"LOWER": "to"},
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
            ],
            attributes={"is_positive": True},
        ),
        TargetRule(
            "<COVID-19> (XXX) DETECTED", "COVID-19",
            pattern=[
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"TEXT": "("},
                {"TEXT": {"NOT_IN": [")"]}, "OP": "+"},
                {"TEXT": ")"},
                {"IS_SPACE": True, "OP": "*"},
                {"TEXT": {"REGEX": "(DETECTED|POSITIVE|^POS$)"}},
            ],
            attributes={"is_positive": True},
        ),
        TargetRule(
            "current covid-19 diagnosis", "COVID-19",
            pattern=[
                {"LOWER": {"IN": ["current", "recent"]}},
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"LOWER": {"IN": ["dx", "dx.", "diagnosis"]}},
            ],
            attributes={"is_positive": True},
        ),
        TargetRule(
            "<COVID-19> evaluation", "COVID-19",
            pattern=[
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"LOWER": {"REGEX": "eval"}},
            ],
            attributes={"is_uncertain": True},
        ),
        TargetRule(
            "<COVID-19> symptoms", "COVID-19",
            pattern=[
                {"_": {"concept_tag": "positive"}, "OP": "*"},
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"LOWER": {"REGEX": "symptom"}},
            ],
            attributes={"is_uncertain": True},
        ),
        TargetRule(
            "<PATIENT> has <COVID-19>", "COVID-19",
            pattern=[
                {"_": {"concept_tag": "patient"}, "OP": "+"},
                {"LEMMA": "do", "OP": "?"},
                {"LEMMA": "have"},
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
            ],
            attributes={"is_positive": True},
        ),
        TargetRule(
            "diagnosis: <COVID>", category="COVID-19",
            pattern=[
                {"LOWER": {"IN": ["diagnosis", "dx"]}},
                {"LOWER": ":"},
                {"IS_SPACE": True, "OP": "*"},
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"IS_SPACE": True, "OP": "*"},
                {"_": {"concept_tag": "positive"}, "OP": "*"},
            ],
            attributes={"is_positive": True},
        ),
        TargetRule(
            "diagnosis: <COVID> testing", category="COVID-19",
            pattern=[
                {"LOWER": {"IN": ["diagnosis", "dx"]}},
                {"LOWER": ":"},
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"LOWER": {"REGEX": "^(test|screen)"}},
            ],
        ),
        TargetRule(
            "diagnosis: <COVID> testing <POSITIVE>", category="COVID-19",
            pattern=[
                {"LOWER": {"IN": ["diagnosis", "dx"]}},
                {"LOWER": ":"},
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"LOWER": {"REGEX": "^(test|screen)"}},
                {"_": {"concept_tag": "positive"}, "OP": "+"},
            ],
            attributes={"is_positive": True},
        ),
        TargetRule(
            "COVID status: positive", "COVID-19",
            pattern=[
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"LOWER": "status"},
                {"LOWER": ":"},
                {"IS_SPACE": True, "OP": "*"},
                {"_": {"concept_tag": "positive"}, "OP": "+"},
            ],
            attributes={"is_positive": True},
        ),
        TargetRule(
            "COVID related admission", "COVID-19",
            pattern=[
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"LOWER": "-", "OP": "?"},
                {"LOWER": "related"},
                {"LOWER": "admission"},
            ],
            attributes={"is_positive": True},
        ),
        TargetRule(
            "admitted due to <COVID-19>", "COVID-19",
            pattern=[
                {"LOWER": "admitted"},
                {"LOWER": "due"},
                {"LOWER": "to"},
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
            ],
            attributes={"is_positive": True},
        ),
        TargetRule(
            "admitted with <COVID-19>", "COVID-19",
            pattern=[
                {"LOWER": "admitted"},
                {"LOWER": {"IN": ["with", "w", "w/"]}},
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
            ],
            attributes={"is_positive": True},
        ),
        TargetRule(
            "COVID related <ASSOCIATED_DIAGNOSIS>", "COVID-19",
            pattern=[
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"LOWER": "-", "OP": "?"},
                {"LOWER": "related"},
                {"_": {"concept_tag": "associated_diagnosis"}, "OP": "+"},
            ],
            attributes={"is_positive": True},
        ),
        TargetRule(
            "<COVID-19> infection", "COVID-19",
            pattern=[
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"IS_SPACE": True, "OP": "*"},
                {"LOWER": "infection"},
            ],
            attributes={"is_positive": True},
        ),
        TargetRule(
            "rule out <COVID-19>", "COVID-19",
            pattern=[
                {"LOWER": "rule"},
                {"LOWER": "out"},
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
            ],
            attributes={"is_uncertain": True},
        ),
        TargetRule(
            "<COVID-19> positive person", "COVID-19",
            pattern=[
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"_": {"concept_tag": "positive"}, "OP": "+"},
                {"_": {"concept_tag": "other_experiencer"}, "OP": "+"},
                # {"LOWER": {"IN": ["person", "persons", "people", "patients"]}}
            ],
            attributes={"is_experienced": False},
        ),
        TargetRule(
            "<COVID-19> <POSITIVE> unit", "COVID-19",
            pattern=[
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"_": {"concept_tag": "positive"}, "OP": "+"},
                {"LOWER": {"IN": ["unit", "floor"]}},
            ],
        ),
        TargetRule(
            "<POSITIVE> <COVID-19> unit", "COVID-19",
            pattern=[
                {"_": {"concept_tag": "positive"}, "OP": "+"},
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"LOWER": {"IN": ["unit", "floor"]}},
            ],
        ),
        TargetRule(
            "active <COVID-19> precautions", "IGNORE",
            pattern=[
                {"LOWER": "active"},
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"LOWER": {"REGEX": "precaution"}},
            ],
        ),
        TargetRule(
            "<POSITIVE> <COVID-19> exposure", "COVID-19",
            pattern=[
                {"_": {"concept_tag": "positive"}, "OP": "+"},
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"LOWER": {"IN": ["exposure", "contact"]}},
            ],
        ),
        TargetRule(
            "known <COVID-19> exposure", "COVID-19",
            pattern=[
                {"LOWER": "known"},
                {"_": {"concept_tag": "positive"}, "OP": "*"},
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"_": {"concept_tag": "positive"}, "OP": "*"},
                {"LOWER": {"IN": ["exposure", "contact"]}},
            ],
        ),
        # If a relevant diagnosis code is in the text,
        # count it as positive
        TargetRule(
            literal="b34.2", category="COVID-19", attributes={"is_positive": True}
        ),
        TargetRule(
            literal="b342", category="COVID-19", attributes={"is_positive": True}
        ),
        TargetRule(
            literal="b97.29", category="COVID-19", attributes={"is_positive": True}
        ),
        TargetRule(
            literal="b97.29", category="COVID-19", attributes={"is_positive": True}
        ),
        TargetRule(
            literal="u07.1", category="COVID-19", attributes={"is_positive": True}
        ),
    ],
    # Extract antibody tests separately from other testing
    "antibody_test": [
        TargetRule(
            "antibody test", "antibody_test",
            pattern=[
                {"LOWER": {"IN": ["antibody", "antibodies", "ab"]}},
                {"LOWER": {"REGEX": "test"}},
            ],
        ),
    ],
    # Non-COVID coronaviruses for disambiguation
    "OTHER_CORONAVIRUS": [
        TargetRule(
            literal="other coronavirus", category="OTHER_CORONAVIRUS",
            pattern=[
                {"LOWER": {"REGEX": "coronavirus|hcovs?|ncovs?|^covs?"}},
                {"TEXT": "-", "OP": "?"},
                {"LOWER": "infection", "OP": "?"},
                {"LOWER": "strain", "OP": "?"},
                {"IS_SPACE": True, "OP": "?"},
                {"LOWER": {
                    "IN": ["229e", "229", "oc43", "oc", "o43", "0c43", "oc-43", "43", "nl63", "hku1", "hkut1", "hkui", "emc", "nl63", "nl65 ", "nl", "63", "hku-1", ]}
                 },
            ],
        ),
        TargetRule(
            literal="other coronavirus", category="OTHER_CORONAVIRUS",
            pattern=[
                {"LOWER": {
                    "IN": ["229e", "229", "oc43", "oc", "o43", "0c43", "oc-43", "43", "nl63", "hku1", "hkut1", "hkui", "emc", "nl63", "nl65 ", "nl", "63", "hku-1", ]}
                 },
                {"LOWER": {"REGEX": "coronavirus|hcovs?|ncovs?|^covs?"}},
            ],
        ),
        TargetRule(
            literal="non-covid coronavirus",
            category="OTHER_CORONAVIRUS",
            pattern=[
                {"LOWER": "non"},
                {"LOWER": "-", "OP": "?"},
                {"LOWER": {"IN": ["novel", "covid", "ncovid", "covid-19"]}},
                {"LOWER": "coronavirus", "OP": "?"},
            ],
        ),
        TargetRule(
            literal="noncovid",
            category="OTHER_CORONAVIRUS",
            pattern=[{"LOWER": {"REGEX": "noncovid"}}],
        ),
    ],
    "coronavirus screening": [
        TargetRule(
            literal="[{'TEXT': '+'}, {'LOWER': 'covid-19'}, {'LOWER': {'REGEX': 'screen'}}]",
            category="coronavirus screening",
            pattern=[
                {"TEXT": "+"},
                {"LOWER": "covid-19"},
                {"LOWER": {"REGEX": "screen"}},
            ],
        ),
        TargetRule(literal=" positive COVID-19 Screening",
                   category="coronavirus screening"),
        TargetRule(literal="COVID-19 Screening",
                   category="coronavirus screening"),
    ],
    # The following rules will extract phrases which may be confused with other concepts.
    # To explicitly exclude them, we'll extract them as "IGNORE", which will then be removed
    # in postprocessing
    "IGNORE": [
        TargetRule(
            literal="coronvirus pandemic", category="IGNORE",
            pattern=[
                {"_": {"concept_tag": "COVID-19"}},
                {"LEMMA": {
                    "IN": ["restriction", "emergency", "epidemic", "outbreak", "crisis", "breakout", "pandemic", "spread", ]}
                 },
            ],
        ),
        TargetRule(
            literal="coronavirus screening", category="IGNORE",
            pattern=[
                {"_": {"concept_tag": "COVID-19"}},
                {"LOWER": {"IN": ["screen", "screening", "screenings"]}},
            ],
        ),
        TargetRule(
            literal="droplet precautions", category="IGNORE",
            pattern=[
                {"LOWER": {"REGEX": "droplet"}},
                {"LOWER": "isolation", "OP": "?"},
                {"LOWER": {"REGEX": "precaution"}},
            ],
        ),
        TargetRule(
            literal="contact precautions", category="IGNORE",
            pattern=[{"LOWER": "contact"}, {"LOWER": {"REGEX": "precaution"}}],
        ),
        TargetRule(
            literal="positive for influenza", category="IGNORE",
            pattern=[
                {"LOWER": "positive"},
                {"LOWER": "for", "OP": "?"},
                {"LOWER": {"IN": ["flu", "influenza"]}},
            ],
        ),
        TargetRule(
            literal="positive patients", category="IGNORE",
            pattern=[
                {"LOWER": "positive"},
                {"LOWER": {"IN": ["people", "patients", "persons"]}},
            ],
        ),
        TargetRule(
            literal="confirm w/", category="IGNORE",
            pattern=[
                {"LEMMA": "confirm"},
                {"LOWER": {"IN": ["with", "w", "w/"]}},
                {"TEXT": "/", "OP": "?"},
            ],
        ),
        TargetRule(
            literal="the positive case", category="IGNORE",
            pattern=[
                {"LOWER": "the"},
                {"LOWER": "positive"},
                {"OP": "?"},
                {"LEMMA": "case"},
            ],
        ),
        TargetRule(literal="positive cases", category="IGNORE"),
        TargetRule(
            literal="results are confirmed", category="IGNORE",
            pattern=[
                {"LOWER": "results"},
                {"LOWER": "are", "OP": "?"},
                {"LOWER": "confirmed"},
            ],
        ),
        TargetRule(
            literal="exposed to <POSITIVE>", category="IGNORE",
            pattern=[
                {"LOWER": "exposed"},
                {"LOWER": "to"},
                {"_": {"concept_tag": "positive"}},
            ],
        ),
        TargetRule(
            literal="negative/positive pressure", category="IGNORE",
            pattern=[{"LOWER": {"REGEX": "^(neg|pos)"}}, {
                "LOWER": "pressure"}],
        ),
        TargetRule(literal="a positive case", category="IGNORE"),
        TargetRule(literal="positive attitude", category="IGNORE"),
        TargetRule(literal="[ ] COVID-19", category="IGNORE"),
        TargetRule(literal="positive feedback", category="IGNORE"),
        TargetRule(
            literal="Has patient been diagnosed with", category="IGNORE",
            pattern=[
                {"LOWER": "has"},
                {"LOWER": "the", "OP": "?"},
                {"LOWER": "patient"},
                {"LOWER": "been"},
                {"LOWER": "diagnosed"},
                {"LOWER": {"IN": ["with", "w", "w/"]}},
            ],
        ),
        TargetRule(literal="people with confirmed covid-19",
                   category="IGNORE"),
        TargetRule(literal="positive serology", category="IGNORE"),
        TargetRule(literal="patients with confirmed covid-19",
                   category="IGNORE"),
        TargetRule(
            literal="covid positive individuals", category="COVID-19",
            pattern=[
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"_": {"concept_tag": "positive"}, "OP": "+"},
                {"LOWER": "tested", "OP": "?"},
                {"_": {"concept_tag": "other_experiencer"}, "OP": "+"},
                # {"LOWER": {"IN": ["individual", "individuals", "contact", "contact", "patients", "pts"]}}
            ],
            attributes={"is_experiencer": False},
        ),
        TargetRule("age 65 +", "IGNORE"),
        TargetRule("age 65+", "IGNORE"),
        TargetRule("return to work", "IGNORE"),
        TargetRule("back to work", "IGNORE"),
        TargetRule(
            "in order to decrease the spread of the COVID-19 infection", "IGNORE"),
        TargetRule("<COVID-19> guidelines", "IGNORE",
                   pattern=[{"_": {"concept_tag": "COVID-19"},
                             "OP": "+"}, {"LOWER": "guidelines"}, ],
                   ),
        TargetRule(
            "<COVID-19> rate", "IGNORE",
            pattern=[
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"LOWER": "infection", "OP": "?"},
                {"LEMMA": "rate"},
            ],
        ),
    ],
    "OTHER_PERSON": [
        TargetRule(
            literal="<COVID-19> <POSITIVE> <PERSON>", category="OTHER_PERSON",
            pattern=[
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"_": {"concept_tag": "positive"}, "OP": "+"},
                {"LOWER": {
                    "IN": ["patients", "persons", "people", "veterans"]}},
            ],
        ),
        TargetRule(
            literal="positive covid individuals", category="COVID-19",
            pattern=[
                {"_": {"concept_tag": "positive"}, "OP": "+"},
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"LOWER": "tested", "OP": "?"},
                {"_": {"concept_tag": "other_experiencer"}, "OP": "+"},
            ],
            attributes={"is_experiencer": False},
        ),
        TargetRule(
            literal="<POSITIVE> <COVID-19> <PERSON>", category="OTHER_PERSON",
            pattern=[
                {"_": {"concept_tag": "positive"}, "OP": "+"},
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"LEMMA": {
                    "IN": ["patients", "persons", "people", "veterans"]}},
            ],
        ),
        TargetRule(
            literal="contact with a <POSITIVE> <COVID-19>", category="OTHER_PERSON",
            pattern=[
                {"LOWER": {"IN": ["contact", "exposure"]}},
                {"LOWER": {"IN": ["with", "to"]}},
                {"OP": "?"},
                {"_": {"concept_tag": "positive"}, "OP": "+"},
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
                {"LEMMA": {"IN": ["patients", "persons",
                                  "people", "veterans", "patient"]}},
            ],
        ),
        TargetRule(
            literal="patient who tested positive for",
            category="OTHER_PERSON",
            pattern=[
                {"LEMMA": {"IN": ["patient", "person", "pt", "pt."]}},
                {"LOWER": {"IN": ["who", "that"]}},
                {"LEMMA": "test"},
                {"LOWER": {"IN": ["positive", "confirmed", "+"]}},
                {"LOWER": "for"},
                {"_": {"concept_tag": "COVID-19"}, "OP": "+"},
            ],
        ),
    ],
}


section_rules = [
    SectionRule(category="labs", literal="Lab results:"),
    SectionRule(category="addendum", literal="ADDENDUM:"),
    SectionRule(category="addendum", literal="Addendum:"),
    SectionRule(category="allergies", literal="ALLERGIC REACTIONS:"),
    SectionRule(category="allergies", literal="ALLERGIES:"),
    SectionRule(category="chief_complaint", literal="CC:"),
    SectionRule(category="chief_complaint", literal="CHIEF COMPLAINT:"),
    SectionRule(category="chief_complaint", literal="Chief Complaint:"),
    SectionRule(category="comments", literal="COMMENTS:"),
    SectionRule(category="diagnoses", literal="ADMISSION DIAGNOSES:"),
    SectionRule(category="diagnoses", literal="DIAGNOSES:"),
    SectionRule(category="diagnoses", literal="Diagnosis:"),
    SectionRule(category="diagnoses", literal="Primary Diagnosis:"),
    SectionRule(category="diagnoses", literal="Primary:"),
    SectionRule(category="diagnoses", literal="SECONDARY DIAGNOSES:"),
    SectionRule(category="diagnoses", literal="Secondary Diagnoses:"),
    SectionRule(category="diagnoses", literal="Secondary Diagnosis:"),
    SectionRule(category="diagnoses", literal="Secondary:"),
    SectionRule(category="family_history", literal="Family History:"),
    SectionRule(category="hospital_course", literal="Brief Hospital Course:"),
    SectionRule(category="hospital_course",
                literal="CONCISE SUMMARY OF HOSPITAL COURSE BY ISSUE/SYSTEM:"),
    SectionRule(category="hospital_course", literal="HOSPITAL COURSE:"),
    SectionRule(category="hospital_course",
                literal="SUMMARY OF HOSPITAL COURSE:"),
    SectionRule(category="imaging", literal="IMAGING:"),
    SectionRule(category="imaging", literal="INTERPRETATION:"),
    SectionRule(category="imaging", literal="Imaging:"),
    SectionRule(category="imaging", literal="MRI:"),
    SectionRule(category="imaging", literal="Radiology:"),
    SectionRule(category="labs_and_studies", literal="ADMISSION LABS:"),
    SectionRule(category="labs_and_studies", literal="Admission Labs:"),
    SectionRule(category="labs_and_studies", literal="Discharge Labs:"),
    SectionRule(category="labs_and_studies", literal="ECHO:"),
    SectionRule(category="labs_and_studies", literal="FINDINGS:"),
    SectionRule(category="labs_and_studies", literal="Findings:"),
    SectionRule(category="labs_and_studies", literal="INDICATION:"),
    SectionRule(category="labs_and_studies", literal="LABS:"),
    SectionRule(category="labs_and_studies", literal="Labs:"),
    SectionRule(category="labs_and_studies", literal="MICRO:"),
    SectionRule(category="labs_and_studies", literal="Micro:"),
    SectionRule(category="labs_and_studies", literal="Microbiology:"),
    SectionRule(category="labs_and_studies", literal="Pertinent Results:"),
    SectionRule(category="labs_and_studies", literal="STUDIES:"),
    SectionRule(category="labs_and_studies", literal="Studies:"),
    SectionRule(category="medications", literal="ACTIVE MEDICATIONS LIST:"),
    SectionRule(category="medications", literal="ACTIVE MEDICATIONS:"),
    SectionRule(category="medications", literal="ADMISSION MEDICATIONS:"),
    SectionRule(category="medications", literal="CURRENT MEDICATIONS:"),
    SectionRule(category="medications", literal="DISCHARGE MEDICATIONS:"),
    SectionRule(category="medications", literal="Discharge Medications:"),
    SectionRule(category="medications", literal="HOME MEDICATIONS:"),
    SectionRule(category="medications", literal="MEDICATIONS AT HOME:"),
    SectionRule(category="medications", literal="MEDICATIONS LIST:"),
    SectionRule(category="medications", literal="MEDICATIONS ON ADMISSION:"),
    SectionRule(category="medications", literal="MEDICATIONS ON DISCHARGE:"),
    SectionRule(category="medications", literal="MEDICATIONS ON TRANSFER:"),
    SectionRule(category="medications",
                literal="MEDICATIONS PRIOR TO ADMISSION:"),
    SectionRule(category="medications", literal="MEDICATIONS:"),
    SectionRule(category="medications", literal="MEDICATIONS:"),
    SectionRule(category="neurological", literal="Neuro:"),
    SectionRule(category="observation_and_plan", literal="A/P:"),
    SectionRule(category="observation_and_plan", literal="ASSESSMENT/PLAN:"),
    SectionRule(category="observation_and_plan", literal="ASSESSMENT:"),
    SectionRule(category="observation_and_plan", literal="Assessment/Plan:"),
    SectionRule(category="observation_and_plan",
                literal="Clinical Impression:"),
    SectionRule(category="observation_and_plan",
                literal="DISCHARGE DIAGNOSES:"),
    SectionRule(category="observation_and_plan",
                literal="DISCHARGE DIAGNOSIS:"),
    SectionRule(category="observation_and_plan",
                literal="Discharge Condition:"),
    SectionRule(category="observation_and_plan",
                literal="Discharge Diagnoses:"),
    SectionRule(category="observation_and_plan",
                literal="Discharge Diagnosis:"),
    SectionRule(category="observation_and_plan",
                literal="Discharge Disposition:"),
    SectionRule(category="observation_and_plan", literal="FINAL DIAGNOSES:"),
    SectionRule(category="observation_and_plan", literal="FINAL DIAGNOSIS:"),
    SectionRule(category="observation_and_plan", literal="IMPRESSION:"),
    SectionRule(category="observation_and_plan",
                literal="Impression and Plan:"),
    SectionRule(category="observation_and_plan",
                literal="Impression and Recommendation:"),
    SectionRule(category="other", literal="Facility:"),
    SectionRule(category="other", literal="Service:"),
    SectionRule(category="past_medical_history",
                literal="Current Medical Problems:"),
    SectionRule(category="past_medical_history",
                literal="History of Chronic Illness:"),
    SectionRule(category="past_medical_history", literal="MHx:"),
    SectionRule(category="past_medical_history", literal="PAST HISTORY:"),
    SectionRule(category="past_medical_history",
                literal="PAST MEDICAL HISTORY:"),
    SectionRule(category="past_medical_history", literal="PAST MEDICAL Hx:"),
    SectionRule(category="past_medical_history",
                literal="PAST SURGICAL HISTORY:"),
    SectionRule(category="past_medical_history", literal="PMH:"),
    SectionRule(category="past_medical_history", literal="PMHx:"),
    SectionRule(category="past_medical_history",
                literal="Past Medical History:"),
    SectionRule(category="past_medical_history",
                literal="UNDERLYING MEDICAL CONDITION:"),
    SectionRule(category="patient_education", literal="Education:"),
    SectionRule(category="patient_education", literal="Patient Education:"),
    SectionRule(category="patient_instructions",
                literal="DISCHARGE INSTRUCTIONS/FOLLOWUP:"),
    SectionRule(category="patient_instructions",
                literal="DISCHARGE INSTRUCTIONS:"),
    SectionRule(category="patient_instructions",
                literal="Discharge Instructions:"),
    SectionRule(category="patient_instructions",
                literal="Followup Instructions:"),
    SectionRule(category="physical_exam", literal="PE:"),
    SectionRule(category="physical_exam", literal="PHYSICAL EXAM:"),
    SectionRule(category="physical_exam", literal="PHYSICAL EXAMINATION:"),
    SectionRule(category="physical_exam", literal="Physical Exam:"),
    SectionRule(category="problem_list", literal="Active Problem List:"),
    SectionRule(category="problem_list", literal="Current Problems:"),
    SectionRule(category="problem_list", literal="Medical Problems:"),
    SectionRule(category="problem_list", literal="PROBLEM LIST:"),
    SectionRule(category="problem_list", literal="Problem List:"),
    SectionRule(category="reason_for_examination",
                literal="REASON FOR THIS EXAMINATION:"),
    SectionRule(category="signature", literal="Electronic Signature:"),
    SectionRule(category="signature", literal="Signed electronically by:"),
    SectionRule(category="social_history", literal="PMHSx:"),
    SectionRule(category="social_history", literal="PSH:"),
    SectionRule(category="social_history", literal="SH:"),
    SectionRule(category="social_history", literal="Sexual History:"),
    SectionRule(category="social_history", literal="Social History:"),
]

context_rules = [
    # =============="NEGATED_EXISTENCE" will be used to negate entities=========================
    ConTextRule(  # ie., "COVID-19 not detected"
        literal="Not Detected", category="NEGATED_EXISTENCE", direction="BACKWARD",
        pattern=[
            {"LOWER": {"IN": ["not", "non"]}},
            {"IS_SPACE": True, "OP": "*"},
            {"TEXT": "-", "OP": "?"},
            {"LOWER": {"REGEX": "detecte?d"}},
        ],
        # Limit to 1 since this phrase occurs in tabular data like:
        # "CORONAVIUS 229E Not Detected CORONAVIRUS HKU1 Detected"
        # max_scope=3, # Set a small window, but allow for whitespaces
        max_targets=1, allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextRule(": negative", "NEGATED_EXISTENCE", direction="BACKWARD",
                max_targets=1, max_scope=3,),  # Set a small window, but allow for whitespaces
    ConTextRule("not been detected", "NEGATED_EXISTENCE",
                direction="BACKWARD"),
    ConTextRule("none detected", "NEGATED_EXISTENCE", direction="BACKWARD"),
    ConTextRule("free from", "NEGATED_EXISTENCE", direction="FORWARD"),
    ConTextRule("not tested", "NEGATED_EXISTENCE", direction="BACKWARD", pattern=[
                {"LOWER": "not"}, {"LOWER": "been", "OP": "?"}, {"LOWER": "tested"}],),
    ConTextRule("Ref Not Detected", "IGNORE", direction="TERMINATE", pattern=[{"LOWER": "ref"}, {"LOWER": ":"}, {
                "LOWER": "not"}, {"LOWER": "detected"}, ], max_targets=1, allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},),
    ConTextRule("not indicated", "NEGATED_EXISTENCE",
                direction="BACKWARD", max_scope=5),
    ConTextRule("NEGATIVE NEG", "NEGATED_EXISTENCE", direction="BACKWARD",  # Lab results
                pattern=[{"TEXT": "NEGATIVE"}, {
                    "IS_SPACE": True, "OP": "*"}, {"TEXT": "NEG"}],
                max_scope=1, allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},),
    ConTextRule("negative screen", "NEGATED_EXISTENCE",
                direction="BIDIRECTIONAL", max_scope=2,),
    ConTextRule("negative test", "NEGATED_EXISTENCE",
                direction="BIDIRECTIONAL", max_scope=4),
    ConTextRule("without any", "NEGATED_EXISTENCE",
                direction="FORWARD", max_scope=2),
    ConTextRule("denies", "NEGATED_EXISTENCE",
                direction="FORWARD", max_scope=10),
    ConTextRule("denies any", "NEGATED_EXISTENCE",
                direction="FORWARD", max_scope=10),
    ConTextRule("denies travel", "NEGATED_EXISTENCE",
                direction="FORWARD", max_scope=10),
    ConTextRule("denied", "NEGATED_EXISTENCE",
                direction="FORWARD", max_scope=10),
    ConTextRule("no evidence", "NEGATED_EXISTENCE", direction="FORWARD"),
    ConTextRule("history of", "NEGATED_EXISTENCE", direction="FORWARD", max_scope=4, pattern=[
                {"LOWER": "no"}, {"LOWER": {"IN": ["hx", "-hx", "history"]}}, {"LOWER": "of"}, ],),
    ConTextRule("no diagnosis of", "NEGATED_EXISTENCE", direction="FORWARD", pattern=[{"LOWER": "no"}, {
                "OP": "?"}, {"LOWER": {"IN": ["dx", "diagnosis"]}}, {"LOWER": "of", "OP": "?"}, ],),
    ConTextRule("no", "NEGATED_EXISTENCE", direction="FORWARD",
                max_scope=2),  # Limit to a small scope
    ConTextRule("no positive", "NEGATED_EXISTENCE", direction="FORWARD"),
    ConTextRule("no one", "NEGATED_EXISTENCE", direction="FORWARD"),
    ConTextRule("no residents", "NEGATED_EXISTENCE", direction="FORWARD"),
    ConTextRule("no confirmed cases", "NEGATED_EXISTENCE", direction="BIDIRECTIONAL", pattern=[
                {"LOWER": "no"}, {"LOWER": "confirmed"}, {"LEMMA": "case"}],),
    ConTextRule("not been confirmed", "NEGATED_EXISTENCE", direction="FORWARD", max_scope=2, pattern=[
                {"LOWER": {"IN": ["not", "n't"]}}, {"LOWER": "been", "OP": "?"}, {"LOWER": "confirmed"}, ],),
    ConTextRule("no known", "NEGATED_EXISTENCE",
                direction="FORWARD", max_scope=5),
    ConTextRule("no contact with", "NEGATED_EXISTENCE", direction="FORWARD", max_scope=None, pattern=[
                {"LOWER": "no"}, {"OP": "?"}, {"LOWER": "contact"}, {"LOWER": {"REGEX": "w/?(ith)?$"}, "OP": "?"}, ],),
    # "Veteran answered no to being exposed to coronavirus"
    ConTextRule("answer no", "NEGATED_EXISTENCE", direction="BIDIRECTIONAL", pattern=[{"LOWER": {"REGEX": "^answer"}}, {
                "TEXT": '"', "OP": "?"}, {"LOWER": {"IN": ["no", "negative", "neg"]}}, {"TEXT": '"', "OP": "?"}, ],),
    ConTextRule("negative", "NEGATED_EXISTENCE", direction="BIDIRECTIONAL",),
    ConTextRule("negative for", "NEGATED_EXISTENCE", direction="FORWARD", pattern=[
                {"LOWER": {"IN": ["negative", "neg"]}}, {"LOWER": "for"}],),
    # ConTextRule("is negative for", "NEGATED_EXISTENCE", direction="FORWARD"),
    ConTextRule("not positive", "NEGATED_EXISTENCE",
                direction="BIDIRECTIONAL"),
    ConTextRule("excluded", "NEGATED_EXISTENCE",
                direction="BIDIRECTIONAL", max_scope=4),
    ConTextRule("negative screening for", "NEGATED_EXISTENCE", direction="FORWARD", pattern=[
                {"LOWER": "negative"}, {"LOWER": {"REGEX": "screen"}}, {"LOWER": "for", "OP": "?"}, ],),
    ConTextRule("screening negative", "NEGATED_EXISTENCE", direction="BACKWARD", pattern=[
                {"LOWER": {"REGEX": "^screen"}}, {"LOWER": {"REGEX": "^neg"}}],),
    ConTextRule("screened negative for", "NEGATED_EXISTENCE", direction="FORWARD", pattern=[
                {"LOWER": {"REGEX": "^screen"}}, {"LOWER": {"REGEX": "^neg"}}, {"LOWER": "for"}, ],),
    ConTextRule("does not screen positive", "NEGATED_EXISTENCE"),
    ConTextRule("is negative", "NEGATED_EXISTENCE", direction="BIDIRECTIONAL", pattern=[
                {"LEMMA": "be"}, {"LOWER": "negative"}],),
    ConTextRule("not test positive", "NEGATED_EXISTENCE",
                direction="BIDIRECTIONAL"),
    ConTextRule("no screening for", "NEGATED_EXISTENCE", direction="FORWARD", pattern=[
                {"LOWER": {"REGEX": "not?"}}, {"LOWER": {"REGEX": "^screen"}}, {"LOWER": "for", "OP": "?"}, ],),
    ConTextRule("no signs of", "NEGATED_EXISTENCE", direction="FORWARD"),
    ConTextRule("no symptoms", "NEGATED_EXISTENCE", direction="FORWARD", pattern=[
                {"LOWER": "no"}, {"LOWER": {"REGEX": "(sign|symptom)"}}],),
    ConTextRule("no testing for", "NEGATED_EXISTENCE", direction="FORWARD", pattern=[
                {"LOWER": {"REGEX": "^no"}}, {"LOWER": {"REGEX": "^test"}}, {"LOWER": "for"}, ],),
    ConTextRule("no indication of", "NEGATED_EXISTENCE", direction="FORWARD", pattern=[{"LOWER": "no"}, {
                "LOWER": {"REGEX": "indication"}}, {"LOWER": {"IN": ["of", "for"]}, "OP": "?"}, ],),
    ConTextRule("no exposure", "NEGATED_EXISTENCE", direction="FORWARD", pattern=[
                {"LOWER": "no"}, {"LOWER": {"REGEX": "^exposure"}}],),
    ConTextRule("without signs/symptoms", "NEGATED_EXISTENCE", direction="FORWARD", pattern=[{"LOWER": "without"}, {"OP": "?"}, {
                "LOWER": {"IN": ["signs", "symptoms"]}}, {"LOWER": "or", "OP": "?"}, {"LOWER": {"IN": ["signs", "symptoms"]}, "OP": "?"}, ],),
    ConTextRule("w/o signs/symptoms", "NEGATED_EXISTENCE", direction="FORWARD", pattern=[{"LOWER": "w/o"}, {"OP": "?"}, {
                "LOWER": {"IN": ["signs", "symptoms"]}}, {"LOWER": "or", "OP": "?"}, {"LOWER": {"IN": ["signs", "symptoms"]}, "OP": "?"}, ],),
    ConTextRule("does not have any signs/symptoms", "NEGATED_EXISTENCE", direction="FORWARD", allowed_types={"COVID-19"}, pattern=[{"LOWER": "does"}, {
                "LOWER": {"IN": ["not", "n't"]}}, {"LOWER": "have"}, {"LOWER": "any", "OP": "?"}, {"LOWER": {"IN": ["signs", "symptoms", "ss", "s/s"]}}, ],),
    ConTextRule("not have", "NEGATED_EXISTENCE", max_scope=5),
    ConTextRule("not have a <POSITIVE>? diagnosis", "NEGATED_EXISTENCE", pattern=[{"LOWER": {"IN": ["not", "n't"]}}, {"LOWER": "have"}, {
                "LOWER": "a"}, {"_": {"concept_tag": "positive"}, "OP": "*"}, {"_": {"concept_tag": "diagnosis"}, "OP": "+"}, ],),
    ConTextRule("no evidence of", "NEGATED_EXISTENCE", direction="FORWARD"),
    ConTextRule("does not meet criteria", "NEGATED_EXISTENCE",
                direction="BIDIRECTIONAL"),
    ConTextRule("no concern for", "NEGATED_EXISTENCE", direction="FORWARD", pattern=[{"LOWER": "no"}, {
                "LOWER": "concern"}, {"LOWER": {"IN": ["for", "of"]}}, ], allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},),
    ConTextRule("not at risk", "NEGATED_EXISTENCE", direction="FORWARD", pattern=[{"LOWER": "not"}, {
                "LOWER": "at"}, {"LOWER": "risk"}], allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},),
    ConTextRule("no risk", "NEGATED_EXISTENCE", direction="FORWARD", pattern=[{"LOWER": "no"}, {
                "OP": "?"}, {"LOWER": "risk"}], allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},),
    ConTextRule("no suspicion", "NEGATED_EXISTENCE", direction="FORWARD", pattern=[
                {"LOWER": "no"}, {"LOWER": {"REGEX": "^suspicion"}}, {"LOWER": "for", "OP": "?"}, ],),
    ConTextRule("not suspect", "NEGATED_EXISTENCE", direction="FORWARD"),
    ConTextRule("not", "NEGATED_EXISTENCE", direction="FORWARD", max_scope=4),
    ConTextRule("ruled out for", "NEGATED_EXISTENCE", direction="FORWARD",
                allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},),
    ConTextRule("is ruled out", "NEGATED_EXISTENCE", direction="BACKWARD", allowed_types={"COVID-19", "OTHER_CORONAVIRUS"}, pattern=[
                {"LOWER": {"IN": ["is", "are", "were"]}}, {"OP": "?", "POS": "ADV"}, {"LOWER": "ruled"}, {"LOWER": "out"}, ],),
    ConTextRule("does not meet criteria", "NEGATED_EXISTENCE",
                direction="FORWARD", allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},),
    ConTextRule("is not likely", "NEGATED_EXISTENCE", direction="BACKWARD", pattern=[
                {"LOWER": {"IN": ["is", "are"]}}, {"LOWER": "not"}, {"LOWER": "likely"}, ],),
    ConTextRule("no travel", "NEGATED_EXISTENCE", direction="FORWARD", pattern=[
                {"LOWER": "no"}, {"LOWER": "recent", "OP": "?"}, {"LOWER": "travel"}],),
    ConTextRule("not be in", "NEGATED_EXISTENCE", direction="FORWARD",
                allowed_types={"location", "COVID-19"},),
    ConTextRule("cleared from", "NEGATED_EXISTENCE", direction="FORWARD", pattern=[
                {"LOWER": {"REGEX": "^clear"}}, {"LOWER": {"IN": ["of", "for", "from"]}}, ],),
    ConTextRule("no history of travel", "NEGATED_EXISTENCE", direction="FORWARD", pattern=[{"LOWER": "no"}, {"LOWER": {
                "IN": ["hx", "history"]}}, {"LOWER": "of", "OP": "?"}, {"LOWER": "travel"}, ], allowed_types={"location", "COVID-19"},),
    ConTextRule("no exposure to", "NEGATED_EXISTENCE", direction="BIDIRECTIONAL", pattern=[{"LOWER": "no"}, {
                "OP": "?"}, {"LOWER": "exposure"}, {"LOWER": "to"}], allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},),
    ConTextRule("no contact with", "NEGATED_EXISTENCE", direction="BIDIRECTIONAL", pattern=[{"LOWER": "no"}, {
                "OP": "?"}, {"LEMMA": "contact"}, {"LOWER": "with"}], allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},),
    ConTextRule("not have contact with", "NEGATED_EXISTENCE", direction="BIDIRECTIONAL", pattern=[{"LOWER": "not"}, {
                "LOWER": "have"}, {"OP": "?"}, {"LOWER": "contact"}, {"LOWER": "with"}, ], allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},),
    ConTextRule("no X contacts", "NEGATED_EXISTENCE", direction="FORWARD", pattern=[{"LOWER": {"IN": ["no", "any"]}}, {
                "LOWER": "known", "OP": "?"}, {"OP": "?"}, {"LEMMA": "contact"}, {"LOWER": "with", "OP": "?"}, ],),
    ConTextRule("anyone with", "NEGATED_EXISTENCE",
                direction="FORWARD", max_scope=None),
    ConTextRule("no symptoms of", "NEGATED_EXISTENCE",
                direction="FORWARD", allowed_types={"COVID-19"},),
    ConTextRule("no risk factors", "NEGATED_EXISTENCE",
                direction="FORWARD", allowed_types={"COVID-19"},),
    ConTextRule("no confirmed cases", "NEGATED_EXISTENCE",
                direction="FORWARD", allowed_types={"COVID-19"},),
    ConTextRule("does not meet screening criteria", "NEGATED_EXISTENCE", direction="FORWARD", pattern=[{"LOWER": "does"}, {"LOWER": {"IN": ["not", "n't"]}}, {
                "LOWER": "meet"}, {"LOWER": "screening", "OP": "?"}, {"LOWER": "criteria", "OP": "?"}, {"LOWER": "for", "OP": "?"}, ], allowed_types={"COVID-19"},),
    ConTextRule(": no", "NEGATED_EXISTENCE",
                direction="BACKWARD", max_scope=4),
    ConTextRule("no report", "NEGATED_EXISTENCE", direction="FORWARD", pattern=[
                {"LOWER": "no"}, {"LOWER": {"REGEX": "report"}}],),
    ConTextRule("not diagnosed with", "NEGATED_EXISTENCE", direction="FORWARD", max_scope=2, pattern=[
                {"LOWER": {"IN": ["not", "never"]}}, {"OP": "?"}, {"LOWER": "diagnosed"}, {"LOWER": "with"}, ],),
    ConTextRule("not been tested or diagnosed with",
                "NEGATED_EXISTENCE", direction="FORWARD", max_scope=2,),
    ConTextRule("not been tested for or diagnosed with",
                "NEGATED_EXISTENCE", direction="FORWARD", max_scope=2,),
    ConTextRule("not tested positive for", "NEGATED_EXISTENCE", direction="BIDIRECTIONAL", pattern=[{"LOWER": "not"}, {
                "LOWER": {"REGEX": "^test"}}, {"_": {"concept_tag": "positive"}, "OP": "+"}, {"LOWER": "for", "OP": "?"}, ],),
    ConTextRule("not tested", "NEGATED_EXISTENCE", direction="FORWARD",),
    ConTextRule("not tested or diagnosed",
                "NEGATED_EXISTENCE", direction="FORWARD",),


    # =============="DEFINITE_POSITIVE_EXISTENCE" will be used to set is_positive to True=======
    ConTextRule("confirmed", "DEFINITE_POSITIVE_EXISTENCE", direction="BIDIRECTIONAL",
                # Too ambiguous of a word, needs to be very close
                on_match=disambiguate_confirmed, max_scope=2,
                ),
    ConTextRule("known", "DEFINITE_POSITIVE_EXISTENCE",
                direction="FORWARD", max_scope=2),
    ConTextRule("positive for", "DEFINITE_POSITIVE_EXISTENCE", direction="FORWARD", pattern=[
                {"LOWER": {"IN": ["pos", "positive", "+"]}}, {"LOWER": "for"}],),
    ConTextRule("positive", "DEFINITE_POSITIVE_EXISTENCE",
                direction="BIDIRECTIONAL", on_match=disambiguate_positive,),
    ConTextRule("pos status", "DEFINITE_POSITIVE_EXISTENCE",
                direction="BACKWARD", max_scope=3),
    ConTextRule("results are positive", "DEFINITE_POSITIVE_EXISTENCE", direction="BACKWARD", max_scope=3, pattern=[
                {"LOWER": {"REGEX": "result"}}, {"LOWER": {"IN": ["is", "are"]}}, {"LOWER": "positive"}, ],),
    ConTextRule("pos", "DEFINITE_POSITIVE_EXISTENCE",
                direction="BIDIRECTIONAL", max_scope=5),
    ConTextRule("results pos", "DEFINITE_POSITIVE_EXISTENCE",
                direction="BIDIRECTIONAL", max_scope=5),
    ConTextRule("positivity", "DEFINITE_POSITIVE_EXISTENCE",
                direction="BACKWARD"),
    ConTextRule("test +", "DEFINITE_POSITIVE_EXISTENCE", direction="BIDIRECTIONAL", pattern=[
                {"LOWER": {"REGEX": "^test"}}, {"LOWER": {"IN": ["positive", "pos", "+", "(+)"]}}, ],),
    ConTextRule("+ve", "DEFINITE_POSITIVE_EXISTENCE",
                direction="BIDIRECTIONAL",),
    ConTextRule("(+)", "DEFINITE_POSITIVE_EXISTENCE", direction="BIDIRECTIONAL", pattern=[{"TEXT": {
                "IN": ["(+)", "+"]}}], max_scope=1, allowed_types={"COVID-19", "OTHER_CORONAVIRUS", "sign/symptom"},),
    ConTextRule("(+)", "DEFINITE_POSITIVE_EXISTENCE", direction="FORWARD", pattern=[{"TEXT": {"IN": [
                "(+)", "+"]}}, {"LOWER": "for"}], max_scope=1, allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},),
    ConTextRule("test remains positive", "DEFINITE_POSITIVE_EXISTENCE", direction="BACKWARD", pattern=[
                {"LOWER": {"IN": ["test", "pcr"]}}, {"LOWER": "remains"}, {"LOWER": {"IN": ["pos", "positive", "+", "(+)"]}}, ],),
    ConTextRule("notified of positive results", "DEFINITE_POSITIVE_EXISTENCE", direction="BIDIRECTIONAL", pattern=[{"LOWER": {"REGEX": "notif(y|ied)"}}, {
                "OP": "?"}, {"LOWER": "of"}, {"_": {"concept_tag": "positive"}, "OP": "+"}, {"LOWER": {"REGEX": "results?|test(ing)?|status"}}, ],),
    ConTextRule("notified the veteran of positive results", "DEFINITE_POSITIVE_EXISTENCE", direction="BIDIRECTIONAL", pattern=[{"LOWER": {"REGEX": "notif(y|ied)"}}, {"LOWER": "the", "OP": "?"}, {
                "LOWER": {"IN": ["veteran", "patient", "family"]}}, {"LOWER": "of"}, {"_": {"concept_tag": "positive"}, "OP": "+"}, {"LOWER": {"REGEX": "results?|test(ing)?|status"}}, ],),
    ConTextRule("likely secondary to", "DEFINITE_POSITIVE_EXISTENCE",
                direction="FORWARD", max_scope=1,),
    ConTextRule("Problem:", "DEFINITE_POSITIVE_EXISTENCE",
                direction="FORWARD", max_scope=10),
    ConTextRule("PROBLEM LIST:", "DEFINITE_POSITIVE_EXISTENCE",
                direction="FORWARD", max_scope=10),
    ConTextRule("current problems:", "DEFINITE_POSITIVE_EXISTENCE", direction="FORWARD", max_scope=10), ConTextRule(
        "Problem List of", "DEFINITE_POSITIVE_EXISTENCE", direction="FORWARD", max_scope=10),
    ConTextRule("active problems:", "DEFINITE_POSITIVE_EXISTENCE",
                direction="FORWARD", max_scope=10),
    ConTextRule("acute problems", "DEFINITE_POSITIVE_EXISTENCE",
                direction="FORWARD", max_scope=10),
    ConTextRule("admission diagnosis:", "DEFINITE_POSITIVE_EXISTENCE", direction="FORWARD", pattern=[{"LOWER": {
                "REGEX": "admi(t|ssion)"}}, {"LOWER": {"IN": ["diagnosis", "dx", "dx."]}}, {"LOWER": ":", "OP": "?"}, ],),
    ConTextRule("Reason for admission:", "DEFINITE_POSITIVE_EXISTENCE",
                direction="FORWARD", max_scope=4,),
    ConTextRule("treatment of", "DEFINITE_POSITIVE_EXISTENCE", direction="FORWARD", max_scope=4), ConTextRule("Admitting Diagnosis:", "DEFINITE_POSITIVE_EXISTENCE",
                                                                                                              direction="FORWARD", max_scope=4, pattern=[{"LOWER": "admitting", "OP": "?"}, {"LOWER": {"IN": ["diagnosis", "dx", "dx."]}}, ],),
    ConTextRule("dx:", "DEFINITE_POSITIVE_EXISTENCE",
                direction="FORWARD", max_scope=4,),
    ConTextRule("diagnosed <DATE>", "DEFINITE_POSITIVE_EXISTENCE", direction="BACKWARD", max_scope=4, pattern=[
                {"LOWER": {"REGEX": "(diagnos|dx)(ed)?"}}, {"LOWER": {"REGEX": "[\d]{1,2}/[\d]{1,2}"}}, ],),
    ConTextRule("diagnosed with", "DEFINITE_POSITIVE_EXISTENCE",
                direction="FORWARD", max_scope=6,),
    ConTextRule("found to be positive", "DEFINITE_POSITIVE_EXISTENCE",
                direction="BACKWARD", max_scope=6,),
    ConTextRule("found to be positive for",
                "DEFINITE_POSITIVE_EXISTENCE", direction="FORWARD", max_scope=6,),
    ConTextRule("+ test", "DEFINITE_POSITIVE_EXISTENCE",),
    ConTextRule("management of", "DEFINITE_POSITIVE_EXISTENCE",
                direction="FORWARD", max_scope=3),
    ConTextRule("history of travel", "DEFINITE_POSITIVE_EXISTENCE", direction="FORWARD", pattern=[{"LOWER": {
                "IN": ["hx", "-hx", "history"]}}, {"LOWER": "of"}, {"LOWER": "travel"}, ], allowed_types={"location"},),
    ConTextRule("presumed positive", "DEFINITE_POSITIVE_EXISTENCE", direction="BIDIRECTIONAL", pattern=[
                {"LOWER": {"REGEX": "^presum"}}, {"LOWER": {"IN": ["pos", "positive", "+"]}, "OP": "?"}, ],),
    ConTextRule("ARDS from", "DEFINITE_POSITIVE_EXISTENCE", direction="FORWARD", pattern=[{"LOWER": "ards"}, {
                "LOWER": {"IN": ["from", "with"]}, "OP": "?"}], allowed_types={"COVID-19"}, max_scope=3,),
    ConTextRule("ARDS secondary to", "DEFINITE_POSITIVE_EXISTENCE", direction="FORWARD", pattern=[
                {"LOWER": "ards"}, {"LOWER": "secondary"}, {"LOWER": "to"}], allowed_types={"COVID-19"}, max_scope=3,),
    ConTextRule("acute respiratory distress",
                "DEFINITE_POSITIVE_EXISTENCE", direction="FORWARD", max_scope=3,),
    ConTextRule("post-extubation", "DEFINITE_POSITIVE_EXISTENCE",
                direction="FORWARD", max_scope=3),
    ConTextRule("in the setting of", "DEFINITE_POSITIVE_EXISTENCE", direction="FORWARD", allowed_types={
                "COVID-19"}, max_scope=6, pattern=[{"LOWER": "in"}, {"LOWER": "the", "OP": "?"}, {"LOWER": "setting"}, {"LOWER": "of"}, ],),
    ConTextRule("in the s/o", "DEFINITE_POSITIVE_EXISTENCE",
                direction="FORWARD", allowed_types={"COVID-19"}, max_scope=6,),
    ConTextRule("found to have", "DEFINITE_POSITIVE_EXISTENCE",
                direction="FORWARD", allowed_types={"COVID-19"}, max_scope=6,),
    ConTextRule("presents with", "DEFINITE_POSITIVE_EXISTENCE", direction="FORWARD", allowed_types={
                "COVID-19"}, max_scope=6, pattern=[{"LOWER": {"REGEX": "^present"}, "POS": "VERB"}, {"LOWER": "with"}],),NEGATION
    ConTextRule("respiratory failure", "DEFINITE_POSITIVE_EXISTENCE", direction="FORWARD", pattern=[{"LOWER": {"REGEX": "resp"}}, {
                "LOWER": "failure"}, {"LOWER": {"IN": ["with", "due"]}, "OP": "?"}, {"LOWER": "to", "OP": "?"}, ], max_scope=4,),
    ConTextRule("respiratory failure 2/2", "DEFINITE_POSITIVE_EXISTENCE", direction="FORWARD", pattern=[{"LOWER": {"REGEX": "resp"}}, {
                "LOWER": "failure"}, {"LOWER": "(", "OP": "?"}, {"LOWER": {"REGEX": "[12]/2"}}, {"LOWER": ")", "OP": "?"}, ], max_scope=4,),
    ConTextRule("active for", "DEFINITE_POSITIVE_EXISTENCE", direction="FORWARD", pattern=[{"LOWER": "active"}, {
                "LOWER": "for", "OP": "?"}], allowed_types={"COVID-19"}, max_scope=2, on_match=disambiguate_active,),
    ConTextRule("resolving", "DEFINITE_POSITIVE_EXISTENCE",
                direction="BACKWARD", max_scope=2),
    ConTextRule("recovering from", "DEFINITE_POSITIVE_EXISTENCE", direction="FORWARD", pattern=[
                {"LOWER": {"IN": ["recovery", "recovering"]}}, {"LOWER": "from"}], max_scope=2,),
    ConTextRule("not recovered", "DEFINITE_POSITIVE_EXISTENCE", direction="FORWARD", pattern=[
                {"LOWER": "not"}, {"LOWER": "yet", "OP": "?"}, {"LOWER": {"REGEX": "^recover"}}, ],),
    ConTextRule("Detected", "DEFINITE_POSITIVE_EXISTENCE", direction="BACKWARD", max_targets=1,
                max_scope=5, pattern=[{"LOWER": {"REGEX": "^detected"}}], on_match=check_no_x_detected,),
    ConTextRule("Value: Detected", "DEFINITE_POSITIVE_EXISTENCE", direction="BACKWARD", max_targets=1, max_scope=5, pattern=[
                {"LOWER": "value"}, {"LOWER": ":"}, {"LOWER": {"REGEX": "^detected"}}, ], on_match=check_no_x_detected,),
    ConTextRule("POSITIVEH", "DEFINITE_POSITIVE_EXISTENCE",
                direction="BACKWARD", max_targets=1, max_scope=5,),

    # =============="ADMISSION" will be used to set is_positive to True=======
    ConTextRule("Reason for admission:", "ADMISSION",
                direction="FORWARD", max_scope=6,),
    ConTextRule("inpatient with", "ADMISSION",
                direction="FORWARD", max_scope=6,),
    ConTextRule("discharged from", "ADMISSION",
                direction="FORWARD", max_scope=6,),
    ConTextRule("in icu for", "ADMISSION", direction="FORWARD", max_scope=6, pattern=[
                {"LOWER": "in"}, {"LOWER": {"REGEX": "^m?icu"}}, {"LOWER": {"IN": ["for", "with"]}}, ],),
    ConTextRule("admitted <DATE>", "ADMISSION", direction="FORWARD", pattern=[
                {"LEMMA": "admit", "POS": "VERB"}, {"LOWER": {"REGEX": "^[\d]{1,2}/[\d]{1,2}"}}, ],),
    ConTextRule("admitted with", "ADMISSION", direction="FORWARD", max_scope=None, pattern=[
                {"LOWER": {"REGEX": "admit"}, "POS": "VERB"}, {"LOWER": {"IN": ["with", "for"]}}, ],),
    ConTextRule("admitted to", "ADMISSION", direction="FORWARD",),
    ConTextRule("admitted on", "ADMISSION", direction="FORWARD"),
    ConTextRule("Reason for ED visit or Hospital Admission:",
                "ADMISSION", direction="FORWARD", max_scope=2,),
    ConTextRule("Reason for ICU:", "ADMISSION", direction="FORWARD"),
    ConTextRule("in the hospital for for", "ADMISSION", direction="FORWARD", max_scope=5, pattern=[{"LOWER": {"IN": [
                "in", "to"]}}, {"LOWER": "the", "OP": "?"}, {"LOWER": {"IN": ["hospital", "icu", "micu"]}}, {"LOWER": "for"}, ],),
    ConTextRule("in the hospital due to", "ADMISSION", direction="FORWARD", max_scope=5, pattern=[{"LOWER": {"IN": ["in", "to"]}}, {
                "LOWER": "the", "OP": "?"}, {"LOWER": {"IN": ["hospital", "icu", "micu"]}}, {"LOWER": "due"}, {"LOWER": "to"}, ],),
    ConTextRule("hospitalized for", "ADMISSION", direction="FORWARD", max_scope=5, pattern=[
                {"LOWER": {"REGEX": "hospitali"}}, {"_": {"concept_tag": "timex"}, "OP": "*"}, {"LOWER": "for"}, ],),
    ConTextRule("hospitalized due to", "ADMISSION", direction="FORWARD", max_scope=5, pattern=[{"LOWER": {
                "REGEX": "hospitali"}}, {"_": {"concept_tag": "timex"}, "OP": "*"}, {"LOWER": "due"}, {"LOWER": "to"}, ],),
    ConTextRule("admission for", "ADMISSION", direction="FORWARD"),

    # =============="PATIENT_EXPERIENCER" will be used to set is_positive to True and is_other_experience to be True =======
    # These will capture constructs such as "76-year-old male admitted for COVID-19"
    ConTextRule(
        # Optionally allow race, ie., "76-year-old **white** male with COVID-19"
        "<NUM> yo with", "PATIENT_EXPERIENCER", direction="FORWARD", pattern=[{"LIKE_NUM": True}, {"LOWER": "-", "OP": "?"}, {"LOWER": "year"}, {"LOWER": "-", "OP": "?"}, {"LOWER": "old"}, {"LOWER": {"IN": ["aa", "white", "black", "hispanic", "caucasian"]}, "OP": "?", }, {"OP": "?", "_": {"concept_tag": {"NOT_IN": ["family", "other_experiencer"]}}, }, {"LOWER": {"IN": ["with", "w", "w/", "admitted",]}}, ], max_scope=10,
    ),
    ConTextRule(
        "<NUM> yo with", "PATIENT_EXPERIENCER", direction="FORWARD", pattern=[{"LIKE_NUM": True}, {"LOWER": {"REGEX": "y[or]"}}, {"OP": "?", "_": {"concept_tag": {"NOT_IN": ["family", "other_experiencer"]}}, }, {"LOWER": {"IN": ["patient", "veteran"]}, "OP": "?"}, {"LOWER": {"IN": ["with", "w", "w/"]}}, ], max_scope=10,
    ),
    ConTextRule(
        "<NUM> y/o with", "PATIENT_EXPERIENCER", direction="FORWARD", pattern=[{"LIKE_NUM": True}, {"LOWER": "y"}, {"LOWER": "/"}, {"LOWER": "o"}, {"OP": "?"}, {"LOWER": {"IN": ["patient", "veteran"]}, "OP": "?"}, {"LOWER": {"IN": ["with", "w", "w/"]}}, ], max_scope=10,
    ),
    ConTextRule(
        "<NUM>yo with", "PATIENT_EXPERIENCER", direction="FORWARD", pattern=[{"LOWER": {"REGEX": "[\d]+yo"}}, {"OP": "?"}, {"LOWER": {"IN": ["patient", "veteran"]}, "OP": "?"}, {"LOWER": {"IN": ["with", "w", "w/"]}}, ], max_scope=10,
    ),
    ConTextRule(
        "the patient has", "PATIENT_EXPERIENCER", direction="FORWARD", max_scope=3, pattern=[{"LOWER": "the"}, {"LOWER": {"IN": ["veteran", "vet", "patient", "pt"]}}, {"LOWER": "has"}, ],
    ),

    # =============="FUTURE/HYPOTHETICAL" will be used to set is_hypothetical to True =================
    # This will capture cases where the patient doesn't actually have COVID-19 but are instead talking about precautions, general information, etc.
    ConTextRule("precaution", "FUTURE/HYPOTHETICAL", direction="BACKWARD",
                max_scope=2, pattern=[{"LOWER": {"REGEX": "precaution"}}],),
    ConTextRule("precautions:", "IGNORE", direction="FORWARD", max_scope=2),
    ConTextRule("precaution for", "FUTURE/HYPOTHETICAL", direction="FORWARD", pattern=[
                {"LOWER": {"REGEX": "precaution|protection|protect"}}, {"LOWER": {"IN": ["for", "against"]}}, ],),
    ConTextRule("concern about", "FUTURE/HYPOTHETICAL", direction="FORWARD"),
    ConTextRule("reports of", "FUTURE/HYPOTHETICAL", direction="FORWARD"),
    # If they're talking about vaccines, it's probably just the patient asking
    ConTextRule("vaccine", "FUTURE/HYPOTHETICAL", direction="BIDIRECTIONAL",
                allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},),
    ConTextRule("protect yourself", "FUTURE/HYPOTHETICAL",
                direction="FORWARD"),
    ConTextRule("prevention", "FUTURE/HYPOTHETICAL", direction="BIDIRECTIONAL",
                pattern=[{"LOWER": {"REGEX": "^prevent"}}],),
    ConTextRule("avoid", "FUTURE/HYPOTHETICAL", direction="FORWARD"),
    ConTextRule("questions about", "FUTURE/HYPOTHETICAL", direction="FORWARD", pattern=[{"LOWER": {"REGEX": "question"}}, {
                "LOWER": {"IN": ["about", "regarding", "re", "concerning", "on", "for"]}}, ], allowed_types={"COVID-19"},),
    ConTextRule("information about", "FUTURE/HYPOTHETICAL", direction="FORWARD", max_scope=3, allowed_types={
                "COVID-19"}, pattern=[{"LOWER": "information"}, {"LOWER": {"IN": ["about", "regarding"]}}],),
    ConTextRule("anxiety about", "FUTURE/HYPOTHETICAL", direction="FORWARD"),
    ConTextRule("ask about", "FUTURE/HYPOTHETICAL", direction="FORWARD", pattern=[
                {"LOWER": {"REGEX": "^ask"}}, {"LOWER": "about"}], allowed_types={"travel", "COVID-19"},),
    ConTextRule("education", "FUTURE/HYPOTHETICAL", direction="BIDIRECTIONAL",
                pattern=[{"LOWER": {"REGEX": "^educat"}}],),
    ConTextRule("instruction", "FUTURE/HYPOTHETICAL", direction="BIDIRECTIONAL",
                pattern=[{"LOWER": {"REGEX": "instruction"}}],),
    ConTextRule("information about", "FUTURE/HYPOTHETICAL", direction="FORWARD", max_scope=3, pattern=[
                {"LOWER": "information"}, {"LOWER": {"IN": ["on", "about", "regarding", "re"]}, "OP": "?"}, ],),
    ConTextRule("materials", "FUTURE/HYPOTHETICAL",
                direction="BIDIRECTIONAL",),
    ConTextRule("factsheet", "FUTURE/HYPOTHETICAL",
                direction="BIDIRECTIONAL",),
    ConTextRule("fact sheet", "FUTURE/HYPOTHETICAL",
                direction="BIDIRECTIONAL",),
    ConTextRule("protocol", "FUTURE/HYPOTHETICAL",
                direction="BIDIRECTIONAL", max_scope=3),
    ConTextRule("literature", "FUTURE/HYPOTHETICAL",
                direction="BIDIRECTIONAL"),
    ConTextRule("handout", "FUTURE/HYPOTHETICAL", direction="BIDIRECTIONAL", pattern=[
                {"LOWER": {"REGEX": "^informat"}, "OP": "?"}, {"LOWER": {"IN": ["handout", "handouts"]}}, ],),
    ConTextRule("anxious about", "FUTURE/HYPOTHETICAL", direction="FORWARD", pattern=[{"LOWER": {"IN": ["anxious", "worried", "worries", "worry", "worrying"]}}, {
                "LOWER": {"IN": ["about", "re", "regarding"]}, "OP": "?"}, ], allowed_types={"COVID-19", },),
    # "If COVID-19 test is positive"
    ConTextRule("if", "FUTURE/HYPOTHETICAL",
                direction="FORWARD", max_scope=10),

    # =============="SCREENING" will be used to set is_hypothetical to True =================
    ConTextRule("advisory", "SCREENING", direction="BIDIRECTIONAL",
                pattern=[{"LOWER": {"IN": ["advisory", "advisories"]}}],),
    ConTextRule("travel screen", "SCREENING", direction="BIDIRECTIONAL"),
    ConTextRule("travel screen:", "SCREENING", direction="BIDIRECTIONAL"),
    ConTextRule("Travel History Questionnaire",
                "SCREENING", direction="BIDIRECTIONAL"),
    ConTextRule("questionnaire:", "SCREENING",
                direction="BACKWARD", max_scope=2),
    ConTextRule("questionnaire", "SCREENING", direction="BACKWARD",
                max_scope=2, pattern=[{"LOWER": {"REGEX": "questionn?aire"}}],),
    ConTextRule("questions", "SCREENING", direction="BACKWARD",
                max_scope=2, pattern=[{"LEMMA": "question"}],),
    ConTextRule("screening", "SCREENING", direction="BIDIRECTIONAL", max_scope=10, pattern=[{"LOWER": {"REGEX": "^screen"}}],
                ),
    ConTextRule("prescreening", "SCREENING", direction="BIDIRECTIONAL",
                max_scope=None, pattern=[{"LOWER": {"REGEX": "prescreen"}}],),
    ConTextRule("front gate", "SCREENING", direction="BIDIRECTIONAL",),
    ConTextRule("have you", "NOT_RELEVANT", direction="FORWARD",),
    ConTextRule("This patient was screened for the following suspected travel related illness(es):",
                "FUTURE/HYPOTHETICAL", direction="BIDIRECTIONAL",),
    ConTextRule("will be traveling", "FUTURE/HYPOTHETICAL", direction="FORWARD", allowed_types={
                "location", "COVID-19"}, pattern=[{"LOWER": "will"}, {"LOWER": "be", "OP": "?"}, {"LOWER": {"REGEX": "travel"}}, ],),
    ConTextRule("travel plans", "FUTURE/HYPOTHETICAL",
                direction="FORWARD", allowed_types={"location", "COVID-19"},),
    ConTextRule("if you need", "FUTURE/HYPOTHETICAL", direction="FORWARD"
                ),  # "If you need to be tested for"
    ConTextRule("limit risk of", "FUTURE/HYPOTHETICAL", direction="FORWARD", allowed_types={"COVID-19"}, pattern=[{"LEMMA": {"IN": ["limit", "reduce", "lower", "minimize"]}}, {"LOWER": "the", "OP": "?"}, {"LEMMA": {"IN": ["risk", "chance", "possibility"]}}, {"LEMMA": "of"}, ],
                ),  # "If you need to be tested for"
    ConTextRule("plan to travel", "FUTURE/HYPOTHETICAL", direction="FORWARD", allowed_types={
                "location", "COVID-19"}, pattern=[{"LOWER": {"REGEX": "plan"}}, {"LOWER": "to"}, {"LOWER": {"REGEX": "travel"}}, ],),
    ConTextRule("N years ago", "HISTORICAL", direction="BIDIRECTIONAL", pattern=[
                {"LIKE_NUM": True, "OP": "?"}, {"LOWER": {"IN": ["year", "years"]}}, {"LOWER": "ago"}, ],),
    # Previously, these modifiers were set to be "HISTORICAL"
    # but are instead being marked as "POSITIVE" so that we identify any current
    # or past cases of COVID-19.
    ConTextRule("history of", "DEFINITE_POSITIVE_EXISTENCE", direction="FORWARD", max_scope=4, pattern=[
                {"LOWER": {"IN": ["hx", "-hx", "history"]}}, {"LOWER": "of"}],),
    ConTextRule("(resolved)", "DEFINITE_POSITIVE_EXISTENCE",
                direction="BACKWARD", max_scope=1),
    ConTextRule("in 20XX", "HISTORICAL", direction="BIDIRECTIONAL", max_scope=5, pattern=[
                {"LOWER": "in"}, {"OP": "?"}, {"TEXT": {"REGEX": "^20[01][0-9]$"}}],),
    # The following modifiers try to capture instances where a health department
    # or infection control team was contacted
    ConTextRule("contacted", "COMMUNICATION", direction="BIDIRECTIONAL", pattern=[{"LOWER": {"IN": ["contacted", "contact"]}, "POS": "VERB"}], allowed_types={"health department"},
                # on_match=callbacks.di,
                ),  # TODO: may have to disambiguate this with "came in contact"
    ConTextRule("contact", "CONTACT", direction="BIDIRECTIONAL", pattern=[
                {"LOWER": "contact", "POS": "NOUN"}], allowed_types={"COVID-19"}, on_match=disambiguate_contact,),
    ConTextRule("call", "COMMUNICATION", direction="BIDIRECTIONAL", pattern=[
                {"LOWER": {"REGEX": "^call"}}], allowed_types={"health department"},),
    ConTextRule("was contacted", "COMMUNICATION", direction="BIDIRECTIONAL", pattern=[{"LOWER": {
                "IN": ["was", "been"]}}, {"LOWER": "contacted"}], allowed_types={"health department"},),
    ConTextRule("notified", "COMMUNICATION", direction="BIDIRECTIONAL",
                allowed_types={"health department"},),
    ConTextRule("communicate with", "COMMUNICATION", direction="BIDIRECTIONAL", pattern=[{"LOWER": {"REGEX": "^communicate"}}, {
                "LOWER": {"IN": ["with", "w"]}}, {"LOWER": "/", "OP": "?"}, ], allowed_types={"health department"},),
    ConTextRule("sent to", "COMMUNICATION", direction="BIDIRECTIONAL", pattern=[
                {"LOWER": "sent"}, {"OP": "?"}, {"LOWER": "to"}], allowed_types={"health department"},),
    ConTextRule("sent", "COMMUNICATION", direction="BIDIRECTIONAL",
                allowed_types={"health department"},),
    ConTextRule("spoke with", "COMMUNICATION", direction="BIDIRECTIONAL", pattern=[
                {"LOWER": "spoke"}, {"LOWER": {"IN": ["with", "to"]}}], allowed_types={"health department"},),
    ConTextRule("consulted", "COMMUNICATION", direction="BIDIRECTIONAL", pattern=[{"LOWER": {
                "REGEX": "consult"}}, {"LOWER": "with", "OP": "?"}], allowed_types={"health department"},),
    ConTextRule("test for", "TEST", direction="BIDIRECTIONAL", allowed_types={
                "COVID-19", "OTHER_CORONAVIRUS"}, pattern=[{"LOWER": {"REGEX": "^test"}}, {"LOWER": "for", "OP": "?"}],),
    ConTextRule("retest for", "TEST", direction="BIDIRECTIONAL", allowed_types={
                "COVID-19", "OTHER_CORONAVIRUS"}, pattern=[{"LOWER": {"REGEX": "^retest"}}, {"LOWER": "for", "OP": "?"}],),
    ConTextRule("check for", "TEST", direction="FORWARD", allowed_types={
                "COVID-19", "OTHER_CORONAVIRUS"}, pattern=[{"LOWER": {"REGEX": "^check"}, "POS": "VERB"}, {"LOWER": "for"}],),
    ConTextRule("work up", "TEST", pattern=[{"LOWER": "work"}, {
                "LOWER": "-", "OP": "?"}, {"LOWER": "up"}],),
    ConTextRule("workup", "TEST"),
    ConTextRule("results", "TEST", direction="BACKWARD", max_scope=2),
    ConTextRule("evaluation", "TEST", direction="BIDIRECTIONAL",
                allowed_types={"COVID-19", "OTHER_CORONAVIRUS"}, max_scope=2,),
    ConTextRule("evaluated for", "TEST", direction="FORWARD", allowed_types={
                "COVID-19", "OTHER_CORONAVIRUS"}, pattern=[{"LOWER": {"REGEX": "^eval"}}, {"LOWER": "for"}],),
    ConTextRule("swab", "TEST", direction="BIDIRECTIONAL", pattern=[
                {"LOWER": {"REGEX": "^swab"}}], allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},),
    ConTextRule("PCR", "TEST", direction="BIDIRECTIONAL",
                allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},),
    ConTextRule("specimen sent", "TEST", direction="BIDIRECTIONAL",
                allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},),
    ConTextRule("awaiting results", "UNCERTAIN", direction="BIDIRECTIONAL"),
    ConTextRule("no risk factors for", "UNCERTAIN", direction="FORWARD", max_scope=5, pattern=[
                {"LOWER": "no"}, {"LOWER": "risk"}, {"LEMMA": "factor"}, {"LOWER": "for"}, ],),
    ConTextRule("at risk for", "UNCERTAIN", direction="FORWARD",
                allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},),
    ConTextRule("risk for", "UNCERTAIN", direction="FORWARD",
                allowed_types={"COVID-19", "OTHER_CORONAVIRUS"}, ),
    ConTextRule("risk", "UNCERTAIN", direction="BACKWARD",
                max_scope=1, pattern=[{"LOWER": {"IN": ["risk", "risks"]}}],),
    ConTextRule("risk factors for", "UNCERTAIN", direction="FORWARD", max_scope=5, pattern=[
                {"LOWER": "risk"}, {"LEMMA": "factor"}, {"LOWER": "for"}],),
    ConTextRule("investigation of", "UNCERTAIN",
                direction="FORWARD", max_scope=1),
    ConTextRule("to exclude", "UNCERTAIN", direction="FORWARD",),
    ConTextRule("awaiting", "UNCERTAIN",
                direction="BIDIRECTIONAL", max_scope=2),
    ConTextRule("question of", "UNCERTAIN", direction="FORWARD", max_scope=4),
    ConTextRule("differential diagnosis:", "UNCERTAIN",
                direction="FORWARD", max_scope=4),
    ConTextRule("ddx:", "UNCERTAIN", direction="FORWARD", max_scope=4),
    ConTextRule("currently being ruled out or has tested positive for",
                "UNCERTAIN", direction="BIDIRECTIONAL",),
    ConTextRule("person of interest", "UNCERTAIN", direction="BIDIRECTIONAL", pattern=[
                {"LEMMA": {"IN": ["person", "patient"]}}, {"LOWER": "of"}, {"LOWER": "interest"}, ],),
    ConTextRule("under investigation", "UNCERTAIN", direction="BIDIRECTIONAL"),
    ConTextRule("may be positive for", "UNCERTAIN", direction="FORWARD", allowed_types={"COVID-19", "OTHER_CORONAVIRUS"}, pattern=[
                {"LOWER": {"IN": ["may", "might"]}}, {"LOWER": "be"}, {"LOWER": "positive"}, {"LOWER": "for"}, ],),
    ConTextRule("may be positive", "UNCERTAIN", direction="BIDIRECTIONAL", allowed_types={
                "COVID-19", "OTHER_CORONAVIRUS"}, pattern=[{"LOWER": {"IN": ["may", "might"]}}, {"LOWER": "be"}, {"LOWER": "positive"}, ],),
    ConTextRule("area with", "OTHER_EXPERIENCER", pattern=[{"LOWER": {"IN": [
                "area", "county", "comsmunity", "city"]}}, {"LOWER": {"IN": ["with", "of"]}}, ],),
    ConTextRule("facility with", "OTHER_EXPERIENCER", direction="FORWARD", pattern=[
                {"LOWER": "facility"}, {"LOWER": {"IN": ["with", "has"]}}, {"LOWER": "a"}, ],),
    ConTextRule("known to have", "OTHER_EXPERIENCER", direction="FORWARD"),
    ConTextRule("same room", "OTHER_EXPERIENCER", pattern=[
                {"LOWER": "same"}, {"OP": "?"}, {"LOWER": {"REGEX": "room"}}],),
    ConTextRule("in the building", "OTHER_EXPERIENCER",
                direction="BIDIRECTIONAL"),
    ConTextRule("several residents", "OTHER_EXPERIENCER", direction="FORWARD", pattern=[
                {"LOWER": {"IN": ["multiple", "several"]}}, {"LOWER": "residents"}],),
    ConTextRule(
        "one of the residents",
        "OTHER_EXPERIENCER",
        direction="FORWARD",
        pattern=[
            {"LOWER": {"IN": ["multiple", "several", "one"]}},
            {"LOWER": "of"},
            {"LOWER": "the"},
            {"LOWER": "residents"},
        ],
    ),
    ConTextRule("patients with", "OTHER_EXPERIENCER", direction="FORWARD",),
    ConTextRule(
        "travel",
        "UNCERTAIN",
        direction="BIDIRECTIONAL",
        pattern=[{"LOWER": {"IN": ["flew", "traveled", "travelled"]}}],
    ),
    ConTextRule("got back from", "UNCERTAIN", direction="BIDIRECTIONAL"),
    ConTextRule("was recently in", "UNCERTAIN", direction="BIDIRECTIONAL"),
    ConTextRule(
        "positive screen",
        "UNCERTAIN",
        direction="BIDIRECTIONAL",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextRule(
        "positive criteria",
        "UNCERTAIN",
        direction="BIDIRECTIONAL",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextRule(
        "positive triage",
        "UNCERTAIN",
        direction="BIDIRECTIONAL",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextRule(
        "pending",
        "UNCERTAIN",
        direction="BIDIRECTIONAL",
        pattern=[{"LOWER": {"REGEX": "^test"},
                  "OP": "?"}, {"LOWER": "pending"}],
    ),
    ConTextRule(
        "screen positive",
        "UNCERTAIN",
        direction="BIDIRECTIONAL",
        pattern=[
            {"LOWER": {"REGEX": "screen"}},
            {"OP": "?"},
            {"OP": "?"},
            {"LOWER": {"IN": ["positive", "pos"]}},
        ],
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextRule(
        "possible",
        "UNCERTAIN",
        direction="FORWARD",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextRule(
        "possibly",
        "UNCERTAIN",
        direction="FORWARD",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextRule(
        "possible positive",
        "UNCERTAIN",
        direction="BIDIRECTIONAL",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        pattern=[{"LOWER": {"REGEX": "possibl"}}, {"LOWER": "positive"}],
    ),
    ConTextRule(
        "risk of",
        "UNCERTAIN",
        direction="FORWARD",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        max_scope=5,
    ),
    ConTextRule(
        "likely",
        "UNCERTAIN",
        direction="FORWARD",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        max_scope=5,
    ),
    ConTextRule(
        "probable",
        "UNCERTAIN",
        direction="FORWARD",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        max_scope=5,
    ),
    ConTextRule(
        "probably",
        "UNCERTAIN",
        direction="FORWARD",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        max_scope=5,
    ),
    ConTextRule(
        "questionnaire",
        "UNCERTAIN",
        direction="BIDIRECTIONAL",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        max_scope=2,
    ),
    ConTextRule(
        "suspicion",
        "UNCERTAIN",
        direction="BIDIRECTIONAL",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextRule(
        "suspect",
        "UNCERTAIN",
        direction="BIDIRECTIONAL",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        pattern=[{"LOWER": {"REGEX": "^suspect"}}],
    ),
    ConTextRule(
        "suspicious for",
        "UNCERTAIN",
        direction="FORWARD",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextRule("differential diagnosis", "UNCERTAIN",
                direction="BIDIRECTIONAL"),
    ConTextRule(
        "differential diagnosis",
        "UNCERTAIN",
        direction="BIDIRECTIONAL",
        pattern=[{"LOWER": "ddx"}, {"LOWER": ":", "OP": "?"}],
    ),
    ConTextRule("symptoms", "SYMPTOM", max_scope=4,),
    ConTextRule(
        "symptoms of",
        "UNCERTAIN",
        direction="FORWARD",
        allowed_types={"COVID-19"},
        pattern=[
            {"LOWER": "positive", "OP": "?"},
            {"LEMMA": {"IN": ["sign", "symptom"]}},
            {"LOWER": "of"},
        ],
        max_scope=4,
    ),
    ConTextRule(
        "s/s", "UNCERTAIN", direction="BIDIRECTIONAL", allowed_types={"COVID-19"}, max_scope=5
    ),
    ConTextRule(
        "sx", "UNCERTAIN", direction="BIDIRECTIONAL", allowed_types={"COVID-19"}, max_scope=5
    ),
    ConTextRule(
        "potential",
        "UNCERTAIN",
        direction="FORWARD",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        pattern=[{"LOWER": {"REGEX": "^potential"}}],
    ),
    ConTextRule(
        "possible exposure",
        "UNCERTAIN",
        # allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        direction="BIDIRECTIONAL",
        pattern=[
            {"LOWER": {"IN": ["possible", "potential"]}},
            {"OP": "?"},
            {"LOWER": "exposure"},
        ],
    ),
    ConTextRule(
        "exposure",
        "UNCERTAIN",
        direction="BIDIRECTIONAL",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        pattern=[{"LOWER": {"REGEX": "^exposure"}}],
        on_match=disambiguate_exposure,
    ),
    ConTextRule(
        "may have been exposed",
        "UNCERTAIN",
        direction="BIDIRECTIONAL",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextRule(
        "exposed to <X>",
        "CONTACT",
        direction="FORWARD",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        pattern=[
            {"LOWER": {"REGEX": "^expos"}},
            {"LOWER": "to"},
            {"POS": "NOUN", "OP": "?", "_": {"concept_tag": ""}},
        ],
    ),
    ConTextRule(
        "concern for",
        "UNCERTAIN",
        direction="FORWARD",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        pattern=[{"LOWER": {"IN": ["concern"]}},
                 {"LOWER": {"IN": ["of", "for"]}}],
    ),
    ConTextRule("concerns", "UNCERTAIN", direction="BIDIRECTIONAL"),
    ConTextRule("if positive", "UNCERTAIN", direction="BIDIRECTIONAL"),
    ConTextRule("if negative", "UNCERTAIN", direction="BIDIRECTIONAL"),
    # ConTextRule("if", "UNCERTAIN",direction="BIDIRECTIONAL", max_scope=5), # "if his covid-19 is positive"
    ConTextRule("if you", "FUTURE/HYPOTHETICAL", direction="FORWARD"),
    ConTextRule(
        "c/f", "UNCERTAIN", direction="FORWARD", allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextRule(
        "assessed for",
        "UNCERTAIN",
        direction="FORWARD",
        pattern=[{"LOWER": {"IN": ["assess", "assessed"]}}, {"LOWER": "for"}],
    ),
    ConTextRule("concerning for", "UNCERTAIN", direction="FORWARD"),
    ConTextRule("r/o", "UNCERTAIN", direction="BIDIRECTIONAL", max_scope=2,),
    ConTextRule("r/o.", "UNCERTAIN", direction="BIDIRECTIONAL", max_scope=2,),
    ConTextRule(
        "rule out",
        "UNCERTAIN",
        direction="BIDIRECTIONAL",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        max_scope=5,
        pattern=[{"LEMMA": "rule"}, {
            "TEXT": "-", "OP": "?"}, {"LOWER": "out"}],
    ),
    ConTextRule(
        "ro",
        "UNCERTAIN",
        direction="BIDIRECTIONAL",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        max_scope=2,
    ),
    ConTextRule(
        "be ruled out",
        "UNCERTAIN",
        direction="FORWARD",
        max_scope=5,
        pattern=[
            {"LOWER": {"IN": ["be", "being"]}},
            {"LOWER": "ruled"},
            {"LOWER": "out"},
            {"LOWER": "for"},
        ],
    ),
    ConTextRule(
        "vs.",
        "UNCERTAIN",
        direction="BIDIRECTIONAL",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        max_scope=5,
        pattern=[{"LOWER": {"REGEX": "^(vs\.?|versus)$"}}],
    ),
    # certainty = low
    ConTextRule("unlikely", "UNLIKELY", direction="BIDIRECTIONAL"),
    ConTextRule("unlikely to be", "UNLIKELY", direction="FORWARD"),
    ConTextRule(
        "doubt", "UNLIKELY", direction="FORWARD", allowed_types={"COVID-19", "OTHER_CORONAVIRUS"}
    ),
    ConTextRule(
        "doubtful",
        "UNLIKELY",
        direction="BIDIRECTIONAL",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextRule(
        "unlikely to be positive",
        "UNLIKELY",
        direction="BIDIRECTIONAL",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
    ),
    ConTextRule("low suspicion", "UNLIKELY", direction="BIDIRECTIONAL"),
    ConTextRule("low probability", "UNLIKELY", direction="BIDIRECTIONAL"),
    ConTextRule(
        "not recommend",
        "UNLIKELY",
        direction="FORWARD",
        pattern=[
            {"LOWER": "not"},
            {"LOWER": "recommend"},
            {"LOWER": {"REGEX": "test"}},
        ],
    ),
    ConTextRule("extremely low", "UNLIKELY",direction="BACKWARD", max_scope=3),
    ConTextRule("low risk of", "UNLIKELY", direction="FORWARD", max_scope=3),
    ConTextRule("is unlikely", "UNLIKELY",direction="BACKWARD"),
    ConTextRule(
        "low risk of",
        "UNLIKELY",
        direction="FORWARD",
        pattern=[{"LOWER": "low"}, {"LOWER": "risk"},
                 {"LOWER": {"IN": ["in", "for"]}}],
    ),
    ConTextRule(
        "positive patients",
        "OTHER_EXPERIENCER",
        direction="BIDIRECTIONAL",
        pattern=[
            {"LOWER": {"IN": ["pos", "positive", "+"]}},
            {"LOWER": {"IN": ["pts", "patients"]}},
        ],
    ),
    ConTextRule(
        "patients",
        "OTHER_EXPERIENCER",
        direction="BIDIRECTIONAL",
        max_scope=10,
        pattern=[{"LOWER": {"IN": ["pts", "patients"]}}],
    ),
    ConTextRule(
        "other person",
        "OTHER_EXPERIENCER",
        direction="FORWARD",
        pattern=[{"_": {"concept_tag": "other_experiencer"}, "OP": "+"},],
    ),
    ConTextRule("family member", "OTHER_EXPERIENCER", direction="FORWARD", pattern=[
                {"_": {"concept_tag": "family"}, "OP": "+"},], on_match=family_speaker,),
    ConTextRule(
        "<OTHER_EXPERIENCER> tested positive",
        "OTHER_EXPERIENCER",
        pattern=[
            {"_": {"concept_tag": {
                "IN": ["other_experiencer", "family"]}}, "OP": "+"},
            {"LOWER": {"REGEX": "^test"}},
            {"_": {"concept_tag": "positive"}, "OP": "+"},
            {"LOWER": "for", "OP": "?"},
        ],
    ),
    ConTextRule(
        "other patient",
        "OTHER_EXPERIENCER",
        direction="BIDIRECTIONAL",
        pattern=[
            {"LOWER": {"REGEX": "other"}},
            {"LOWER": {"REGEX": "(patient|resident|veteran|soldier)"}},
        ],
    ),
    ConTextRule(
        "a patient",
        "OTHER_EXPERIENCER",
        direction="BIDIRECTIONAL",
        pattern=[
            {"LOWER": "a"},
            {"LOWER": {"IN": ["patient", "pt", "pt.", "resident"]}},
        ],
    ),
    ConTextRule("any one", "OTHER_EXPERIENCER",
                direction="BIDIRECTIONAL", max_scope=100),
    ConTextRule(
        "contact with",
        "OTHER_EXPERIENCER",
        direction="BIDIRECTIONAL",
        max_scope=1000,
        pattern=[
            {"LEMMA": "contact", "POS": {"NOT_IN": ["VERB"]}},
            {"LOWER": "with"},
            {"LOWER": "known", "OP": "?"},
        ],
    ),
    ConTextRule("had contact", "OTHER_EXPERIENCER",
                direction="BIDIRECTIONAL", max_scope=1000,),
    ConTextRule("same building", "OTHER_EXPERIENCER",
                direction="BIDIRECTIONAL", max_scope=1000,),
    ConTextRule("same floor", "OTHER_EXPERIENCER",
                direction="BIDIRECTIONAL", max_scope=1000,),
    ConTextRule(
        "cared for",
        "OTHER_EXPERIENCER",
        # The patient is a nurse who cared for a patient with COVID-19
        direction="BIDIRECTIONAL",
        pattern=[{"LEMMA": "care"}, {"LOWER": "for"}],
    ),
    ConTextRule(
        "the woman/man",
        "OTHER_EXPERIENCER",
        direction="BIDIRECTIONAL",
        pattern=[
            {"LOWER": {"IN": ["a", "the"]}},
            {"LOWER": {"IN": ["man", "men", "woman", "women"]}},
        ],
    ),
    ConTextRule(
        "XXmate",
        "OTHER_EXPERIENCER",
        direction="BIDIRECTIONAL",  # "roommate", "housemate", etc...
        pattern=[{"LOWER": {"REGEX": "mates?$"}}],
    ),
    ConTextRule(
        "clean",
        "OTHER_EXPERIENCER",
        direction="BIDIRECTIONAL",
        pattern=[{"LEMMA": "clean", "POS": "VERB"}],
    ),  # "She has been cleaning covid-19 positive rooms"
    ConTextRule(
        "A X tested positive",
        "OTHER_EXPERIENCER",
        direction="BIDIRECTIONAL",
        pattern=[
            {"LOWER": {"IN": ["a", "an", "another"]}},
            {"POS": "NOUN"},
            {"LOWER": "tested"},
            {"LOWER": "positive"},
        ],
    ),
    # Since this is not very clinical, more likely to be from the pt's perspective; should review
    # Example: " is concerned about the coronavirus as she works at costco
    # ConTextRule("request", "FUTURE/HYPOTHETICAL",direction="FORWARD", pattern=[{"LEMMA": "request"}]),
    ConTextRule(
        "concerned about",
        "FUTURE/HYPOTHETICAL",
        direction="FORWARD",
        pattern=[{"LOWER": {"REGEX": "concern"}}, {"LOWER": "about"}],
        max_scope=3,
    ),
    ConTextRule(
        "patient concern for",
        "FUTURE/HYPOTHETICAL",
        direction="FORWARD",
        allowed_types={"COVID-19", "OTHER_CORONAVIRUS"},
        pattern=[
            {"LOWER": {"IN": ["pt", "patient"]}},
            {"LOWER": {"IN": ["concern"]}},
            {"LOWER": {"IN": ["of", "for"]}},
        ],
    ),
    ConTextRule(
        "he thinks he has",
        "FUTURE/HYPOTHETICAL",
        direction="FORWARD",
        pattern=[
            {"LOWER": {"IN": ["he", "she"]}},
            {"LOWER": {"REGEX": "(think|thought)"}},
            {"LOWER": {"IN": ["he", "she"]}},
            {"LOWER": {"IN": ["has", "had", "have"]}},
        ],
    ),
    ConTextRule(
        "she would like",
        "FUTURE/HYPOTHETICAL",
        direction="FORWARD",
        pattern=[{"POS": "PRON"}, {"LOWER": "would"}, {"LOWER": "like"}],
    ),
    ConTextRule(
        "desires", "FUTURE/HYPOTHETICAL", direction="FORWARD", pattern=[{"LEMMA": "desire"}]
    ),
    ConTextRule(
        "concerned for",
        "FUTURE/HYPOTHETICAL",
        direction="FORWARD",
        pattern=[{"LOWER": "concerned"}, {"LOWER": "for"}],
    ),
    ConTextRule(
        "prepare for",
        "FUTURE/HYPOTHETICAL",
        direction="FORWARD",
        pattern=[
            {"LOWER": {"REGEX": "prepare"}},
            {"LOWER": {"IN": ["for", "against"]}},
        ],
    ),
    ConTextRule("mers", "NOT_RELEVANT", direction="FORWARD",
                allowed_types={"COVID-19"}),
    ConTextRule(
        "seen in", "NOT_RELEVANT", direction="FORWARD", allowed_types={"COVID-19"}, max_scope=2
    ),  # "commonly seen in COVID-19 pneumonia"
    ConTextRule(
        "seen in the setting of",
        "NOT_RELEVANT",
        direction="FORWARD",
        allowed_types={"COVID-19"},
        max_scope=6,
        pattern=[
            {"LOWER": "seen"},
            {"LOWER": "in"},
            {"LOWER": "the", "OP": "?"},
            {"LOWER": "setting"},
            {"LOWER": "of"},
        ],
    ),
    # These mental health terms below will rule out cases where the patient
    # is anxious about the pandemic or about being exposed to COVID-19
    # but may not have any symptoms or diagnosis.
    # Example: "The patient is very anxious about the COVID-19 disease and is scared they will catch it."
    # But you should be cautious about them as well because they could cause potential false negatives.
    ConTextRule(
        "anxiety",
        "MENTAL_HEALTH",
        direction="BIDIRECTIONAL",
        allowed_types={"COVID-19"},
        pattern=[
            {
                "LOWER": {
                    "IN": [
                        "anxious",
                        "anxiety",
                        "afraid",
                        "fear",
                        "fears",
                        "nervous",
                        "scared",
                        "scare",
                        "panic",
                        "panick",
                        "panicking",
                        "obsess",
                        "obsessed",
                        "obsessing",
                        "stress",
                        "stressor",
                        "stressors",
                    ]
                }
            }
        ],
        max_scope=5,
    ),
    # Cancel vacation due to COVID
    ConTextRule(
        "cancel vacation",
        "FUTURE/HYPOTHETICAL",
        direction="BIDIRECTIONAL",
        pattern=[
            {"LOWER": {"REGEX": "^cancel"}},
            {
                "LOWER": {
                    "IN": [
                        "flight",
                        "flights",
                        "plan",
                        "plans",
                        "trip",
                        "trips",
                        "vacation",
                    ]
                },
            },
        ],
    ),
    ConTextRule(
        "supposed to travel",
        "NOT_RELEVANT",
        direction="BIDIRECTIONAL",
        pattern=[
            {"LOWER": "supposed"},
            {"LOWER": "to"},
            {"LOWER": {"IN": ["travel", "go", "visit"]}},
        ],
    ),
    ConTextRule("called off", "FUTURE/HYPOTHETICAL",
                direction="BIDIRECTIONAL"),
    ConTextRule("goals:", "FUTURE/HYPOTHETICAL", direction="FORWARD"),
    ConTextRule(
        "a positive case of",
        "NOT_RELEVANT",
        direction="FORWARD",
        allowed_types={"COVID-19"},
        max_scope=2,
    ),
    ConTextRule(
        "a confirmed case of",
        "NOT_RELEVANT",
        direction="FORWARD",
        allowed_types={"COVID-19"},
        max_scope=2,
    ),
    ConTextRule(
        "there has been",
        "NOT_RELEVANT",
        direction="FORWARD",
        allowed_types={"COVID-19"},
        max_scope=10,  # "He was in NYC, where there have been manyt confirmed cases"
        pattern=[
            {"LOWER": "there"},
            {"LOWER": {"IN": ["has", "have"]}},
            {"LOWER": "been"},
        ],
    ),
    ConTextRule(
        "in the area",
        "NOT_RELEVANT",
        direction="BIDIRECTIONAL",
        pattern=[
            {"LOWER": "in"},
            {"LOWER": "the"},
            {"LOWER": {"IN": ["area", "community"]}},
        ],
    ),
    ConTextRule(
        "cases",
        "NOT_RELEVANT",
        direction="BIDIRECTIONAL",
        allowed_types={"COVID-19"},
        max_scope=2,
    ),
    ConTextRule(
        "outbreak of",
        "NOT_RELEVANT",
        direction="FORWARD",
        allowed_types={"COVID-19"},
        max_scope=1,
    ),
    ConTextRule(
        "outbreak",
        "NOT_RELEVANT",
        direction="BIDIRECTIONAL",
        allowed_types={"COVID-19"},
        max_scope=2,
    ),
    ConTextRule(
        "epidemic",
        "NOT_RELEVANT",
        direction="BIDIRECTIONAL",
        allowed_types={"COVID-19"},
        max_scope=2,
    ),
    ConTextRule(
        "pandemic",
        "NOT_RELEVANT",
        direction="BIDIRECTIONAL",
        allowed_types={"COVID-19"},
        max_scope=2,
    ),
    ConTextRule(
        "national emergency",
        "NOT_RELEVANT",
        direction="BIDIRECTIONAL",
        allowed_types={"COVID-19"},
        max_scope=2,
    ),
    ConTextRule(
        "crisis",
        "NOT_RELEVANT",
        direction="BIDIRECTIONAL",
        allowed_types={"COVID-19"},
        max_scope=2,
    ),
    ConTextRule(
        "situation",
        "NOT_RELEVANT",
        direction="BIDIRECTIONAL",
        allowed_types={"COVID-19"},
        max_scope=2,
    ),
    ConTextRule(
        "mandate",
        "NOT_RELEVANT",
        direction="BIDIRECTIONAL",
        allowed_types={"COVID-19"},
        max_scope=2,
        pattern=[{"LOWER": {"REGEX": "mandate"}}],
    ),
    ConTextRule(
        "news",
        "NOT_RELEVANT",
        direction="BIDIRECTIONAL",
        allowed_types={"COVID-19"},
        pattern=[ { "LOWER": { "IN": [ "news", "media", "tv", "television", "broadcast", "headline", "headlines", "newspaper", "newspapers", ] } } ],
    ),
    ConTextRule("clinic cancellation", "NOT_RELEVANT",
                direction="BIDIRECTIONAL"),
    # ConTextRule("flight/trip", "NOT_RELEVANT",direction="BIDIRECTIONAL", allowed_types={"COVID-19"},
    #             pattern=[{"LOWER": {"IN": ["flight", "flights",
    #                                        "trip", "trips",
    #                                 "vacation", "vacations"]}}]), # "cancelled his flight because of coronavirus"
    ConTextRule(
        "read about",
        "NOT_RELEVANT",
        direction="BIDIRECTIONAL",
        allowed_types={"COVID-19"},
        pattern=[{"LOWER": {"REGEX": "^read"}}, {"LOWER": "about"}],
    ),
    ConTextRule(
        "deployment",
        "NOT_RELEVANT",
        direction="BIDIRECTIONAL",
        pattern=[{"LOWER": {"REGEX": "deploy"}}],
        allowed_types={"COVID-19"},
    ),
    # ConTextRule("current events", "NOT_RELEVANT",direction="BIDIRECTIONAL",
    #             pattern=[{"LOWER": {"IN": ["current", "recent"]}},
    #                      {"LOWER": {"REGEX": "^event"}}]), # Discussing current events for cognitive understanding
    # ConTextRule("topics", "NOT_RELEVANT",direction="BIDIRECTIONAL",
    #             pattern=[{"LOWER": {"REGEX": "^topic"}}]), # Discussing current events for cognitive understanding
    ConTextRule(
        "come in close contact", "NOT_RELEVANT", direction="BIDIRECTIONAL",
        # Common phrase used in screenings allowed_types={"COVID-19", "travel"},
        pattern=[{"LOWER": "in"}, {"LOWER": "close"}, {
            "LOWER": "contact"}, {"LOWER": "with"}, ],
    ),
    ConTextRule("?", "NOT_RELEVANT",direction="BACKWARD", max_scope=2),
    # ConTextRule("in the last 14 days", "NOT_RELEVANT",direction="BIDIRECTIONAL"),
    ConTextRule("have you had close contact",
                "NOT_RELEVANT", direction="BIDIRECTIONAL"),
    # 'Checkup done via telephone because of COVID-19.'
    # Won't match: 'Pt notified via telephone of his positive COVID-19 result.'
    # ConTextRule("telephone", "NOT_RELEVANT",direction="BIDIRECTIONAL", pattern=[{"LOWER": {"IN": ["telephone", "telehealth"]}}],
    #             on_match=callbacks.check_telephone_notification),
    # Group therapy sessions
    ConTextRule("the group", "NOT_RELEVANT", direction="FORWARD"),
    ConTextRule("session", "NOT_RELEVANT", direction="FORWARD", pattern=[{"LOWER": {"REGEX": "^session"}}]
                ),  # Group therapy sessions
    # ConTextRule("mental health", "NOT_RELEVANT",direction="BIDIRECTIONAL"),
    ConTextRule("website", "NOT_RELEVANT", direction="BIDIRECTIONAL"),
    ConTextRule("web site", "NOT_RELEVANT", direction="BIDIRECTIONAL"),
    ConTextRule("internet", "NOT_RELEVANT", direction="BIDIRECTIONAL"),
    # ConTextRule("global", "NOT_RELEVANT",direction="BIDIRECTIONAL"),
    ConTextRule("worldwide", "NOT_RELEVANT", direction="BIDIRECTIONAL"),
    ConTextRule("world wide", "NOT_RELEVANT", direction="BIDIRECTIONAL"),
    ConTextRule("world-wide", "NOT_RELEVANT", direction="BIDIRECTIONAL"),
    # "Patients with confirmed covid-19 should stay home"
    ConTextRule(
        "patients with", "NOT_RELEVANT", direction="FORWARD", max_scope=3,
        pattern=[{"LOWER": {"IN": ["persons", "patients", "people"]}}, {"LOWER": "with"}, {
            "LOWER": "confirmed"}, {"LOWER": "or", "OP": "?"}, {"LOWER": "suspected", "OP": "?"}, ],
    ),
    ConTextRule(
        "nurse notes:", "NOT_RELEVANT", direction="FORWARD",  # often precedes a screening
        pattern=[{"LOWER": {"IN": ["nurse", "nurses", "rn"]}}, {"LOWER": "notes"}],
    ),
    # ConTextRule("mental health", "NOT_RELEVANT",direction="BIDIRECTIONAL",
    #             pattern=[{"LOWER": {"IN": ["psychiatry", "psychotic", "paranoid", "paranoia", "psych"]}}]),
    ConTextRule("countries with cases", "NOT_RELEVANT", direction="BIDIRECTIONAL"),
    # ConTextRule(":", "NOT_RELEVANT",direction="BACKWARD", max_scope=1), # "Coronavirus: ..."
    ConTextRule("cases of", "NOT_RELEVANT", direction="FORWARD", max_scope=3),  # "his daughter lives in Seoul, where cases of coronavirus have been discovered"
    # ConTextRule("alert and oriented", "NOT_RELEVANT",direction="FORWARD"),
    # ConTextRule("the", "NOT_RELEVANT",direction="FORWARD", max_scope=1, allowed_types={"COVID-19"}), # When clinicians are relaying a patient's anxieties or questions, they often use 'the coronavirus', whereas when they're using their own clinical judgment they just say 'coronavirus'
    ConTextRule("been in contact with anyone confirmed", "NOT_RELEVANT", direction="BIDIRECTIONAL"),
    ConTextRule("error", "NOT_RELEVANT", direction="BIDIRECTIONAL"),  # "COVID-19 marked positive in error"
    ConTextRule("elective", "NOT_RELEVANT", direction="BIDIRECTIONAL", max_scope=5),  # "elective surgeries will be scheduled after COVID-19 has ended"
    ConTextRule("rescheduled", "NOT_RELEVANT", direction="BIDIRECTIONAL", pattern=[{"LEMMA": "reschedule"}],),
    ConTextRule("postponed", "NOT_RELEVANT", direction="BIDIRECTIONAL", pattern=[{"LEMMA": "postpone"}]),
    ConTextRule(
        "barriers to travel", "NOT_RELEVANT", direction="BIDIRECTIONAL",
        pattern=[{"LEMMA": "barrier"}, {"LOWER": "to"}, {"LOWER": "travel"}],
    ),
    # Contact with sick individuals
    ConTextRule(
        "positive individual", "CONTACT", direction="BIDIRECTIONAL",
        pattern=[{"LOWER": {"IN": ["positive", "+", "confirmed"]}, "POS": "ADJ"},
                 {"LEMMA": {"IN": ["individual", "contact", "patient"]}}, ],
    ),
    ConTextRule("someone who has tested positive", "CONTACT", direction="BIDIRECTIONAL",
                pattern=[{"LEMMA": {"IN": ["someone", "person", "people"]}}, {"LOWER": "who"}, {"LEMMA": {"IN": ["has", "have"]}}, {"LOWER": "tested"}, {"LOWER": "positive"}, ],),
    ConTextRule("contact with", "CONTACT", direction="FORWARD", pattern=[
                {"LOWER": "contact"}, {"LOWER": {"REGEX": "w(/|ith)?$"}}],),
    ConTextRule("social worker", "IGNORE", direction="BIDIRECTIONAL"),
    ConTextRule("initially negative", "IGNORE", direction="BIDIRECTIONAL"),
    ConTextRule("likely recovered", "IGNORE", direction="BIDIRECTIONAL"),
    ConTextRule("not aware", "IGNORE", direction="BIDIRECTIONAL"),
    ConTextRule("positive cases", "IGNORE", direction="BIDIRECTIONAL"),
    ConTextRule("client history", "IGNORE", direction="BIDIRECTIONAL"),
    ConTextRule("emergency contact", "IGNORE", direction="BIDIRECTIONAL"),
    ConTextRule("several positive", "IGNORE", direction="BIDIRECTIONAL"),
    ConTextRule("special instructions:", "IGNORE", direction="BIDIRECTIONAL"),
    ConTextRule("positive symptoms", "IGNORE", direction="BIDIRECTIONAL", pattern=[
                {"LOWER": "positive"}, {"LOWER": {"REGEX": "symptom|sign"}}],),
    # Ignore "history" in "history of present illness"
    ConTextRule("history of present illness", "IGNORE",
               direction="TERMINATE", allowed_types={"COVID-19"}),
    ConTextRule("does not know", "IGNORE",direction="TERMINATE"),
    ConTextRule("benign", "SPECIFIED_STRAIN",
                direction="BIDIRECTIONAL", allowed_types={"COVID-19"}),
    ConTextRule("but", "CONJ",direction="TERMINATE"),
    ConTextRule("therefore", "CONJ",direction="TERMINATE"),
    ConTextRule(";", "CONJ",direction="TERMINATE"),
    # "Positive for X" should terminate
    ConTextRule("Metapneumovirus", "CONJ",direction="TERMINATE"),
    ConTextRule("flu", "CONJ",direction="TERMINATE", pattern=[
                {"LOWER": {"REGEX": "flu"}}]),  # Stop modifiers for flu
    # ConTextRule("who", "CONJ",direction="TERMINATE"), # example: "male with history of afib, who recently came back from China"
]


"""
1. remove entity 
    - tagged with ignore/education
    - followed by a question mark..
    - contains denies/contact, false positive?
2. set entity to be positive
    - if contains infection/penumonia/ards, false positive
    - if beginning of sentence has something?
    - if sentence is incorrectly splitted on '+'
    - look at its next sentence if possible
    - if a patient is admitted to the covid unit
3. set entity to be uncertain if hypothetical/in the future
    - covid-19 occurs in the positive section, but doesn't have definite positive existence
    - change to quite certain if modified by screening and test
    - uncertain if admitted for testing and not poisitive
    - uncertain if subjunctive, e.g., will contact patient should his covid-19 test return positive 虚拟
    - change to quite certain if modified by precautions?
    - change to quite certain if has a retest pending
    - change to quite certain if followed by with signs/symptoms
    - change to quite certain if followed by symptoms?
4. negation and label
    - negation + pending => it should be uncertain not negation
    - if repeat test is negative, then it should be false positive
    - if modified by a specific strain of covid, set label to specified coronavirus
    - if modified by both screen and positive, change label to positive coronavirus screening
"""
postprocess_rules = [
    PostprocessingRule(
        patterns=[PostprocessingPattern(lambda ent: ent.label_.upper(), success_value="IGNORE")], 
        action=F.remove_ent, description="Remove any entities which were tagged to be ignored.",
    ),
    PostprocessingRule(
        patterns=[PostprocessingPattern(F.is_modified_by_text, True, target="education")], 
        action=F.remove_ent, description="Remove any entities which are modified by 'education'",
    ),
    PostprocessingRule(
        patterns=[
            # PostprocessingPattern(F.is_followed_by, condition_args=("?",2))
            PostprocessingPattern(lambda ent: ent.label_, success_value="COVID-19"), 
            PostprocessingPattern( lambda ent: "?" in ent.sent[-3:].text, True, )], 
        action=F.remove_ent, description="Remove any entities which are followed by a question mark since this are often screenings.",
    ),
    PostprocessingRule(
        patterns=[
            PostprocessingPattern(lambda ent: ent.label_, "COVID-19"),
            PostprocessingPattern(F.sentence_contains, True, target={"deny", "denies", "denied"}),
            PostprocessingPattern(F.sentence_contains, True, target={"contact", "contacts", "confirmed"}),
        ],
        action=F.remove_ent, description="Remove a coronavirus entity if 'denies' and 'contact' are in. This will help get rid of false positives from screening.",
    ),
    # --------------------------------------------------------------------------------
    PostprocessingRule(
        patterns=[
            PostprocessingPattern(lambda ent: ent.label_, "COVID-19"),
            PostprocessingPattern( has_tag, target="positive", success_value=False),
            PostprocessingPattern(F.is_modified_by_text, True, target="(setting of|s/o)"),
            PostprocessingPattern(F.ent_contains, ent={"infection", "pneumonia", "ards"},success_value=False),
        ],
        action=set_is_positive, value = False, description="Only allow 'setting of' to modify entities which have a specific clinical phrase such as 'infection'. "
        "This will disambiguate between phrases like 'Life has changed in the setting of COVID-19' vs. "
        "'Pt presents to ED in the setting of COVID-19 infection.'",
    ),
    PostprocessingRule(
        patterns=[
            PostprocessingPattern(lambda ent: ent.label_, "COVID-19"),
            PostprocessingPattern(lambda ent: ent._.is_positive, False),
            PostprocessingPattern(ent_is_sent_start, True),
            PostprocessingPattern(lambda ent: has_positive_tag(get_preceding_span(ent, 3)), True),
        ],
        action=set_is_positive, value = True, description="Bad sentence splitting sometimes splits on 'Covid' and separates a positive result, so look in the beginning of the next sentence.",
    ),
    PostprocessingRule(
        patterns=[
            PostprocessingPattern(lambda ent: ent.label_, "COVID-19"),
            PostprocessingPattern(lambda ent: ent._.is_positive, False),
            PostprocessingPattern( next_sentence_starts_with, True, target=r"(\+|pos\b|positive|detected)", max_dist=5, window=1),
        ],
        action=set_is_positive, description="Sentences often incorrectly split on '+', leading to false negatives",
    ),
    PostprocessingRule(
        patterns=[
            PostprocessingPattern(lambda ent: ent.label_, "COVID-19"),
            PostprocessingPattern( F.is_modified_by_category, True, category="test"),
            PostprocessingPattern(has_positive, False),
            (
                PostprocessingPattern( next_sentence_contains, True, target=("results? (are|is) positive")),
                PostprocessingPattern( next_sentence_contains, True, target=("results pos[^s]")),
            ),
        ],
        action=set_is_positive, description="If a test does not have any results within the same sentence, check the next sentence.",
    ),
    PostprocessingRule(
        patterns=[
            PostprocessingPattern(lambda ent: ent.label_, "COVID-19"),
            PostprocessingPattern( F.sentence_contains, True, target="admitted to covid unit"),
        ],
        action=set_is_positive, description="If a patient is admitted to the covid unit with covid, count as positive",
    ),
    # --------------------------------------------------------------------------------
    PostprocessingRule(
        patterns=[
            PostprocessingPattern(lambda ent: ent.label_, "COVID-19"),
            PostprocessingPattern(lambda ent: ent._.section_category in [ "diagnoses", "problem_list", "past_medical_history"], True),
            PostprocessingPattern( F.is_modified_by_category, True, span="TEST"), 
            PostprocessingPattern( F.is_modified_by_category, False, category="DEFINITE_POSITIVE_EXISTENCE"),
            PostprocessingPattern(has_positive_tag, success_value=False),
        ],
        action=set_is_uncertain, value=True, description="If a mention of COVID testing occurs in a positive section but doesn't have any " "additional positive modifiers, set uncertain to True. " "Example: 'Diagnoses: COVID-19 testing'"
        # TODO: Might want to modify the logic for sections so that it doesn't immediately assign is_positive to all spans.
    ),
    PostprocessingRule(
        patterns=[
            PostprocessingPattern(lambda ent: ent.label_, "COVID-19"),
            PostprocessingPattern(F.is_modified_by_category, True, category="SCREENING"),
            PostprocessingPattern(F.is_modified_by_category, True, category="TEST"),
            PostprocessingPattern(lambda ent: ent._.is_positive, True),
        ],
        action=set_is_uncertain, value = False, description="If coronavirus is modified by 'screening', 'test' and 'positive', change the certainty to certain. Example: 'Pt was screened for covid and later tested positive.'",
    ),
    PostprocessingRule(
        patterns=[
            PostprocessingPattern(lambda ent: ent.label_, "COVID-19"),
            PostprocessingPattern( F.is_modified_by_category, True, category='test'),
            PostprocessingPattern( F.is_modified_by_category, False, category="DEFINITE_POSITIVE_EXISTENCE"),
            PostprocessingPattern(has_positive_tag, success_value=False),
            (
                PostprocessingPattern( F.is_modified_by_category, True, category="ADMISSION"),
                PostprocessingPattern( F.is_modified_by_category, True, category="PATIENT_EXPERIENCER"),
            ),
        ],
        action=set_is_uncertain, description="If a patient is admitted for testing and it is not positive, set to uncertain.",
    ),
    PostprocessingRule(
        patterns=[
            PostprocessingPattern(lambda ent: ent.label_, "COVID-19"),
            PostprocessingPattern( F.is_modified_by_category, True, category="DEFINITE_POSITIVE_EXISTENCE"),
            # PostprocessingPattern(F.is_modified_by_category, condition_args=("TEST",)),
            PostprocessingPattern( F.sentence_contains, True, target= { "should", "unless", "either", "if comes back", "if returns", "if s?he tests positive"})
        ],
        action=set_is_uncertain, description="Subjunctive of test returning positive. 'Will contact patient should his covid-19 test return positive.'",
    ),
    PostprocessingRule(
        patterns=[
            PostprocessingPattern(lambda ent: ent.label_, "COVID-19"),
            (
                PostprocessingPattern( F.is_modified_by_category, True, category="DEFINITE_POSITIVE_EXISTENCE"),
                PostprocessingPattern( has_tag, target="positive", success_value=True),
            ),
            PostprocessingPattern(F.is_modified_by_text, True, target="precaution"),
        ],
        action=set_is_future, value=False, description="Differentiate 'COVID + precautions' from 'COVID precautions'",
    ),
    PostprocessingRule(
        patterns=[
            PostprocessingPattern(lambda ent: ent.label_, "COVID-19"),
            PostprocessingPattern(F.is_modified_by_text, True, target="pending"),
            PostprocessingPattern(F.sentence_contains, True, target=["retest"]),
        ],
        action=set_is_uncertain, value = False, description="If a patient has a retest pending, modify the COVID certainty to 'certain'",
    ),
    PostprocessingRule(
        patterns=[
            PostprocessingPattern(lambda ent: ent.label_, "COVID-19"),
            (
                PostprocessingPattern( F.is_modified_by_category, True, category="DEFINITE_POSITIVE_EXISTENCE"),
                PostprocessingPattern(has_positive_tag, True),
            ),
            PostprocessingPattern( F.is_modified_by_text, True, target=["sign", "symptom", "s/s"]),
            PostprocessingPattern( F.is_followed_by, True, target="with", window=3),
        ],
        action=set_is_uncertain, value=False, description="If a patient is positive for 'covid-19 with signs/symptoms', set certainty to True.",
    ),
    PostprocessingRule(
        patterns=[
            PostprocessingPattern(lambda ent: ent.label_, "COVID-19"),
            PostprocessingPattern(lambda ent: "symptom" in ent.text.lower(), True),
            PostprocessingPattern( F.is_modified_by_category, True, category="DEFINITE_POSITIVE_EXISTENCE"),
            PostprocessingPattern( F.is_modified_by_text, True, target="test"),
        ],
        action=set_is_uncertain, value = False, description="Set certainty to True for phrases like 'COVID-19 symptoms and positive test'.",
    ),
    # --------------------------------------------------------------------------------
    PostprocessingRule(
        patterns=[
            PostprocessingPattern(lambda ent: ent.label_, "COVID-19"),
            PostprocessingPattern( F.is_modified_by_category, True, category="NEGATED_EXISTENCE"),
            PostprocessingPattern( F.is_modified_by_text, True, target="pending"),
        ],
        action=F.set_negated, value = False, description="If a coronavirus entity is negated but also has 'pending' in the sentence, set is_negated to False. It should be uncertain.",
    ),
    PostprocessingRule(
        patterns=[
            PostprocessingPattern(lambda ent: ent.label_, "COVID-19"),
            PostprocessingPattern(F.is_modified_by_category, True, category="NEGATED_EXISTENCE",),
            PostprocessingPattern(has_positive, True),
            PostprocessingPattern( F.sentence_contains, True, target=["re[ -]?test", "second test", "repeat"]),
        ],
        action=F.set_negated, value = False, description="If COVID-19 is positive but a repeat is negative, consider it positive and set is_negated to False.",
    ),
    PostprocessingRule(
        patterns=[
            PostprocessingPattern(lambda ent: ent.label_, "COVID-19"),
            PostprocessingPattern(F.is_modified_by_category, True, category ="SPECIFIED_STRAIN"),
        ],
        action=F.set_label, span_group_name="specified coronavirus", description="Example: Tested for positive coronavirus benign, not the novel strain.",
    ),
    PostprocessingRule(
        patterns=[
            PostprocessingPattern(lambda ent: ent.label_, "COVID-19"),
            PostprocessingPattern( F.is_modified_by_category, True, category="SCREENING"),
            PostprocessingPattern( F.is_modified_by_category, False, category ="TEST"),
            PostprocessingPattern(lambda ent: ent._.is_positive, True),  
            # If the positive modifier is actually part of the entity, then fail
            PostprocessingPattern( has_tag, False, target="positive"),
            PostprocessingPattern( has_tag, False, target="associated_diagnosis"), 
        ],
        action=F.set_label, span_group_name="positive coronavirus screening", description="If coronavirus is modified by both 'screening' and 'positive', change the label to 'POSITIVE CORONAVIRUS SCREENING'.",
    ),
]
