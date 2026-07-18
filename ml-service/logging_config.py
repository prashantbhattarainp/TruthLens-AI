import json
import logging
from datetime import datetime, timezone


class JsonFormatter(logging.Formatter):
    """Render safe structured events without request text or other user content."""

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
        }
        for key, value in record.__dict__.items():
            if key.startswith('_') or key in _LOG_RECORD_FIELDS:
                continue
            payload[key] = value
        return json.dumps(payload, ensure_ascii=False, default=str)


_LOG_RECORD_FIELDS = frozenset(logging.makeLogRecord({}).__dict__)


def configure_logging(log_level: str) -> None:
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    logging.basicConfig(level=log_level, handlers=[handler], force=True)


def get_logger() -> logging.Logger:
    return logging.getLogger('truthlens.ml_service')
