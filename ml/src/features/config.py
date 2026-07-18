"""Strict, hashable configuration for feature-representation methods."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping

from features.exceptions import FeatureConfigurationError


METHOD_NAME_PATTERN = re.compile(r"^[a-z][a-z0-9_-]*$")
NORMALIZATION_MODES = {"none", "l1", "l2"}


@dataclass(frozen=True)
class FeatureValidationSettings:
    max_empty_feature_vector_rate: float
    max_matrix_memory_mb: float
    require_nonempty_vocabulary: bool


@dataclass(frozen=True)
class FeatureConfig:
    """Versioned method configuration whose canonical JSON identity is recorded per run."""

    feature_pipeline_version: str
    method: str
    parameters: dict[str, Any]
    validation: FeatureValidationSettings

    @classmethod
    def from_json_file(cls, path: Path) -> "FeatureConfig":
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except OSError as error:
            raise FeatureConfigurationError(f"Unable to read configuration {path}: {error}") from error
        except json.JSONDecodeError as error:
            raise FeatureConfigurationError(f"Configuration {path} is not valid JSON: {error}") from error
        return cls.from_mapping(payload)

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "FeatureConfig":
        expected = {"feature_pipeline_version", "method", "parameters", "validation"}
        unknown, missing = set(payload) - expected, expected - set(payload)
        if unknown or missing:
            raise FeatureConfigurationError(
                f"Configuration keys must match the schema; missing={sorted(missing)}, unknown={sorted(unknown)}."
            )
        version = _nonempty_text(payload, "feature_pipeline_version")
        method = _nonempty_text(payload, "method")
        if not METHOD_NAME_PATTERN.fullmatch(method):
            raise FeatureConfigurationError("method must use lowercase letters, numbers, underscores, or hyphens.")
        parameters = payload["parameters"]
        if not isinstance(parameters, Mapping):
            raise FeatureConfigurationError("parameters must be an object.")
        return cls(
            feature_pipeline_version=version,
            method=method,
            parameters=dict(parameters),
            validation=_validation_settings(payload["validation"]),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @property
    def sha256(self) -> str:
        canonical = json.dumps(self.to_dict(), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class VectorizerParameters:
    """Parameter contract shared by the CountVectorizer and TF-IDF components."""

    ngram_range: tuple[int, int]
    max_features: int | None
    min_df: int | float
    max_df: int | float
    binary: bool
    normalization: str

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "VectorizerParameters":
        expected = {"ngram_range", "max_features", "min_df", "max_df", "binary", "normalization"}
        unknown, missing = set(payload) - expected, expected - set(payload)
        if unknown or missing:
            raise FeatureConfigurationError(
                "Vectorizer parameters must match the baseline schema; "
                f"missing={sorted(missing)}, unknown={sorted(unknown)}."
            )
        ngram_range = payload["ngram_range"]
        if (
            not isinstance(ngram_range, list)
            or len(ngram_range) != 2
            or any(not _positive_integer(value) for value in ngram_range)
            or ngram_range[0] > ngram_range[1]
        ):
            raise FeatureConfigurationError("ngram_range must be a two-item ascending list of positive integers.")
        max_features = payload["max_features"]
        if max_features is not None and not _positive_integer(max_features):
            raise FeatureConfigurationError("max_features must be null or a positive integer.")
        min_df, max_df = _document_frequency(payload["min_df"], "min_df"), _document_frequency(
            payload["max_df"], "max_df"
        )
        if type(min_df) is type(max_df) and min_df > max_df:
            raise FeatureConfigurationError("min_df cannot exceed max_df when both use the same unit.")
        binary, normalization = payload["binary"], payload["normalization"]
        if not isinstance(binary, bool):
            raise FeatureConfigurationError("binary must be a boolean.")
        if normalization not in NORMALIZATION_MODES:
            raise FeatureConfigurationError(f"normalization must be one of {sorted(NORMALIZATION_MODES)}.")
        return cls(
            ngram_range=(ngram_range[0], ngram_range[1]),
            max_features=max_features,
            min_df=min_df,
            max_df=max_df,
            binary=binary,
            normalization=normalization,
        )


def _validation_settings(value: Any) -> FeatureValidationSettings:
    if not isinstance(value, Mapping):
        raise FeatureConfigurationError("validation must be an object.")
    expected = {"max_empty_feature_vector_rate", "max_matrix_memory_mb", "require_nonempty_vocabulary"}
    if set(value) != expected:
        raise FeatureConfigurationError("validation must contain the complete baseline validation schema.")
    empty_rate, memory_mb, require_vocabulary = (
        value["max_empty_feature_vector_rate"],
        value["max_matrix_memory_mb"],
        value["require_nonempty_vocabulary"],
    )
    if not _nonnegative_number(empty_rate) or float(empty_rate) > 1:
        raise FeatureConfigurationError("max_empty_feature_vector_rate must be between zero and one.")
    if not _positive_number(memory_mb) or not isinstance(require_vocabulary, bool):
        raise FeatureConfigurationError(
            "max_matrix_memory_mb must be positive and require_nonempty_vocabulary must be boolean."
        )
    return FeatureValidationSettings(
        max_empty_feature_vector_rate=float(empty_rate),
        max_matrix_memory_mb=float(memory_mb),
        require_nonempty_vocabulary=require_vocabulary,
    )


def _nonempty_text(payload: Mapping[str, Any], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        raise FeatureConfigurationError(f"{key} must be a nonempty string.")
    return value


def _positive_integer(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def _nonnegative_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value >= 0


def _positive_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0


def _document_frequency(value: Any, key: str) -> int | float:
    if _positive_integer(value):
        return value
    if isinstance(value, float) and 0 < value <= 1:
        return value
    raise FeatureConfigurationError(f"{key} must be a positive integer or a proportion in (0, 1].")
