"""Internal model readiness and lineage endpoints."""

from fastapi import APIRouter, Header
from fastapi.responses import JSONResponse

from api.dependencies import get_production_model_service
from config import get_settings
from inference.production_model_service import ModelPackageError
from logging_config import get_logger


router = APIRouter(tags=['model'])
logger = get_logger()


@router.get('/ready')
def ready(x_request_id: str | None = Header(default=None)) -> dict[str, object]:
    service = get_production_model_service()
    try:
        service.ensure_loaded()
    except ModelPackageError as error:
        logger.warning('model_readiness_failed', extra={'event': 'model_readiness_failed', 'request_id': x_request_id, 'code': error.code})
        return JSONResponse(
            content={'status': 'not_ready', 'error': {'code': error.code, 'message': error.message}},
            status_code=503,
        )
    metadata = service.metadata()
    return {
        'status': 'ready',
        'model_loaded': True,
        'model_version': metadata['model_version'],
        'deployment_status': metadata['deployment_status'],
    }


@router.get('/metadata')
def metadata() -> dict[str, object]:
    service = get_production_model_service()
    service.ensure_loaded()
    metadata = service.metadata()
    return {
        'model_name': metadata['model_name'],
        'model_version': metadata['model_version'],
        'deployment_status': metadata['deployment_status'],
        'dataset_version': metadata['dataset_version'],
        'feature_engineering_version': metadata['feature_engineering_version'],
        'preprocessing_version': metadata['preprocessing_version'],
        'training_timestamp': metadata['training_timestamp'],
        'experiment_id': metadata['experiment_id'],
        'optimization_id': metadata['optimization_id'],
        'metrics_summary': metadata['metrics_summary'],
        'limitations': metadata['limitations'],
    }


@router.get('/version')
def version() -> dict[str, object]:
    settings = get_settings()
    service = get_production_model_service()
    metadata = service.metadata()
    return {
        'service': settings.service_name,
        'service_version': settings.service_version,
        'environment': settings.environment,
        'model_status': service.status,
        'model_version': metadata.get('model_version'),
        'deployment_status': metadata.get('deployment_status'),
    }
