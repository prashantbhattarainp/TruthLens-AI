"""Configurable multilingual text preparation for Phase 4.4 research.

This module is intentionally not imported by :mod:`preprocessing.__init__` or
the packaged inference path.  The immutable English model continues to use
``PreprocessingPipeline`` unchanged.  These utilities provide a transparent,
dependency-free language-processing layer for bounded multilingual audits and
future research datasets.
"""

from __future__ import annotations

import hashlib
import re
import unicodedata
from dataclasses import dataclass
from typing import Literal


LanguageCode = Literal["english", "hindi", "hinglish"]

DEVANAGARI_PATTERN = re.compile(r"[\u0900-\u097F]")
LATIN_WORD_PATTERN = re.compile(r"[A-Za-z]+")
TOKEN_PATTERN = re.compile(r"[A-Za-z]+|[\u0900-\u097F]+")
URL_PATTERN = re.compile(r"(?i)\b(?:https?://|www\.)[^\s<>\"']+")
EMAIL_PATTERN = re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b")
HTML_TAG_PATTERN = re.compile(r"<[^>]+>")
WHITESPACE_PATTERN = re.compile(r"\s+")
ZERO_WIDTH_CHARACTERS = "\u200b\u200c\u200d\ufeff"

# A deliberately small, high-signal marker list.  Two distinct markers are
# required so the detector is conservative on English content, including
# political references such as the uppercase AAP party name.
HINGLISH_MARKERS = frozenset(
    {
        "aap",
        "aaj",
        "abhi",
        "agar",
        "apna",
        "apne",
        "aur",
        "bahut",
        "bhi",
        "daava",
        "daave",
        "dekho",
        "ek",
        "gaya",
        "gayi",
        "hai",
        "hain",
        "haan",
        "hoga",
        "hoon",
        "hum",
        "ka",
        "karna",
        "karo",
        "ki",
        "ko",
        "kya",
        "kyun",
        "lekin",
        "mein",
        "mera",
        "meri",
        "nahi",
        "nahin",
        "ne",
        "par",
        "phir",
        "tha",
        "thi",
        "toh",
        "ye",
        "yeh",
        "zaroori",
    }
)

# Normalization only consolidates common Roman-Hindi spelling variants.  It
# never translates text or asserts that a Roman token has one unique meaning.
HINGLISH_NORMALIZATION = {
    "haii": "hai",
    "haanji": "haan",
    "kyo": "kyun",
    "kyu": "kyun",
    "nai": "nahin",
    "nahi": "nahin",
    "nhi": "nahin",
}


@dataclass(frozen=True)
class MultilingualPreprocessingConfig:
    """Settings for the research-only multilingual preparation layer."""

    pipeline_version: str = "P44-multilingual-preprocessing-v1"
    unicode_normalization_form: str = "NFC"
    remove_urls: bool = True
    remove_emails: bool = True
    remove_html_tags: bool = True
    remove_zero_width_characters: bool = True
    lowercase_latin: bool = True
    normalize_hinglish: bool = True
    min_distinct_hinglish_markers: int = 2

    def __post_init__(self) -> None:
        if self.unicode_normalization_form not in {"NFC", "NFD", "NFKC", "NFKD"}:
            raise ValueError("unicode_normalization_form must be a Unicode normalization form")
        if self.min_distinct_hinglish_markers < 1:
            raise ValueError("min_distinct_hinglish_markers must be positive")


@dataclass(frozen=True)
class MultilingualDocument:
    """In-memory result that exposes language processing without model output."""

    document_id: str
    source_text_sha256: str
    language: LanguageCode
    language_evidence: str
    normalized_text: str
    tokens: tuple[str, ...]
    hinglish_normalization_count: int


class MultilingualPreprocessor:
    """Unicode-aware, conservative English/Hindi/Hinglish preparation.

    Detection is a transparent heuristic, not a language-identification model.
    Devanagari-bearing text is classed as Hindi; Roman text requires two
    distinct Hindi markers to be classed as Hinglish; all other text is
    treated as English for this three-language audit.  Additional languages
    can be added by extending the detector and tokenizer behind this class.
    """

    def __init__(self, configuration: MultilingualPreprocessingConfig | None = None) -> None:
        self.configuration = configuration or MultilingualPreprocessingConfig()

    def process_document(self, *, document_id: str, text: str) -> MultilingualDocument:
        """Clean and tokenise one in-memory document without retaining it elsewhere."""

        cleaned = self._clean(text)
        language, evidence = self.detect_language(cleaned)
        tokens = list(TOKEN_PATTERN.findall(cleaned))
        normalization_count = 0
        processed_tokens: list[str] = []
        for token in tokens:
            value = token.lower() if self.configuration.lowercase_latin and LATIN_WORD_PATTERN.fullmatch(token) else token
            if language == "hinglish" and self.configuration.normalize_hinglish:
                normalized = HINGLISH_NORMALIZATION.get(value, value)
                normalization_count += int(normalized != value)
                value = normalized
            processed_tokens.append(value)
        return MultilingualDocument(
            document_id=document_id,
            source_text_sha256=hashlib.sha256(text.encode("utf-8")).hexdigest(),
            language=language,
            language_evidence=evidence,
            normalized_text=" ".join(processed_tokens),
            tokens=tuple(processed_tokens),
            hinglish_normalization_count=normalization_count,
        )

    def detect_language(self, text: str) -> tuple[LanguageCode, str]:
        """Return a language class and auditable heuristic evidence."""

        devanagari_count = len(DEVANAGARI_PATTERN.findall(text))
        if devanagari_count:
            return "hindi", f"Devanagari characters detected: {devanagari_count}"

        markers = self._roman_hindi_markers(text)
        if len(markers) >= self.configuration.min_distinct_hinglish_markers:
            return "hinglish", f"Distinct Roman-Hindi markers: {','.join(sorted(markers))}"
        return "english", "No Devanagari script and insufficient Roman-Hindi marker evidence"

    def _clean(self, text: str) -> str:
        value = unicodedata.normalize(self.configuration.unicode_normalization_form, text)
        if self.configuration.remove_html_tags:
            value = HTML_TAG_PATTERN.sub(" ", value)
        if self.configuration.remove_urls:
            value = URL_PATTERN.sub(" ", value)
        if self.configuration.remove_emails:
            value = EMAIL_PATTERN.sub(" ", value)
        if self.configuration.remove_zero_width_characters:
            value = value.translate({ord(character): None for character in ZERO_WIDTH_CHARACTERS})
        return WHITESPACE_PATTERN.sub(" ", value).strip()

    def _roman_hindi_markers(self, text: str) -> set[str]:
        markers: set[str] = set()
        for token in LATIN_WORD_PATTERN.findall(text):
            # Treat fully uppercase words as named entities/acronyms, avoiding
            # a common AAP-party false Hinglish signal in political content.
            if token.isupper():
                continue
            folded = token.casefold()
            canonical = HINGLISH_NORMALIZATION.get(folded, folded)
            if canonical in HINGLISH_MARKERS:
                markers.add(canonical)
        return markers
