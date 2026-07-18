"""Configuration-driven construction of approved baseline classifier instances."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sklearn.base import ClassifierMixin

from experiments.exceptions import ExperimentConfigurationError
from models.registry import BaselineModelRegistry, build_baseline_model_registry

if TYPE_CHECKING:
    from experiments.config import ExperimentConfig


class BaselineModelFactory:
    """Creates only registered Phase 3.7 baseline models from declared hyperparameters."""

    def __init__(self, registry: BaselineModelRegistry | None = None) -> None:
        self._registry = registry or build_baseline_model_registry()

    def create(self, config: "ExperimentConfig", seed: int) -> ClassifierMixin:
        parameters = dict(config.hyperparameters)
        try:
            return self._registry.get(config.model)(parameters, seed)
        except (TypeError, ValueError) as error:
            raise ExperimentConfigurationError(
                f"Invalid hyperparameters for {config.model!r}: {error}"
            ) from error
