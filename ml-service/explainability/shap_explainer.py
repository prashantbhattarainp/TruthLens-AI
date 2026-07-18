"""SHAP explanations for the frozen sparse TF-IDF LinearSVC classifier."""

from __future__ import annotations

from typing import Any

import numpy as np
import shap
from scipy import sparse

from schemas.explainability import ShapExplanation

from .utilities import rank_signed_features


class ShapTextExplainer:
    """Uses SHAP's linear explainer with a transparent all-zero TF-IDF reference."""

    def __init__(self, *, classifier: Any, feature_names: np.ndarray, top_feature_count: int) -> None:
        self.classifier = classifier
        self.feature_names = np.asarray(feature_names, dtype=object)
        self.top_feature_count = top_feature_count
        reference = sparse.csr_matrix((1, self.feature_names.size), dtype=float)
        self._explainer = shap.LinearExplainer(classifier, reference)

    def explain(self, feature_vector: Any, *, decision_score: float) -> ShapExplanation:
        shap_values = self._explainer(feature_vector)
        values = np.asarray(shap_values.values, dtype=float).reshape(-1)
        base_values = np.asarray(shap_values.base_values, dtype=float).reshape(-1)
        active_indices = feature_vector.nonzero()[1]
        active_names = self.feature_names[active_indices]
        active_values = values[active_indices]
        positive, negative, least = rank_signed_features(
            active_names,
            active_values,
            limit=self.top_feature_count,
        )
        base_value = float(base_values[0]) if base_values.size else 0.0
        return ShapExplanation(
            method='linear_shap',
            baseline='zero_tfidf_reference',
            base_value=base_value,
            additive_residual=float(decision_score - base_value - values.sum()),
            top_positive_features=positive,
            top_negative_features=negative,
            least_influential_features=least,
        )
