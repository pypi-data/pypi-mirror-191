"""
Pipeline transformer for scikit-learn to clean text
"""

from typing import Any, List, Union
import re, sys, logging
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from unicodedata import category, normalize
from emoji import UNICODE_EMOJI, demojize, emojize
from ftfy import fix_text
from spellchecker import SpellChecker
from tknlp.contribute import constants as C
from operator import attrgetter

log = logging.getLogger()

# add new languages here
specials = {
    "de": {
        "case_insensitive": [["ä", "ae"], ["ü", "ue"], ["ö", "oe"]],
        "case_sensitive": [["ß", "ss"]],
    }
}
escape_sequence = "xxxxx"


def norm(text):
    return normalize("NFC", text)

def remove_substrings(text, to_replace, replace_with=""):
    """
    Remove (or replace) substrings from a text.
    Args:
        text (str): raw text to preprocess
        to_replace (iterable or str): substrings to remove/replace
        replace_with (str): defaults to an empty string but
            you replace substrings with a token.
    """
    if isinstance(to_replace, str):
        to_replace = [to_replace]

    result = text
    for x in to_replace:
        result = result.replace(x, replace_with)
    return result

def save_replace(text, lang, back=False):
    # perserve the casing of the original text
    # TODO: performance of matching

    # normalize the text to make sure to really match all occurences
    text = norm(text)

    possibilities = (
        specials[lang]["case_sensitive"]
        + [[norm(x[0]), x[1]] for x in specials[lang]["case_insensitive"]]
        + [
            [norm(x[0].upper()), x[1].upper()]
            for x in specials[lang]["case_insensitive"]
        ]
    )
    for pattern, target in possibilities:
        if back:
            text = text.replace(escape_sequence + target + escape_sequence, pattern)
        else:
            text = text.replace(pattern, escape_sequence + target + escape_sequence)
    return text


class CleanTransformer(TransformerMixin, BaseEstimator):
    """
    Scikit-learn equivalent of :term:`clean` function.
    """

    def __init__( self, 
        fix_unicode=True,
        to_ascii=True,
        lower=True,
        normalize_whitespace=True,
        no_line_breaks=False,
        strip_lines=True,
        keep_two_line_breaks=False,
        no_urls=False,
        no_emails=False,
        no_phone_numbers=False,
        no_numbers=False,
        no_digits=False,
        no_user=False,
        no_repeat=False,
        no_currency_symbols=False,
        no_punct=False,
        no_emoji=False,
        replace_with_url="<URL>",
        replace_with_email="<EMAIL>",
        replace_with_phone_number="<PHONE>",
        replace_with_number="<NUMBER>",
        replace_with_digit="0",
        replace_with_currency_symbol="<CUR>",
        replace_with_punct="",
        replace_with_user="<USER>",
        lang="en",
        markdown=False
    ):
        """
        All parameters are same as the :term:`clean` function.
        """
        self.fix_unicode = fix_unicode
        self.to_ascii = to_ascii
        self.lower = lower
        self.normalize_whitespace = normalize_whitespace
        self.no_line_breaks = no_line_breaks
        self.strip_lines = strip_lines
        self.keep_two_line_breaks = keep_two_line_breaks
        self.no_urls = no_urls
        self.no_emails = no_emails
        self.no_phone_numbers = no_phone_numbers
        self.no_numbers = no_numbers
        self.no_digits = no_digits
        self.no_currency_symbols = no_currency_symbols
        self.no_punct = no_punct
        self.no_emoji = no_emoji
        self.no_user = no_user
        self.no_repeat = no_repeat
        self.replace_with_url = replace_with_url
        self.replace_with_email = replace_with_email
        self.replace_with_phone_number = replace_with_phone_number
        self.replace_with_number = replace_with_number
        self.replace_with_digit = replace_with_digit
        self.replace_with_currency_symbol = replace_with_currency_symbol
        self.replace_with_punct = replace_with_punct
        self.replace_with_user = replace_with_user
        self.lang = lang
        self.markdown = markdown

    @property
    def special_token(self):
        return attrgetter(*[x for x in self.__dict__ if x.startswith('replace')])(self)

    def fit(self, X: Any):
        """
        This method is defined for compatibility. It does nothing.
        """
        return self

    def transform(self, X: Union[List[str], pd.Series]) -> Union[List[str], pd.Series]:
        """
        Normalize various aspects of each item in raw text array-like.
        Args:
            X (array-like): an array-like of strings. It could be a list or a Pandas Series.
        Returns:
            array-like[str]: an array-like with the same type as ``X``
                             and with the processed items of ``X`` as content.
        """
        if not (isinstance(X, list) or isinstance(X, pd.Series)):
            raise ValueError("The input must be a list or pd.Series")
        if isinstance(X, pd.Series):
            return X.apply(lambda text: clean(text, **self.get_params()))
        else:
            return list(map(lambda text: clean(text, **self.get_params()), X))


# fall back to `unicodedata`
try:
    from unidecode import unidecode

except ImportError:
    from unicodedata import normalize

    unidecode = lambda x: normalize("NFD", x).encode("ASCII", "ignore").decode("utf-8")
    log.warning(
        "Since the GPL-licensed package `unidecode` is not installed, using Python's `unicodedata` package which yields worse results."
    )


def fix_strange_quotes(text):
    """
    Replace strange quotes, i.e., 〞with a single quote ' or a double quote " if it fits better.
    """
    text = C.SINGLE_QUOTE_REGEX.sub("'", text)
    text = C.DOUBLE_QUOTE_REGEX.sub('"', text)
    return text


def fix_bad_unicode(text, normalization="NFC"):
    """
    Fix unicode text that's "broken" using `ftfy <http://ftfy.readthedocs.org/>`_;
    this includes mojibake, HTML entities and other code cruft,
    and non-standard forms for display purposes.
    Args:
        text (str): raw text
        normalization ({'NFC', 'NFKC', 'NFD', 'NFKD'}): if 'NFC',
            combines characters and diacritics written using separate code points,
            e.g. converting "e" plus an acute accent modifier into "é"; unicode
            can be converted to NFC form without any change in its meaning!
            if 'NFKC', additional normalizations are applied that can change
            the meanings of characters, e.g. ellipsis characters will be replaced
            with three periods
    """
    # trying to fix backslash-replaced strings (via https://stackoverflow.com/a/57192592/4028896)
    try:
        text = text.encode("latin", "backslashreplace").decode("unicode-escape")
    except:
        pass

    return fix_text(text, normalization=normalization)


def to_ascii_unicode(text, lang="en", no_emoji=False):
    """
    Try to represent unicode data in ascii characters similar to what a human
    with a US keyboard would choose.
    Works great for languages of Western origin, worse the farther the language
    gets from Latin-based alphabets. It's based on hand-tuned character mappings
    that also contain ascii approximations for symbols and non-Latin alphabets.
    """
    # normalize quotes before since this improves transliteration quality
    text = fix_strange_quotes(text)

    if not no_emoji:
        text = demojize(text, use_aliases=True)

    lang = lang.lower()
    # special handling for German text to preserve umlauts
    if lang == "de":
        text = save_replace(text, lang=lang)

    text = unidecode(text)

    # important to remove utility characters
    if lang == "de":
        text = save_replace(text, lang=lang, back=True)

    if not no_emoji:
        text = emojize(text, use_aliases=True)

    return text


def normalize_whitespace(
    text, no_line_breaks=False, strip_lines=True, keep_two_line_breaks=False
):
    """
    Given ``text`` str, replace one or more spacings with a single space, and one
    or more line breaks with a single newline. Also strip leading/trailing whitespace.
    """
    if strip_lines:
        text = "\n".join([x.strip() for x in text.splitlines()])

    if no_line_breaks:
        text = C.MULTI_WHITESPACE_TO_ONE_REGEX.sub(" ", text)
    else:
        if keep_two_line_breaks:
            text = C.NONBREAKING_SPACE_REGEX.sub(
                " ", C.TWO_LINEBREAK_REGEX.sub(r"\n\n", text)
            )
        else:
            text = C.NONBREAKING_SPACE_REGEX.sub(
                " ", C.LINEBREAK_REGEX.sub(r"\n", text)
            )

    return text.strip()


# used below to keep `normalize_whitespace` as a parameter in `clean`
def _normalize_whitespace(*kwargs):
    return normalize_whitespace(*kwargs)


def replace_urls(text, replace_with="<URL>", markdown=False):
    """
    Replace all URLs in ``text`` str with ``replace_with`` str.
    """
    if markdown: 
        URL_REGEX = re.compile(r'(?:\[(?P<text>.*?)\])\((?P<link>.*?)\)', flags=C.URL_REGEX.flags)
        return URL_REGEX.sub(replace_with, text)
    return C.URL_REGEX.sub(replace_with, text)


def replace_emails(text, replace_with="<EMAIL>"):
    """
    Replace all emails in ``text`` str with ``replace_with`` str.
    """
    return C.EMAIL_REGEX.sub(replace_with, text)


def replace_phone_numbers(text, replace_with="<PHONE>"):
    """
    Replace all phone numbers in ``text`` str with ``replace_with`` str.
    """
    return C.PHONE_REGEX.sub(replace_with, text)


def replace_numbers(text, replace_with="<NUMBER>"):
    """
    Replace all numbers in ``text`` str with ``replace_with`` str.
    """
    return C.NUMBERS_REGEX.sub(replace_with, text)


def replace_digits(text, replace_with="0"):
    """
    Replace all digits in ``text`` str with ``replace_with`` str, i.e., 123.34 to 000.00
    """
    return re.sub(r"\d", replace_with, text)
    
def replace_users(text, replace_with="<USER>"):
    """
    Replace all @usr in ``text`` str with ``replace_with`` str, i.e., @duffman911
    """
    return re.sub(r'@[^\s]+', replace_with, text)


def replace_currency_symbols(text, replace_with="<CUR>"):
    """
    Replace all currency symbols in ``text`` str with string specified by ``replace_with`` str.
    Args:
        text (str): raw text
        replace_with (str): if None (default), replace symbols with
            their standard 3-letter abbreviations (e.g. '$' with 'USD', '£' with 'GBP');
            otherwise, pass in a string with which to replace all symbols
            (e.g. "*CURRENCY*")
    """
    if replace_with is None:
        for k, v in C.CURRENCIES.items():
            text = text.replace(k, v)
        return text
    else:
        return C.CURRENCY_REGEX.sub(replace_with, text)


def replace_punct(text, replace_with=" "):
    """
    Replace punctuations from ``text`` with whitespaces (or other tokens).
    """
    return text.translate(
        dict.fromkeys(
            (i for i in range(sys.maxunicode) if category(chr(i)).startswith("P")),
            replace_with,
        )
    )


def remove_punct(text):
    """
    Remove punctuations from ``text``.
    """
    return text.translate(C.PUNCT_TRANSLATE_UNICODE)


def remove_emoji(text):
    return remove_substrings(text, UNICODE_EMOJI["en"])

def remove_repeat(text):
    """Reduces repeated consecutive characters from given tweet to only two."""
    return re.sub(r'(.)\1+', r'\1\1', text)


def clean(
    text,
    fix_unicode=True,
    to_ascii=True,
    lower=True,
    normalize_whitespace=True,
    no_line_breaks=False,
    strip_lines=True,
    keep_two_line_breaks=False,
    no_urls=False,
    no_emails=False,
    no_phone_numbers=False,
    no_numbers=False,
    no_digits=False,
    no_user=False,
    no_repeat=False,
    no_currency_symbols=False,
    no_punct=False,
    no_emoji=False,
    replace_with_url="<URL>",
    replace_with_email="<EMAIL>",
    replace_with_phone_number="<PHONE>",
    replace_with_number="<NUMBER>",
    replace_with_digit="0",
    replace_with_currency_symbol="<CUR>",
    replace_with_punct="",
    replace_with_user="<USER>",
    lang="en",
    markdown=False
):
    """
    Normalize various aspects of a raw text. A convenience function for applying all other preprocessing functions in one go.
    Args:
        text (str): raw text to preprocess
        fix_unicode (bool): if True, fix "broken" unicode such as
            mojibake and garbled HTML entities
        to_ascii (bool): if True, convert non-to_ascii characters
            into their closest to_ascii equivalents
        lower (bool): if True, all text is lower-cased
        no_line_breaks (bool): if True, strip line breaks from text
        no_urls (bool): if True, replace all URL strings with a special URL token
        no_emails (bool): if True, replace all email strings with a special EMAIL token
        no_phone_numbers (bool): if True, replace all phone number strings
            with a special PHONE token
        no_numbers (bool): if True, replace all number-like strings
            with a special NUMBER token
        no_digits (bool): if True, replace all digits with a special DIGIT token
        no_currency_symbols (bool): if True, replace all currency symbols
            with a special CURRENCY token
        no_punct (bool): if True, remove all punctuation (replace with
            empty string)
        replace_with_url (str): special URL token, default "<URL>",
        replace_with_email (str): special EMAIL token, default "<EMAIL>",
        replace_with_phone_number (str): special PHONE token, default "<PHONE>",
        replace_with_number (str): special NUMBER token, default "<NUMBER>",
        replace_with_digit (str): special DIGIT token, default "0",
        replace_with_currency_symbol (str): special CURRENCY token, default "<CUR>",
        replace_with_punct (str): replace punctuations with this token, default "",
        lang (str): special language-depended preprocessing. Besides the default English ('en'), only German ('de') is supported

    Returns:
        str: input ``text`` processed according to function args
    """

    if text is None:
        return ""

    text = str(text)

    if fix_unicode:
        text = fix_bad_unicode(text)
    if no_currency_symbols:
        text = replace_currency_symbols(text, replace_with_currency_symbol)
    if to_ascii:
        text = to_ascii_unicode(text, lang=lang, no_emoji=no_emoji)
    if no_urls:
        text = replace_urls(text, replace_with_url, markdown)
    if no_emails:
        text = replace_emails(text, replace_with_email)
    if no_phone_numbers:
        text = replace_phone_numbers(text, replace_with_phone_number)
    if no_numbers:
        text = replace_numbers(text, replace_with_number)
    if no_digits:
        text = replace_digits(text, replace_with_digit)
    if no_user:
        text = replace_users(text, replace_with_user)
    if no_punct:
        if replace_with_punct == "":
            text = remove_punct(text)
        else:
            text = replace_punct(text, replace_with_punct)

    if no_emoji and not to_ascii:
        text = remove_emoji(text)
    if lower:
        text = text.lower()
    if no_repeat:
        text = remove_repeat(text)

    if normalize_whitespace:
        text = _normalize_whitespace(
            text, no_line_breaks, strip_lines, keep_two_line_breaks
        )

    return text
