"""Deterministic, documented text stressors for the Phase 4.5 audit.

The functions intentionally do not claim semantic equivalence. Their output is
used only for aggregate robustness diagnostics against the frozen validation
partition and is never written into tracked artifacts.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Callable


URL_PATTERN = re.compile(r'(?i)\b(?:https?://|www\.)[^\s<>"\']+')
WORD_BOUNDARY = lambda word: re.compile(rf"(?i)\b{re.escape(word)}\b")


@dataclass(frozen=True)
class Perturbation:
    """One deterministic input stressor with explicit interpretation limits."""

    key: str
    display_name: str
    transform: Callable[[str], tuple[str, bool]]
    interpretation: str
    label_preservation: str


def _replace_words(text: str, replacements: dict[str, str]) -> tuple[str, bool]:
    changed = False
    value = text
    for source, target in replacements.items():
        value, count = WORD_BOUNDARY(source).subn(target, value)
        changed = changed or bool(count)
    return value, changed


def _typos(text: str) -> tuple[str, bool]:
    return _replace_words(
        text,
        {
            "government": "goverment",
            "health": "healt",
            "minister": "minster",
            "news": "nwes",
            "vaccine": "vacine",
            "election": "electon",
        },
    )


def _extra_punctuation(text: str) -> tuple[str, bool]:
    return (f"{text} !!! ???" if text else text, bool(text))


def _capitalization(text: str) -> tuple[str, bool]:
    value = text.swapcase()
    return value, value != text


def _emoji(text: str) -> tuple[str, bool]:
    return (f"{text} 🔎" if text else text, bool(text))


def _remove_urls(text: str) -> tuple[str, bool]:
    value, count = URL_PATTERN.subn(" ", text)
    return value, bool(count)


STOP_WORDS = frozenset({"a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "in", "is", "it", "of", "on", "or", "that", "the", "to", "with"})


def _stop_word_variation(text: str) -> tuple[str, bool]:
    tokens = re.findall(r"\S+", text)
    kept = [token for token in tokens if token.casefold().strip(".,;:!?()[]{}\"'") not in STOP_WORDS]
    value = " ".join(kept)
    return value, value != text


def _synonyms(text: str) -> tuple[str, bool]:
    return _replace_words(
        text,
        {
            "fake": "false",
            "claim": "assertion",
            "government": "administration",
            "said": "stated",
            "news": "report",
            "video": "clip",
        },
    )


def _light_paraphrase(text: str) -> tuple[str, bool]:
    return _replace_words(
        text,
        {
            "according to": "reports say",
            "has said": "stated",
            "is fake": "is false",
            "was fake": "was false",
            "social media": "online platforms",
        },
    )


def _shorten(text: str) -> tuple[str, bool]:
    value = text[:140].rstrip()
    return value, value != text


def _expand(text: str) -> tuple[str, bool]:
    suffix = " Additional context is available in the report."
    return (f"{text}{suffix}" if text else text, bool(text))


def perturbations() -> tuple[Perturbation, ...]:
    """Return the fixed, ordered Phase 4.5 perturbation set."""

    return (
        Perturbation("typos", "Typographical errors", _typos, "Common deterministic misspellings.", "mechanical text corruption"),
        Perturbation("punctuation", "Extra punctuation", _extra_punctuation, "Appends punctuation emphasis.", "mechanical punctuation change"),
        Perturbation("capitalization", "Capitalization changes", _capitalization, "Swaps letter case without editing terms.", "mechanical casing change"),
        Perturbation("emoji", "Emoji insertion", _emoji, "Appends one neutral inspection emoji.", "mechanical insertion"),
        Perturbation("url_removal", "URL removal", _remove_urls, "Removes literal URL spans when present.", "mechanical deletion; may have zero coverage"),
        Perturbation("stop_words", "Stop-word variation", _stop_word_variation, "Removes a fixed English function-word list.", "synthetic contraction; semantic equivalence not guaranteed"),
        Perturbation("synonyms", "Synonym replacement", _synonyms, "Uses a small fixed lexical replacement map.", "synthetic lexical approximation; semantic equivalence not guaranteed"),
        Perturbation("paraphrase", "Light headline paraphrase", _light_paraphrase, "Rewrites a few fixed headline-like phrases.", "synthetic lexical approximation; semantic equivalence not guaranteed"),
        Perturbation("shortened", "Shortened headline", _shorten, "Truncates input at 140 characters.", "information-removing stressor; original label may not fully apply"),
        Perturbation("expanded", "Expanded headline", _expand, "Appends a neutral context sentence.", "synthetic expansion; semantic equivalence not guaranteed"),
    )
