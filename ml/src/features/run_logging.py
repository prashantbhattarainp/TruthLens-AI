"""Structured event logging for feature-extraction runs."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class FeatureRunLogger:
    """Accumulates JSON-safe events before one atomic artifact-writing step."""

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
