"""Process-local service dependencies."""

from functools import lru_cache

from config import get_settings
from explainability.configuration import ExplainabilityConfiguration
from explainability.service import ExplanationService
from inference.production_model_service import ProductionModelService


@lru_cache
def get_production_model_service() -> ProductionModelService:
    return ProductionModelService(get_settings().model_package_directory)


@lru_cache
def get_explanation_service() -> ExplanationService:
    return ExplanationService(
        get_production_model_service(),
        ExplainabilityConfiguration.from_settings(get_settings()),
    )
