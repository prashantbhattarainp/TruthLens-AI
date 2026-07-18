import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv


load_dotenv(Path(__file__).resolve().parent / '.env')


def _read_port(value: str | None) -> int:
    port = int(value or '8000')
    if not 1 <= port <= 65535:
        raise ValueError('ML_SERVICE_PORT must be between 1 and 65535.')
    return port


def _read_environment(value: str | None) -> str:
    environment = (value or 'development').strip().lower()
    if environment not in {'development', 'testing', 'production'}:
        raise ValueError('ML_SERVICE_ENV must be development, testing, or production.')
    return environment


def _read_loading_mode(value: str | None, environment: str) -> str:
    mode = (value or ('eager' if environment == 'production' else 'lazy')).strip().lower()
    if mode not in {'lazy', 'eager'}:
        raise ValueError('MODEL_LOADING_MODE must be lazy or eager.')
    return mode


def _read_package_directory(value: str | None) -> Path:
    default = Path(__file__).resolve().parent / 'artifacts' / 'candidate' / 'TL-LSVM-TFIDF-v1.1.0-rc.1'
    return Path(value).expanduser().resolve() if value else default.resolve()


@dataclass(frozen=True)
class Settings:
    environment: str
    host: str
    port: int
    log_level: str
    service_name: str
    model_package_directory: Path
    model_loading_mode: str
    service_version: str


@lru_cache
def get_settings() -> Settings:
    environment = _read_environment(os.getenv('ML_SERVICE_ENV'))
    return Settings(
        environment=environment,
        host=os.getenv('ML_SERVICE_HOST', '127.0.0.1'),
        port=_read_port(os.getenv('ML_SERVICE_PORT')),
        log_level=os.getenv('LOG_LEVEL', 'INFO').upper(),
        service_name='TruthLens ML Service',
        model_package_directory=_read_package_directory(os.getenv('MODEL_PACKAGE_DIR')),
        model_loading_mode=_read_loading_mode(os.getenv('MODEL_LOADING_MODE'), environment),
        service_version=os.getenv('ML_SERVICE_VERSION', '0.2.0'),
    )
