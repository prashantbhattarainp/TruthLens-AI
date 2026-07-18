"""Small immutable data models for request-time preprocessing."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class InputDocument:
    document_id: str
    text: str


@dataclass(frozen=True)
class ProcessedDocument:
    document_id: str
    source_text_sha256: str
    processed_text: str
    tokens: tuple[str, ...]
