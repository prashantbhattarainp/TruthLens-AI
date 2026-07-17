from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.health import router as health_router
from api.prediction import router as prediction_router
from config import get_settings
from logging_config import configure_logging, get_logger


settings = get_settings()
configure_logging(settings.log_level)
logger = get_logger()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    logger.info(
        'ml_service_started environment=%s host=%s port=%s',
        settings.environment,
        settings.host,
        settings.port,
    )
    yield
    logger.info('ml_service_stopped')


app = FastAPI(
    title=settings.service_name,
    version='0.1.0',
    lifespan=lifespan,
)
app.include_router(health_router)
app.include_router(prediction_router)
