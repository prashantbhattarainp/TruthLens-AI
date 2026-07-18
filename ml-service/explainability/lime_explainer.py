"""LIME local margin-surrogate explanations for the existing text pipeline."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path
from typing import Any

os.environ.setdefault('MPLCONFIGDIR', str(Path(tempfile.gettempdir()) / 'truthlens-matplotlib'))

import numpy as np
from lime.lime_text import LimeTextExplainer

from schemas.explainability import LimeExplanation

from .utilities import rank_signed_features


class LimeTextMarginExplainer:
    """Explains the uncalibrated Fake-minus-Real margin, never a probability."""

    def __init__(
        self,
        *,
        classifier: Any,
        vectorizer: Any,
        top_feature_count: int,
        sample_count: int,
        random_seed: int,
    ) -> None:
        self.classifier = classifier
        self.vectorizer = vectorizer
        self.top_feature_count = top_feature_count
        self.sample_count = sample_count
        self.random_seed = random_seed
        self._explainer = LimeTextExplainer(
            class_names=['Real margin', 'Fake margin'],
            random_state=random_seed,
        )

    def explain(self, processed_text: str) -> LimeExplanation:
        result = self._explainer.explain_instance(
            processed_text,
            self._score_matrix,
            labels=(1,),
            num_features=self.top_feature_count * 2,
            num_samples=self.sample_count,
        )
        features, values = zip(*result.as_list(label=1), strict=True) if result.as_list(label=1) else ((), ())
        positive, negative, _least = rank_signed_features(
            features,
            values,
            limit=self.top_feature_count,
        )
        return LimeExplanation(
            method='lime_text_margin_surrogate',
            target='fake_margin',
            local_fidelity=float(result.score),
            random_seed=self.random_seed,
            sample_count=self.sample_count,
            top_positive_features=positive,
            top_negative_features=negative,
        )

    def _score_matrix(self, processed_texts: list[str]) -> np.ndarray:
        feature_matrix = self.vectorizer.transform(processed_texts)
        fake_margin = np.asarray(self.classifier.decision_function(feature_matrix), dtype=float)
        return np.column_stack((-fake_margin, fake_margin))
