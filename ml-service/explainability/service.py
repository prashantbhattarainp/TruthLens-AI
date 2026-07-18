"""Orchestrates local SHAP and LIME explanations after a successful prediction."""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass

from inference.production_model_service import PreparedPrediction, ProductionModelService
from logging_config import get_logger
from schemas.explainability import ExplainabilityMetadata, PredictionExplainability

from .configuration import ExplainabilityConfiguration
from .lime_explainer import LimeTextMarginExplainer
from .shap_explainer import ShapTextExplainer
from .utilities import merge_top_features


@dataclass(frozen=True)
class ExplainedPrediction:
    prepared_prediction: PreparedPrediction
    explainability: PredictionExplainability
    keywords: list[str]
    processing_time_ms: int


class ExplanationService:
    """In-process explanation boundary; input text remains in memory for one request only."""

    def __init__(
        self,
        model_service: ProductionModelService,
        configuration: ExplainabilityConfiguration,
    ) -> None:
        self.model_service = model_service
        self.configuration = configuration
        self._lock = threading.Lock()
        self._shap_explainer: ShapTextExplainer | None = None
        self._lime_explainer: LimeTextMarginExplainer | None = None
        self._component_identity: tuple[int, int] | None = None
        self._logger = get_logger()

    def predict_and_explain(self, *, headline: str, article: str) -> ExplainedPrediction:
        started = time.perf_counter()
        prepared = self.model_service.predict_with_context(headline=headline, article=article)
        explainability = self.explain_prepared(prepared)
        keywords = [contribution.feature for contribution in explainability.top_influential_features]
        return ExplainedPrediction(
            prepared_prediction=prepared,
            explainability=explainability,
            keywords=keywords,
            processing_time_ms=round((time.perf_counter() - started) * 1000),
        )

    def explain_prepared(self, prepared: PreparedPrediction) -> PredictionExplainability:
        try:
            shap_explainer, lime_explainer = self._get_explainers()
            shap_result = shap_explainer.explain(
                prepared.feature_vector,
                decision_score=prepared.prediction.decision_score,
            )
            lime_result = lime_explainer.explain(prepared.processed_text)
            top_features = merge_top_features(
                shap_result.top_positive_features,
                shap_result.top_negative_features,
                limit=self.configuration.top_feature_count,
            )
            return PredictionExplainability(
                metadata=self._metadata(status='available'),
                top_influential_features=top_features,
                shap=shap_result,
                lime=lime_result,
            )
        except Exception as error:
            self._logger.exception(
                'prediction_explanation_failed',
                extra={
                    'event': 'prediction_explanation_failed',
                    'error_type': type(error).__name__,
                },
            )
            return PredictionExplainability(
                metadata=self._metadata(status='unavailable'),
                top_influential_features=[],
                shap=None,
                lime=None,
            )

    def _get_explainers(self) -> tuple[ShapTextExplainer, LimeTextMarginExplainer]:
        vectorizer, classifier = self.model_service.explainability_components()
        identity = (id(vectorizer), id(classifier))
        if self._component_identity == identity and self._shap_explainer and self._lime_explainer:
            return self._shap_explainer, self._lime_explainer
        with self._lock:
            if self._component_identity != identity or not self._shap_explainer or not self._lime_explainer:
                feature_names = vectorizer.get_feature_names_out()
                self._shap_explainer = ShapTextExplainer(
                    classifier=classifier,
                    feature_names=feature_names,
                    top_feature_count=self.configuration.top_feature_count,
                )
                self._lime_explainer = LimeTextMarginExplainer(
                    classifier=classifier,
                    vectorizer=vectorizer,
                    top_feature_count=self.configuration.top_feature_count,
                    sample_count=self.configuration.lime_sample_count,
                    random_seed=self.configuration.lime_random_seed,
                )
                self._component_identity = identity
        assert self._shap_explainer is not None and self._lime_explainer is not None
        return self._shap_explainer, self._lime_explainer

    @staticmethod
    def _metadata(*, status: str) -> ExplainabilityMetadata:
        return ExplainabilityMetadata(
            status=status,
            prediction_confidence_status='unavailable',
            decision_score_interpretation='uncalibrated_linear_svm_margin',
            preprocessing_reused=True,
            feature_engineering_reused=True,
            disclaimer=(
                'Feature contributions explain the model margin only; they are not evidence of factual '
                'truth, causal effects, calibrated confidence, or a fact-checking verdict.'
            ),
        )
