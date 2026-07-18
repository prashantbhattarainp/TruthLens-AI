"""Closed registry of the baseline algorithms approved for Phase 3.7."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from sklearn.base import ClassifierMixin
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC


ModelBuilder = Callable[[dict[str, Any], int], ClassifierMixin]


class BaselineModelRegistry:
    """Registry deliberately limited to the three transparent approved baselines."""

    def __init__(self) -> None:
        self._builders: dict[str, ModelBuilder] = {}

    def register(self, name: str, builder: ModelBuilder) -> None:
        if name in self._builders:
            raise ValueError(f"A baseline model is already registered for {name!r}.")
        self._builders[name] = builder

    def get(self, name: str) -> ModelBuilder:
        try:
            return self._builders[name]
        except KeyError as error:
            allowed = ", ".join(sorted(self._builders))
            raise ValueError(f"Model {name!r} is not approved. Allowed baseline models: {allowed}.") from error

    @property
    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._builders))


def build_baseline_model_registry() -> BaselineModelRegistry:
    """Build the Phase 3.7 model allowlist without exposing unapproved algorithms."""
    registry = BaselineModelRegistry()
    registry.register("logistic_regression", _build_logistic_regression)
    registry.register("multinomial_naive_bayes", _build_multinomial_naive_bayes)
    registry.register("linear_svm", _build_linear_svm)
    return registry


def _build_logistic_regression(parameters: dict[str, Any], seed: int) -> ClassifierMixin:
    return LogisticRegression(random_state=seed, **parameters)


def _build_multinomial_naive_bayes(parameters: dict[str, Any], _seed: int) -> ClassifierMixin:
    return MultinomialNB(**parameters)


def _build_linear_svm(parameters: dict[str, Any], seed: int) -> ClassifierMixin:
    return LinearSVC(random_state=seed, **parameters)
