from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from api.dependencies import get_production_model_service
from api.health import router as health_router
from api.prediction import router as prediction_router
from config import get_settings
from logging_config import configure_logging, get_logger
from inference.production_model_service import ModelPackageError


settings = get_settings()
configure_logging(settings.log_level)
logger = get_logger()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    logger.info(
        'ml_service_started',
        extra={'event': 'ml_service_started', 'environment': settings.environment, 'host': settings.host, 'port': settings.port, 'model_loading_mode': settings.model_loading_mode},
    )
    if settings.model_loading_mode == 'eager':
        try:
            get_production_model_service().ensure_loaded()
            logger.info('model_loaded_at_startup', extra={'event': 'model_loaded_at_startup'})
        except Exception as error:
            logger.error('model_load_failed_at_startup', extra={'event': 'model_load_failed_at_startup', 'error_type': type(error).__name__})
    yield
    logger.info('ml_service_stopped', extra={'event': 'ml_service_stopped'})


app = FastAPI(
    title=settings.service_name,
    version=settings.service_version,
    lifespan=lifespan,
)
app.include_router(health_router)
app.include_router(prediction_router)


@app.exception_handler(ModelPackageError)
async def model_package_error_handler(request: Request, error: ModelPackageError) -> JSONResponse:
    status_code = 422 if error.code == 'EMPTY_PROCESSED_INPUT' else 503
    return JSONResponse(
        status_code=status_code,
        content={'error': {'code': error.code, 'message': error.message}, 'request_id': request.headers.get('x-request-id')},
    )


@app.exception_handler(RequestValidationError)
async def request_validation_error_handler(request: Request, _error: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={'error': {'code': 'VALIDATION_ERROR', 'message': 'Request validation failed.'}, 'request_id': request.headers.get('x-request-id')},
    )


@app.exception_handler(Exception)
async def unexpected_error_handler(request: Request, error: Exception) -> JSONResponse:
    logger.exception('ml_service_unhandled_error', extra={'event': 'ml_service_unhandled_error', 'error_type': type(error).__name__})
    return JSONResponse(
        status_code=500,
        content={'error': {'code': 'INTERNAL_SERVER_ERROR', 'message': 'An unexpected error occurred.'}, 'request_id': request.headers.get('x-request-id')},
    )
