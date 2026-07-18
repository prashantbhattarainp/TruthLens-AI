"""Pydantic response contracts for bounded explanation metadata."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class FeatureContribution(BaseModel):
    model_config = ConfigDict(extra='forbid')

    feature: str = Field(min_length=1)
    contribution: float
    direction: Literal['supports_fake_margin', 'supports_real_margin', 'minimal_effect']
    rank: int = Field(ge=1)


class ShapExplanation(BaseModel):
    model_config = ConfigDict(extra='forbid')

    method: Literal['linear_shap']
    baseline: Literal['zero_tfidf_reference']
    base_value: float
    additive_residual: float
    top_positive_features: list[FeatureContribution]
    top_negative_features: list[FeatureContribution]
    least_influential_features: list[FeatureContribution]


class LimeExplanation(BaseModel):
    model_config = ConfigDict(extra='forbid')

    method: Literal['lime_text_margin_surrogate']
    target: Literal['fake_margin']
    local_fidelity: float
    random_seed: int = Field(ge=0)
    sample_count: int = Field(ge=1)
    top_positive_features: list[FeatureContribution]
    top_negative_features: list[FeatureContribution]


class ExplainabilityMetadata(BaseModel):
    model_config = ConfigDict(extra='forbid')

    status: Literal['available', 'unavailable']
    prediction_confidence_status: Literal['unavailable']
    decision_score_interpretation: Literal['uncalibrated_linear_svm_margin']
    preprocessing_reused: bool
    feature_engineering_reused: bool
    disclaimer: str


class PredictionExplainability(BaseModel):
    model_config = ConfigDict(extra='forbid')

    metadata: ExplainabilityMetadata
    top_influential_features: list[FeatureContribution]
    shap: ShapExplanation | None = None
    lime: LimeExplanation | None = None
