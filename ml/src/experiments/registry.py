"""Filesystem-backed local experiment registry inspired by immutable MLflow runs."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from experiments.models import ExperimentRecord


@dataclass(frozen=True)
class ExperimentRegistryEntry:
    """Small discoverable index record that points to one self-contained experiment bundle."""

    experiment_id: str
    status: str
    timestamp: str
    dataset_version: str
    dataset_hash: str
    model: str
    model_version: str
    primary_metric: str
    macro_f1: float
    artifact_location: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_experiment_registry_entry(
    experiment: ExperimentRecord,
    artifact_directory: Path,
) -> ExperimentRegistryEntry:
    """Create an immutable entry written beside—not instead of—the complete experiment record."""
    return ExperimentRegistryEntry(
        experiment_id=experiment.experiment_id,
        status=experiment.status,
        timestamp=experiment.completed_at,
        dataset_version=experiment.dataset_version,
        dataset_hash=experiment.dataset_hash,
        model=experiment.model,
        model_version=experiment.model_version,
        primary_metric="macro_f1",
        macro_f1=experiment.aggregate_metrics.macro_f1,
        artifact_location=str(artifact_directory.resolve()),
    )


class LocalExperimentRegistry:
    """Discovers self-contained local run entries without a mutable shared database or service."""

    def discover(self, root: Path) -> tuple[ExperimentRegistryEntry, ...]:
        """Return all valid registry entries below an experiment-output root in stable order."""
        if not root.exists():
            return ()
        entries: list[ExperimentRegistryEntry] = []
        for path in sorted(root.rglob("experiment-registry-entry.json")):
            value = json.loads(path.read_text(encoding="utf-8"))
            entries.append(
                ExperimentRegistryEntry(
                    experiment_id=value["experiment_id"],
                    status=value["status"],
                    timestamp=value["timestamp"],
                    dataset_version=value["dataset_version"],
                    dataset_hash=value.get("dataset_hash"),
                    model=value["model"],
                    model_version=value["model_version"],
                    primary_metric=value["primary_metric"],
                    macro_f1=float(value["macro_f1"]),
                    artifact_location=value["artifact_location"],
                )
            )
        return tuple(entries)
