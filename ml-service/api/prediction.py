from fastapi import APIRouter, Header

from api.dependencies import get_explanation_service
from logging_config import get_logger
from schemas.prediction import PredictionExplanation, PredictionRequest, PredictionResponse


router = APIRouter()
logger = get_logger()


@router.post('/predict', response_model=PredictionResponse, tags=['prediction'])
def predict(request: PredictionRequest, x_request_id: str | None = Header(default=None)) -> PredictionResponse:
    logger.info('prediction_request_received', extra={'event': 'prediction_request_received', 'request_id': x_request_id, 'headline_length': len(request.headline), 'article_length': len(request.article)})
    explained_prediction = get_explanation_service().predict_and_explain(headline=request.headline, article=request.article)
    prediction = explained_prediction.prepared_prediction.prediction
    response = PredictionResponse(
        prediction=prediction.label,
        explanation=PredictionExplanation(
            summary='AI-assisted content assessment. Verify important information independently.',
            reasons=[
                'Use this classification as a review signal, not a factual verdict.',
                'Check claims against credible, independent sources before sharing or acting on them.',
                'Contributing words describe the automated classification and do not establish certainty.',
            ],
        ),
        keywords=explained_prediction.keywords,
        processing_time_ms=explained_prediction.processing_time_ms,
        explainability=explained_prediction.explainability,
    )
    logger.info('prediction_response_sent', extra={'event': 'prediction_response_sent', 'request_id': x_request_id, 'prediction': response.prediction, 'explainability_status': response.explainability.metadata.status if response.explainability else None, 'latency_ms': response.processing_time_ms, 'status': 'success'})
    return response
