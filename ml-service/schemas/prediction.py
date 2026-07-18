from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class PredictionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    headline: str = Field(min_length=1, max_length=300)
    article: str = Field(min_length=100, max_length=15000)


class PredictionExplanation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    summary: str
    reasons: list[str]


class PredictionResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    prediction: Literal["Real", "Fake"]
    confidence: None = None
    confidence_status: Literal["unavailable"]
    decision_score: float
    risk_level: Literal["not_assessed"]
    explanation: PredictionExplanation
    keywords: list[str]
    processing_time_ms: int = Field(ge=0)
    model: str
    model_version: str
    dataset_version: str
