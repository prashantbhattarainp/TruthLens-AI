from fastapi import APIRouter, Header

from api.dependencies import get_explanation_service, get_production_model_service
from logging_config import get_logger
from schemas.prediction import PredictionExplanation, PredictionRequest, PredictionResponse


router = APIRouter()
logger = get_logger()


@router.post("/predict", response_model=PredictionResponse, tags=["prediction"])
def predict(
    request: PredictionRequest,
    x_request_id: str | None = Header(default=None),
) -> PredictionResponse:
    logger.info(
        "prediction_request_received",
        extra={
            'event': 'prediction_request_received',
            'request_id': x_request_id,
            'headline_length': len(request.headline),
            'article_length': len(request.article),
        },
    )

    service = get_production_model_service()
    explained_prediction = get_explanation_service().predict_and_explain(
        headline=request.headline,
        article=request.article,
    )
    prediction = explained_prediction.prepared_prediction.prediction
    metadata = service.metadata()
    response = PredictionResponse(
        prediction=prediction.label,
        confidence=None,
        confidence_status='unavailable',
        decision_score=prediction.decision_score,
        risk_level='not_assessed',
        explanation=PredictionExplanation(
            summary='Limited research classification signal only; it is not a factual verdict.',
            reasons=[
                'The Linear SVM score is not a calibrated probability.',
                'This candidate is untested after tuning and is not deployment-approved.',
                'Results are limited to the governed English research scope and require human review.',
            ],
        ),
        keywords=explained_prediction.keywords,
        processing_time_ms=explained_prediction.processing_time_ms,
        model=metadata['model_name'],
        model_version=metadata['model_version'],
        dataset_version=metadata['dataset_version'],
        explainability=explained_prediction.explainability,
    )

    logger.info(
        "prediction_response_sent",
        extra={
            'event': 'prediction_response_sent',
            'request_id': x_request_id,
            'prediction': response.prediction,
            'decision_score_recorded': True,
            'confidence_status': response.confidence_status,
            'explainability_status': response.explainability.metadata.status if response.explainability else None,
            'latency_ms': response.processing_time_ms,
            'model_version': response.model_version,
            'status': 'success',
        },
    )

    return response
