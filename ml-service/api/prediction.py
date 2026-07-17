from fastapi import APIRouter, Header

from inference.mock_prediction_service import create_mock_prediction
from logging_config import get_logger
from schemas.prediction import PredictionRequest, PredictionResponse


router = APIRouter()
logger = get_logger()


@router.post("/predict", response_model=PredictionResponse, tags=["prediction"])
def predict(
    request: PredictionRequest,
    x_request_id: str | None = Header(default=None),
) -> PredictionResponse:
    logger.info(
        "prediction_request_received request_id=%s headline_length=%s article_length=%s",
        x_request_id,
        len(request.headline),
        len(request.article),
    )

    prediction = create_mock_prediction()

    logger.info(
        "prediction_response_sent request_id=%s prediction=%s processing_time_ms=%s",
        x_request_id,
        prediction.prediction,
        prediction.processing_time_ms,
    )

    return prediction
