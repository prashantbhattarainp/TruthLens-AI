from fastapi import APIRouter

from api.dependencies import get_production_model_service
from config import get_settings


router = APIRouter()


@router.get('/health', tags=['health'])
def get_health() -> dict[str, object]:
    settings = get_settings()
    service = get_production_model_service()
    metadata = service.metadata()

    return {
        'service': settings.service_name,
        'status': 'healthy',
        'model_loaded': service.is_loaded,
        'model_status': service.status,
        'model_version': metadata.get('model_version'),
        'deployment_status': metadata.get('deployment_status'),
    }
