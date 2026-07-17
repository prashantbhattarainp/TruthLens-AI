from fastapi import APIRouter

from config import get_settings


router = APIRouter()


@router.get('/health', tags=['health'])
def get_health() -> dict[str, object]:
    settings = get_settings()

    return {
        'service': settings.service_name,
        'status': 'healthy',
        'model_loaded': False,
    }
