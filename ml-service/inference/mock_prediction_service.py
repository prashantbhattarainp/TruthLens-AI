from schemas.prediction import PredictionExplanation, PredictionResponse


def create_mock_prediction() -> PredictionResponse:
    """Return fixed contract data until a real inference pipeline is introduced."""
    return PredictionResponse(
        prediction="Fake",
        confidence=0.87,
        risk_level="high",
        explanation=PredictionExplanation(
            summary="Deterministic mock explanation for API-contract verification only.",
            reasons=[
                "Sensational language detected",
                "Clickbait patterns",
                "Unverified claims",
                "Emotional wording",
            ],
        ),
        keywords=["breaking", "shocking", "viral", "urgent", "exclusive"],
        processing_time_ms=42,
        model="mock-logistic-regression",
        model_version="0.1.0-mock",
        dataset_version="indian-digital-media-demo-v1",
    )
