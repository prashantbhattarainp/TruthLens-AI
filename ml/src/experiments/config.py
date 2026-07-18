"""Strict, hashable configuration for baseline-model experiments."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping

from experiments.exceptions import ExperimentConfigurationError


CV_STRATEGIES = {"stratified_kfold", "stratified_group_kfold"}


@dataclass(frozen=True)
class CrossValidationSettings:
    strategy: str
    n_splits: int
    shuffle: bool


@dataclass(frozen=True)
class MetricsSettings:
    primary_metric: str
    positive_label: int
    zero_division: int


@dataclass(frozen=True)
class ExperimentConfig:
    """Configuration that identifies one baseline method and reproducible CV policy."""

    experiment_framework_version: str
    model: str
    model_version: str
    hyperparameters: dict[str, Any]
    cross_validation: CrossValidationSettings
    random_seed: int
    metrics: MetricsSettings

    @classmethod
    def from_json_file(cls, path: Path) -> "ExperimentConfig":
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except OSError as error:
            raise ExperimentConfigurationError(f"Unable to read configuration {path}: {error}") from error
        except json.JSONDecodeError as error:
            raise ExperimentConfigurationError(f"Configuration {path} is not valid JSON: {error}") from error
        return cls.from_mapping(payload)

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "ExperimentConfig":
        expected = {
            "experiment_framework_version",
            "model",
            "model_version",
            "hyperparameters",
            "cross_validation",
            "random_seed",
            "metrics",
        }
        unknown, missing = set(payload) - expected, expected - set(payload)
        if unknown or missing:
            raise ExperimentConfigurationError(
                f"Configuration keys must match the schema; missing={sorted(missing)}, unknown={sorted(unknown)}."
            )
        hyperparameters = payload["hyperparameters"]
        if not isinstance(hyperparameters, Mapping):
            raise ExperimentConfigurationError("hyperparameters must be an object.")
        seed = payload["random_seed"]
        if not isinstance(seed, int) or isinstance(seed, bool) or seed < 0:
            raise ExperimentConfigurationError("random_seed must be a nonnegative integer.")
        return cls(
            experiment_framework_version=_nonempty_text(payload, "experiment_framework_version"),
            model=_nonempty_text(payload, "model"),
            model_version=_nonempty_text(payload, "model_version"),
            hyperparameters=dict(hyperparameters),
            cross_validation=_cross_validation(payload["cross_validation"]),
            random_seed=seed,
            metrics=_metrics(payload["metrics"]),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @property
    def sha256(self) -> str:
        canonical = json.dumps(self.to_dict(), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _cross_validation(value: Any) -> CrossValidationSettings:
    if not isinstance(value, Mapping) or set(value) != {"strategy", "n_splits", "shuffle"}:
        raise ExperimentConfigurationError(
            "cross_validation must contain strategy, n_splits, and shuffle."
        )
    strategy, n_splits, shuffle = value["strategy"], value["n_splits"], value["shuffle"]
    if strategy not in CV_STRATEGIES:
        raise ExperimentConfigurationError(f"cross_validation.strategy must be one of {sorted(CV_STRATEGIES)}.")
    if not isinstance(n_splits, int) or isinstance(n_splits, bool) or n_splits < 2:
        raise ExperimentConfigurationError("cross_validation.n_splits must be an integer of at least two.")
    if not isinstance(shuffle, bool):
        raise ExperimentConfigurationError("cross_validation.shuffle must be boolean.")
    return CrossValidationSettings(strategy=strategy, n_splits=n_splits, shuffle=shuffle)


def _metrics(value: Any) -> MetricsSettings:
    if not isinstance(value, Mapping) or set(value) != {"primary_metric", "positive_label", "zero_division"}:
        raise ExperimentConfigurationError(
            "metrics must contain primary_metric, positive_label, and zero_division."
        )
    primary_metric, positive_label, zero_division = (
        value["primary_metric"],
        value["positive_label"],
        value["zero_division"],
    )
    if primary_metric != "macro_f1":
        raise ExperimentConfigurationError("macro_f1 is the required Phase 3 primary metric.")
    if positive_label != 1 or zero_division not in {0, 1}:
        raise ExperimentConfigurationError("metrics require positive_label=1 and zero_division of 0 or 1.")
    return MetricsSettings(
        primary_metric=primary_metric,
        positive_label=positive_label,
        zero_division=zero_division,
    )


def _nonempty_text(payload: Mapping[str, Any], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ExperimentConfigurationError(f"{key} must be a nonempty string.")
    return value
