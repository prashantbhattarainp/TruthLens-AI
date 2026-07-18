"""Model-candidate registry records derived from complete experiment bundles."""

from __future__ import annotations

from pathlib import Path

from experiments.models import ExperimentRecord, ModelRegistryRecord


def build_candidate_model_record(
    experiment: ExperimentRecord,
    artifact_directory: Path,
) -> ModelRegistryRecord:
    """Create a candidate entry without claiming held-out evaluation or research approval."""
    model_token = experiment.model.replace("_", "-")
    return ModelRegistryRecord(
        model_id=f"MDL-{model_token}-{experiment.model_version}-{experiment.experiment_id}",
        model_version=experiment.model_version,
        status="candidate",
        dataset_version=experiment.dataset_version,
        dataset_hash=experiment.dataset_hash,
        feature_engineering_version=experiment.feature_engineering_version,
        feature_configuration_sha256=experiment.feature_configuration_sha256,
        experiment_id=experiment.experiment_id,
        performance_metrics=experiment.aggregate_metrics,
        artifact_location=str(artifact_directory.resolve()),
        training_date=experiment.completed_at,
        notes=experiment.notes,
    )
