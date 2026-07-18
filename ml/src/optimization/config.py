"""Strict, hashable configuration contract for Phase 3.9 searches."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping


_MODELS = {"logistic_regression", "multinomial_naive_bayes", "linear_svm"}


@dataclass(frozen=True)
class OptimizationConfig:
    """One reproducible search definition for one already-approved baseline."""

    optimization_framework_version: str
    model: str
    model_version: str
    search_strategy: str
    scoring: str
    random_seed: int
    n_splits: int
    parameter_grid: tuple[dict[str, tuple[Any, ...]], ...]

    @classmethod
    def from_json_file(cls, path: Path) -> "OptimizationConfig":
        return cls.from_mapping(json.loads(path.read_text(encoding="utf-8")))

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "OptimizationConfig":
        expected = {
            "optimization_framework_version", "model", "model_version", "search_strategy", "scoring",
            "random_seed", "n_splits", "parameter_grid",
        }
        if set(payload) != expected:
            raise ValueError(f"Optimization configuration keys must match the schema; got {sorted(payload)}.")
        model = _text(payload["model"], "model")
        if model not in _MODELS:
            raise ValueError(f"Optimization model must be one of {sorted(_MODELS)}.")
        strategy, scoring = _text(payload["search_strategy"], "search_strategy"), _text(payload["scoring"], "scoring")
        if strategy != "grid" or scoring != "macro_f1":
            raise ValueError("Phase 3.9 requires grid search with Macro F1 scoring.")
        seed, n_splits = payload["random_seed"], payload["n_splits"]
        if not isinstance(seed, int) or isinstance(seed, bool) or seed < 0:
            raise ValueError("random_seed must be a non-negative integer.")
        if n_splits != 5:
            raise ValueError("The frozen experiment protocol requires exactly five folds.")
        raw_grid = payload["parameter_grid"]
        if not isinstance(raw_grid, list) or not raw_grid:
            raise ValueError("parameter_grid must be a non-empty list of parameter objects.")
        grid: list[dict[str, tuple[Any, ...]]] = []
        for candidate in raw_grid:
            if not isinstance(candidate, Mapping) or not candidate:
                raise ValueError("Each parameter-grid branch must be a non-empty object.")
            normalized: dict[str, tuple[Any, ...]] = {}
            for key, values in candidate.items():
                if not isinstance(key, str) or not key or not isinstance(values, list) or not values:
                    raise ValueError("Each parameter-grid field must have a non-empty list of values.")
                normalized[key] = tuple(values)
            grid.append(normalized)
        return cls(
            optimization_framework_version=_text(payload["optimization_framework_version"], "optimization_framework_version"),
            model=model,
            model_version=_text(payload["model_version"], "model_version"),
            search_strategy=strategy,
            scoring=scoring,
            random_seed=seed,
            n_splits=n_splits,
            parameter_grid=tuple(grid),
        )

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["parameter_grid"] = [{key: list(values) for key, values in branch.items()} for branch in self.parameter_grid]
        return value

    @property
    def sha256(self) -> str:
        canonical = json.dumps(self.to_dict(), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    @property
    def configuration_count(self) -> int:
        total = 0
        for branch in self.parameter_grid:
            count = 1
            for values in branch.values():
                count *= len(values)
            total += count
        return total


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be non-empty text.")
    return value
