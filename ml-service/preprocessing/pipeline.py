"""Request-time implementation of the frozen preprocessing policy."""

from __future__ import annotations

import hashlib
import re
import unicodedata
from html.parser import HTMLParser

import spacy

from .config import HandlingSetting, PreprocessingConfig
from .models import InputDocument, ProcessedDocument


URL_PATTERN = re.compile(r'(?i)\b(?:https?://|www\.)[^\s<>"\']+')
EMAIL_PATTERN = re.compile(r'(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b')
WHITESPACE_PATTERN = re.compile(r'\s+')
NUMBER_PATTERN = re.compile(r'\d+')
NEGATIONS = frozenset({'no', 'not', 'nor', 'never', 'none', 'neither', 'cannot', "can't", "won't", "isn't", "wasn't", "don't", "doesn't", "didn't"})


class _HtmlTextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)

    def text(self) -> str:
        return ' '.join(self.parts)


class PreprocessingPipeline:
    """Transforms one in-memory document without logging or retaining its contents."""

    def __init__(self, configuration: PreprocessingConfig) -> None:
        self.configuration = configuration
        self._nlp = self._load_spacy()

    def process_document(self, document: InputDocument) -> ProcessedDocument:
        text = document.text
        if self.configuration.unicode_normalization.enabled:
            text = unicodedata.normalize(self.configuration.unicode_normalization.form, text)
        if self.configuration.html_removal.enabled:
            parser = _HtmlTextExtractor()
            parser.feed(text)
            parser.close()
            text = parser.text()
        if self.configuration.url_removal.enabled:
            text = URL_PATTERN.sub('', text)
        if self.configuration.email_removal.enabled:
            text = EMAIL_PATTERN.sub('', text)
        if self.configuration.lowercasing.enabled:
            text = text.lower()
        text = self._apply_handling(text, self.configuration.special_character_handling, self._is_special)
        text = self._apply_handling(text, self.configuration.number_handling, str.isdigit, NUMBER_PATTERN)
        text = self._apply_handling(text, self.configuration.punctuation_handling, self._is_punctuation)
        if self.configuration.whitespace_normalization.enabled:
            text = WHITESPACE_PATTERN.sub(' ', text).strip()

        if self.configuration.tokenization.enabled:
            tokens = self._tokenize(text)
            processed_text = ' '.join(tokens)
        else:
            processed_text = text
            tokens = tuple(text.split())
        return ProcessedDocument(
            document_id=document.document_id,
            source_text_sha256=hashlib.sha256(document.text.encode('utf-8')).hexdigest(),
            processed_text=processed_text,
            tokens=tokens,
        )

    def _load_spacy(self):
        try:
            return spacy.load(self.configuration.spacy.model_name)
        except OSError:
            if not self.configuration.spacy.allow_blank_fallback:
                raise
            return spacy.blank(self.configuration.language)

    def _tokenize(self, text: str) -> tuple[str, ...]:
        doc = self._nlp(text)
        tokens: list[str] = []
        for token in doc:
            value = token.lemma_ if self.configuration.lemmatization.enabled and token.lemma_ else token.text
            if self.configuration.stopword_removal.enabled and token.is_stop:
                if not self.configuration.stopword_removal.preserve_negations or value.lower() not in NEGATIONS:
                    continue
            if value:
                tokens.append(value)
        return tuple(tokens)

    @staticmethod
    def _apply_handling(
        text: str,
        setting: HandlingSetting,
        predicate,
        pattern: re.Pattern[str] | None = None,
    ) -> str:
        if not setting.enabled or setting.mode == 'preserve':
            return text
        if pattern is not None:
            replacement = '' if setting.mode == 'remove' else ' '
            return pattern.sub(replacement, text)
        replacement = '' if setting.mode == 'remove' else ' '
        return ''.join(replacement if predicate(character) else character for character in text)

    @staticmethod
    def _is_special(character: str) -> bool:
        return not character.isalnum() and not character.isspace() and not PreprocessingPipeline._is_punctuation(character)

    @staticmethod
    def _is_punctuation(character: str) -> bool:
        return unicodedata.category(character).startswith('P')
