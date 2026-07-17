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


@dataclass(frozen=True)
class Settings:
    environment: str
    host: str
    port: int
    log_level: str
    service_name: str


@lru_cache
def get_settings() -> Settings:
    return Settings(
        environment=os.getenv('ML_SERVICE_ENV', 'development'),
        host=os.getenv('ML_SERVICE_HOST', '127.0.0.1'),
        port=_read_port(os.getenv('ML_SERVICE_PORT')),
        log_level=os.getenv('LOG_LEVEL', 'INFO').upper(),
        service_name='TruthLens ML Service',
    )
