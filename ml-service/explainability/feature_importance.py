"""Global, non-evaluative feature-importance analysis for sparse linear models."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

from schemas.explainability import FeatureContribution

from .utilities import merge_top_features, rank_signed_features


@dataclass(frozen=True)
class GlobalFeatureImportance:
    coefficient_positive: list[FeatureContribution]
    coefficient_negative: list[FeatureContribution]
    coefficient_top: list[FeatureContribution]
    mean_absolute_shap: list[FeatureContribution]


def calculate_global_feature_importance(
    *,
    classifier: Any,
    feature_names: np.ndarray,
    feature_matrix: Any,
    top_feature_count: int,
) -> GlobalFeatureImportance:
    """Aggregate train-only zero-reference SHAP magnitudes without model evaluation."""

    coefficients = np.asarray(classifier.coef_, dtype=float).reshape(-1)
    coefficient_positive, coefficient_negative, _ = rank_signed_features(
        feature_names,
        coefficients,
        limit=top_feature_count,
    )
    mean_absolute_shap = np.asarray(abs(feature_matrix.multiply(coefficients)).mean(axis=0)).reshape(-1)
    signed_global_magnitude = np.copysign(mean_absolute_shap, coefficients)
    magnitude_positive, magnitude_negative, _ = rank_signed_features(
        feature_names,
        signed_global_magnitude,
        limit=top_feature_count,
    )
    return GlobalFeatureImportance(
        coefficient_positive=coefficient_positive,
        coefficient_negative=coefficient_negative,
        coefficient_top=merge_top_features(
            coefficient_positive,
            coefficient_negative,
            limit=top_feature_count * 2,
        ),
        mean_absolute_shap=merge_top_features(
            magnitude_positive,
            magnitude_negative,
            limit=top_feature_count * 2,
        ),
    )
