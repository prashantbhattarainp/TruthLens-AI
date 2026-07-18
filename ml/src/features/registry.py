"""Open registry for feature-extractor components."""

from __future__ import annotations

from collections.abc import Callable

from features.config import FeatureConfig
from features.exceptions import FeatureConfigurationError
from features.extractors.base import FeatureExtractor
from features.extractors.count import CountFeatureExtractor
from features.extractors.tfidf import TfidfFeatureExtractor


FeatureExtractorFactory = Callable[[FeatureConfig], FeatureExtractor]


class FeatureExtractorRegistry:
    """Maps a configuration method name to an independently supplied extractor factory."""

    def __init__(self) -> None:
        self._factories: dict[str, FeatureExtractorFactory] = {}

    def register(self, method: str, factory: FeatureExtractorFactory) -> None:
        if method in self._factories:
            raise FeatureConfigurationError(f"A feature extractor is already registered for {method!r}.")
        self._factories[method] = factory

    def create(self, config: FeatureConfig) -> FeatureExtractor:
        factory = self._factories.get(config.method)
        if factory is None:
            available = ", ".join(sorted(self._factories)) or "none"
            raise FeatureConfigurationError(
                f"No extractor is registered for {config.method!r}. Available methods: {available}."
            )
        return factory(config)


def build_default_registry() -> FeatureExtractorRegistry:
    """Register baseline methods at the composition root without constraining future extensions."""
    registry = FeatureExtractorRegistry()
    registry.register(CountFeatureExtractor.method, CountFeatureExtractor)
    registry.register(TfidfFeatureExtractor.method, TfidfFeatureExtractor)
    return registry
