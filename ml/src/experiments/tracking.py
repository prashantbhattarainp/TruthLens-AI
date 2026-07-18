"""Unique experiment identifiers and structured lifecycle-event logging."""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def generate_experiment_id(model: str, now: datetime | None = None) -> str:
    """Generate a collision-resistant immutable ID without relying on a mutable global counter."""
    timestamp = now or datetime.now(timezone.utc)
    model_token = model.replace("_", "-")
    return f"EXP-{timestamp:%Y%m%d}-{model_token}-{uuid.uuid4().hex[:10]}"


class ExperimentRunLogger:
    """Accumulates JSON-safe experiment lifecycle events for one artifact bundle."""

    def __init__(self) -> None:
        self._events: list[dict[str, Any]] = []

    def record(self, event: str, **fields: Any) -> None:
        self._events.append(
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "event": event,
                **fields,
            }
        )

    def write_jsonl(self, path: Path) -> None:
        path.write_text(
            "\n".join(json.dumps(event, ensure_ascii=False, sort_keys=True) for event in self._events) + "\n",
            encoding="utf-8",
        )
