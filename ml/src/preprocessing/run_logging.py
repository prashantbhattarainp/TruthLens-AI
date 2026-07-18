"""Structured JSON Lines logging for preprocessing runs."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class RunEvent:
    event: str
    at: str
    payload: dict[str, Any]

    def to_json_line(self) -> str:
        return json.dumps(
            {"event": self.event, "at": self.at, **self.payload},
            ensure_ascii=False,
            sort_keys=True,
        )


class PreprocessingRunLogger:
    """Collect auditable events and emit them beside one processed-data run."""

    def __init__(self) -> None:
        self._events: list[RunEvent] = []

    def record(self, event: str, **payload: Any) -> None:
        self._events.append(
            RunEvent(event=event, at=datetime.now(timezone.utc).isoformat(), payload=payload)
        )

    def write_jsonl(self, path: Path) -> None:
        path.write_text("\n".join(event.to_json_line() for event in self._events) + "\n", encoding="utf-8")
