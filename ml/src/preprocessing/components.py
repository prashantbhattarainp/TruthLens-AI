"""Independent text and token preprocessing components."""

from __future__ import annotations

import re
import unicodedata
from html.parser import HTMLParser
from typing import Callable, Protocol

from spacy.tokens import Doc, Token

from preprocessing.config import HandlingSetting, NEGATIONS, PreprocessingConfig
from preprocessing.exceptions import ModelCapabilityError


URL_PATTERN = re.compile(r"(?i)\b(?:https?://|www\.)[^\s<>\"']+")
EMAIL_PATTERN = re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b")
WHITESPACE_PATTERN = re.compile(r"\s+")
NUMBER_PATTERN = re.compile(r"\d+")


class TextTransform(Protocol):
    """One deterministic operation on a source text string."""

    name: str

    def apply(self, text: str) -> str:
        """Apply the transform without accessing records or external state."""


class _HtmlTextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self._parts.append(data)

    def handle_starttag(self, tag: str, _attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() in {"br", "div", "li", "p", "section"}:
            self._parts.append(" ")

    @property
    def text(self) -> str:
        return "".join(self._parts)


class UnicodeNormalizer:
    name = "unicode_normalization"

    def __init__(self, form: str) -> None:
        self._form = form

    def apply(self, text: str) -> str:
        return unicodedata.normalize(self._form, text)


class HtmlRemover:
    name = "html_removal"

    def apply(self, text: str) -> str:
        parser = _HtmlTextExtractor()
        parser.feed(text)
        parser.close()
        return parser.text


class UrlRemover:
    name = "url_removal"

    def apply(self, text: str) -> str:
        return URL_PATTERN.sub(" ", text)


class EmailRemover:
    name = "email_removal"

    def apply(self, text: str) -> str:
        return EMAIL_PATTERN.sub(" ", text)


class WhitespaceNormalizer:
    name = "whitespace_normalization"

    def apply(self, text: str) -> str:
        return WHITESPACE_PATTERN.sub(" ", text).strip()


class Lowercaser:
    name = "lowercasing"

    def apply(self, text: str) -> str:
        return text.lower()


class SpecialCharacterHandler:
    name = "special_character_handling"

    def __init__(self, setting: HandlingSetting) -> None:
        self._setting = setting

    def apply(self, text: str) -> str:
        return _apply_character_mode(text, self._setting.mode, _is_special_character, " specialtoken ")


class NumberHandler:
    name = "number_handling"

    def __init__(self, setting: HandlingSetting) -> None:
        self._setting = setting

    def apply(self, text: str) -> str:
        if self._setting.mode == "preserve":
            return text
        if self._setting.mode == "remove":
            return NUMBER_PATTERN.sub("", text)
        if self._setting.mode == "replace_with_space":
            return NUMBER_PATTERN.sub(" ", text)
        return NUMBER_PATTERN.sub(" numbertoken ", text)


class PunctuationHandler:
    name = "punctuation_handling"

    def __init__(self, setting: HandlingSetting) -> None:
        self._setting = setting

    def apply(self, text: str) -> str:
        return _apply_character_mode(text, self._setting.mode, _is_punctuation, " punctuationtoken ")


class SpacyTokenProcessor:
    """spaCy-backed tokenizer plus independently configurable token filters."""

    def __init__(self, config: PreprocessingConfig, has_lemmatizer: bool) -> None:
        self._config = config
        if config.lemmatization.enabled and not has_lemmatizer:
            raise ModelCapabilityError(
                "Lemmatization is enabled, but the selected spaCy pipeline has no lemmatizer. "
                "Install the configured language model or disable lemmatization."
            )

    def process(self, doc: Doc) -> tuple[str, ...]:
        tokens: list[str] = []
        for token in doc:
            if self._include_token(token):
                tokens.append(self._render_token(token))
        return tuple(tokens)

    def _include_token(self, token: Token) -> bool:
        if token.is_space:
            return False
        if not self._config.stopword_removal.enabled:
            return True
        if self._config.stopword_removal.preserve_negations and token.lower_ in NEGATIONS:
            return True
        return not token.is_stop

    def _render_token(self, token: Token) -> str:
        if not self._config.lemmatization.enabled:
            return token.text
        lemma = token.lemma_.strip()
        if not lemma:
            raise ModelCapabilityError("spaCy returned an empty lemma for a retained token.")
        return lemma


def build_text_transforms(config: PreprocessingConfig) -> tuple[TextTransform, ...]:
    """Construct only the independent operations enabled by a configuration."""
    transforms: list[TextTransform] = []
    if config.unicode_normalization.enabled:
        transforms.append(UnicodeNormalizer(config.unicode_normalization.form))
    if config.html_removal.enabled:
        transforms.append(HtmlRemover())
    if config.url_removal.enabled:
        transforms.append(UrlRemover())
    if config.email_removal.enabled:
        transforms.append(EmailRemover())
    if config.special_character_handling.enabled:
        transforms.append(SpecialCharacterHandler(config.special_character_handling))
    if config.number_handling.enabled:
        transforms.append(NumberHandler(config.number_handling))
    if config.punctuation_handling.enabled:
        transforms.append(PunctuationHandler(config.punctuation_handling))
    if config.whitespace_normalization.enabled:
        transforms.append(WhitespaceNormalizer())
    if config.lowercasing.enabled:
        transforms.append(Lowercaser())
    return tuple(transforms)


def _apply_character_mode(
    text: str,
    mode: str,
    predicate: Callable[[str], bool],
    replacement_token: str,
) -> str:
    if mode == "preserve":
        return text
    if mode == "remove":
        return "".join(character for character in text if not predicate(character))
    if mode == "replace_with_space":
        return "".join(" " if predicate(character) else character for character in text)
    return "".join(replacement_token if predicate(character) else character for character in text)


def _is_special_character(character: str) -> bool:
    return unicodedata.category(character).startswith("S")


def _is_punctuation(character: str) -> bool:
    return unicodedata.category(character).startswith("P")
