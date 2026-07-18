"""Bounded, deployment-configurable parameters for local explanations."""

from dataclasses import dataclass

from config import Settings


@dataclass(frozen=True)
class ExplainabilityConfiguration:
    top_feature_count: int
    lime_sample_count: int
    lime_random_seed: int

    @classmethod
    def from_settings(cls, settings: Settings) -> 'ExplainabilityConfiguration':
        return cls(
            top_feature_count=settings.xai_top_feature_count,
            lime_sample_count=settings.xai_lime_sample_count,
            lime_random_seed=settings.xai_lime_random_seed,
        )
