"""Process-local service dependencies."""

from functools import lru_cache

from config import get_settings
from inference.production_model_service import ProductionModelService


@lru_cache
def get_production_model_service() -> ProductionModelService:
    return ProductionModelService(get_settings().model_package_directory)
