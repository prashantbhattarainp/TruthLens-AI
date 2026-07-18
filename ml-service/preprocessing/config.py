"""Strict reader for the immutable preprocessing configuration packaged with a model."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class EnabledSetting:
    enabled: bool


@dataclass(frozen=True)
class UnicodeNormalizationSetting(EnabledSetting):
    form: str = 'NFC'


@dataclass(frozen=True)
class HandlingSetting(EnabledSetting):
    mode: str = 'preserve'


@dataclass(frozen=True)
class StopwordSetting(EnabledSetting):
    preserve_negations: bool = True


@dataclass(frozen=True)
class SpacySetting:
    model_name: str
    allow_blank_fallback: bool
    batch_size: int


@dataclass(frozen=True)
class ValidationSetting:
    max_empty_document_rate: float
    max_failures: int


@dataclass(frozen=True)
class PreprocessingConfig:
    pipeline_version: str
    language: str
    spacy: SpacySetting
    unicode_normalization: UnicodeNormalizationSetting
    html_removal: EnabledSetting
    url_removal: EnabledSetting
    email_removal: EnabledSetting
    whitespace_normalization: EnabledSetting
    lowercasing: EnabledSetting
    special_character_handling: HandlingSetting
    number_handling: HandlingSetting
    punctuation_handling: HandlingSetting
    tokenization: EnabledSetting
    stopword_removal: StopwordSetting
    lemmatization: EnabledSetting
    validation: ValidationSetting

    @classmethod
    def from_json_file(cls, path: Path) -> 'PreprocessingConfig':
        try:
            payload = json.loads(path.read_text(encoding='utf-8'))
        except (OSError, json.JSONDecodeError) as error:
            raise ValueError('Preprocessing configuration is unreadable.') from error
        if not isinstance(payload, dict):
            raise ValueError('Preprocessing configuration must be an object.')

        def mapping(name: str) -> dict[str, Any]:
            value = payload.get(name)
            if not isinstance(value, dict):
                raise ValueError(f'Preprocessing configuration field {name} must be an object.')
            return value

        def enabled(name: str) -> EnabledSetting:
            value = mapping(name).get('enabled')
            if not isinstance(value, bool):
                raise ValueError(f'Preprocessing configuration field {name}.enabled must be boolean.')
            return EnabledSetting(enabled=value)

        def handling(name: str) -> HandlingSetting:
            value = mapping(name)
            if not isinstance(value.get('enabled'), bool) or value.get('mode') not in {
                'preserve',
                'remove',
                'replace_with_space',
            }:
                raise ValueError(f'Preprocessing configuration field {name} is invalid.')
            return HandlingSetting(enabled=value['enabled'], mode=value['mode'])

        spacy = mapping('spacy')
        validation = mapping('validation')
        unicode_normalization = mapping('unicode_normalization')
        stopwords = mapping('stopword_removal')
        if not isinstance(payload.get('pipeline_version'), str) or not isinstance(payload.get('language'), str):
            raise ValueError('Preprocessing configuration identity fields are invalid.')
        if not isinstance(spacy.get('model_name'), str) or not isinstance(spacy.get('allow_blank_fallback'), bool):
            raise ValueError('Preprocessing configuration spaCy settings are invalid.')
        if not isinstance(spacy.get('batch_size'), int) or spacy['batch_size'] < 1:
            raise ValueError('Preprocessing configuration spaCy batch size is invalid.')
        if not isinstance(unicode_normalization.get('enabled'), bool) or unicode_normalization.get('form') not in {
            'NFC', 'NFD', 'NFKC', 'NFKD'
        }:
            raise ValueError('Preprocessing configuration Unicode settings are invalid.')
        if not isinstance(stopwords.get('enabled'), bool) or not isinstance(stopwords.get('preserve_negations'), bool):
            raise ValueError('Preprocessing configuration stopword settings are invalid.')
        if not isinstance(validation.get('max_empty_document_rate'), (int, float)):
            raise ValueError('Preprocessing configuration empty-document threshold is invalid.')
        if not isinstance(validation.get('max_failures'), int) or validation['max_failures'] < 0:
            raise ValueError('Preprocessing configuration failure threshold is invalid.')

        return cls(
            pipeline_version=payload['pipeline_version'],
            language=payload['language'],
            spacy=SpacySetting(**spacy),
            unicode_normalization=UnicodeNormalizationSetting(**unicode_normalization),
            html_removal=enabled('html_removal'),
            url_removal=enabled('url_removal'),
            email_removal=enabled('email_removal'),
            whitespace_normalization=enabled('whitespace_normalization'),
            lowercasing=enabled('lowercasing'),
            special_character_handling=handling('special_character_handling'),
            number_handling=handling('number_handling'),
            punctuation_handling=handling('punctuation_handling'),
            tokenization=enabled('tokenization'),
            stopword_removal=StopwordSetting(**stopwords),
            lemmatization=enabled('lemmatization'),
            validation=ValidationSetting(**validation),
        )
