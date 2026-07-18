"""Strict, serialisable configuration for modular preprocessing operations."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping

from preprocessing.exceptions import ConfigurationError


HANDLING_MODES = {"preserve", "remove", "replace_with_space", "replace_with_token"}
NEGATIONS = frozenset({"no", "nor", "not", "never", "neither", "none", "n't"})


@dataclass(frozen=True)
class EnabledSetting:
    enabled: bool


@dataclass(frozen=True)
class UnicodeNormalizationSetting:
    enabled: bool
    form: str


@dataclass(frozen=True)
class HandlingSetting:
    enabled: bool
    mode: str


@dataclass(frozen=True)
class StopwordSetting:
    enabled: bool
    preserve_negations: bool


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
    """Versioned configuration whose serialisation is hashed for every run."""

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
    def from_json_file(cls, path: Path) -> "PreprocessingConfig":
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except OSError as error:
            raise ConfigurationError(f"Unable to read configuration {path}: {error}") from error
        except json.JSONDecodeError as error:
            raise ConfigurationError(f"Configuration {path} is not valid JSON: {error}") from error
        return cls.from_mapping(payload)

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "PreprocessingConfig":
        expected = {
            "pipeline_version",
            "language",
            "spacy",
            "unicode_normalization",
            "html_removal",
            "url_removal",
            "email_removal",
            "whitespace_normalization",
            "lowercasing",
            "special_character_handling",
            "number_handling",
            "punctuation_handling",
            "tokenization",
            "stopword_removal",
            "lemmatization",
            "validation",
        }
        unknown = set(payload) - expected
        missing = expected - set(payload)
        if unknown or missing:
            raise ConfigurationError(
                f"Configuration keys must match the schema; missing={sorted(missing)}, unknown={sorted(unknown)}."
            )

        config = cls(
            pipeline_version=_required_nonempty_text(payload, "pipeline_version"),
            language=_required_nonempty_text(payload, "language"),
            spacy=_spacy_setting(_mapping(payload, "spacy")),
            unicode_normalization=_unicode_setting(_mapping(payload, "unicode_normalization")),
            html_removal=_enabled_setting(_mapping(payload, "html_removal"), "html_removal"),
            url_removal=_enabled_setting(_mapping(payload, "url_removal"), "url_removal"),
            email_removal=_enabled_setting(_mapping(payload, "email_removal"), "email_removal"),
            whitespace_normalization=_enabled_setting(
                _mapping(payload, "whitespace_normalization"), "whitespace_normalization"
            ),
            lowercasing=_enabled_setting(_mapping(payload, "lowercasing"), "lowercasing"),
            special_character_handling=_handling_setting(
                _mapping(payload, "special_character_handling"), "special_character_handling"
            ),
            number_handling=_handling_setting(_mapping(payload, "number_handling"), "number_handling"),
            punctuation_handling=_handling_setting(
                _mapping(payload, "punctuation_handling"), "punctuation_handling"
            ),
            tokenization=_enabled_setting(_mapping(payload, "tokenization"), "tokenization"),
            stopword_removal=_stopword_setting(_mapping(payload, "stopword_removal")),
            lemmatization=_enabled_setting(_mapping(payload, "lemmatization"), "lemmatization"),
            validation=_validation_setting(_mapping(payload, "validation")),
        )
        if not config.tokenization.enabled and (
            config.stopword_removal.enabled or config.lemmatization.enabled
        ):
            raise ConfigurationError("Stopword removal and lemmatization require tokenization.")
        return config

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @property
    def sha256(self) -> str:
        canonical = json.dumps(self.to_dict(), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _mapping(payload: Mapping[str, Any], key: str) -> Mapping[str, Any]:
    value = payload.get(key)
    if not isinstance(value, Mapping):
        raise ConfigurationError(f"{key} must be an object.")
    return value


def _required_nonempty_text(payload: Mapping[str, Any], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ConfigurationError(f"{key} must be a nonempty string.")
    return value


def _enabled_setting(payload: Mapping[str, Any], key: str) -> EnabledSetting:
    if set(payload) != {"enabled"} or not isinstance(payload["enabled"], bool):
        raise ConfigurationError(f"{key} must contain only boolean enabled.")
    return EnabledSetting(enabled=payload["enabled"])


def _unicode_setting(payload: Mapping[str, Any]) -> UnicodeNormalizationSetting:
    if set(payload) != {"enabled", "form"}:
        raise ConfigurationError("unicode_normalization must contain enabled and form.")
    enabled, form = payload["enabled"], payload["form"]
    if not isinstance(enabled, bool) or form not in {"NFC", "NFD", "NFKC", "NFKD"}:
        raise ConfigurationError("unicode_normalization.form must be NFC, NFD, NFKC, or NFKD.")
    return UnicodeNormalizationSetting(enabled=enabled, form=form)


def _handling_setting(payload: Mapping[str, Any], key: str) -> HandlingSetting:
    if set(payload) != {"enabled", "mode"}:
        raise ConfigurationError(f"{key} must contain enabled and mode.")
    enabled, mode = payload["enabled"], payload["mode"]
    if not isinstance(enabled, bool) or mode not in HANDLING_MODES:
        raise ConfigurationError(f"{key}.mode must be one of {sorted(HANDLING_MODES)}.")
    return HandlingSetting(enabled=enabled, mode=mode)


def _stopword_setting(payload: Mapping[str, Any]) -> StopwordSetting:
    if set(payload) != {"enabled", "preserve_negations"}:
        raise ConfigurationError("stopword_removal must contain enabled and preserve_negations.")
    enabled, preserve_negations = payload["enabled"], payload["preserve_negations"]
    if not isinstance(enabled, bool) or not isinstance(preserve_negations, bool):
        raise ConfigurationError("stopword_removal values must be booleans.")
    return StopwordSetting(enabled=enabled, preserve_negations=preserve_negations)


def _spacy_setting(payload: Mapping[str, Any]) -> SpacySetting:
    if set(payload) != {"model_name", "allow_blank_fallback", "batch_size"}:
        raise ConfigurationError("spacy must contain model_name, allow_blank_fallback, and batch_size.")
    model_name = _required_nonempty_text(payload, "model_name")
    fallback, batch_size = payload["allow_blank_fallback"], payload["batch_size"]
    if not isinstance(fallback, bool) or not isinstance(batch_size, int) or batch_size < 1:
        raise ConfigurationError("spacy.allow_blank_fallback must be boolean and batch_size a positive integer.")
    return SpacySetting(model_name=model_name, allow_blank_fallback=fallback, batch_size=batch_size)


def _validation_setting(payload: Mapping[str, Any]) -> ValidationSetting:
    if set(payload) != {"max_empty_document_rate", "max_failures"}:
        raise ConfigurationError("validation must contain max_empty_document_rate and max_failures.")
    empty_rate, max_failures = payload["max_empty_document_rate"], payload["max_failures"]
    if (
        not isinstance(empty_rate, (int, float))
        or not 0 <= float(empty_rate) <= 1
        or not isinstance(max_failures, int)
        or max_failures < 0
    ):
        raise ConfigurationError("validation values are outside their allowed ranges.")
    return ValidationSetting(max_empty_document_rate=float(empty_rate), max_failures=max_failures)
