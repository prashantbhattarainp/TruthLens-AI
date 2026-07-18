"""CLI adapter for an approved labelled preprocessed training partition."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from experiments.artifacts import assert_experiment_output_path, assert_not_raw_path
from experiments.config import ExperimentConfig
from experiments.models import ExperimentDocument
from experiments.runner import ExperimentContext, ExperimentRunner
from features.config import FeatureConfig


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run a TruthLens cross-validated baseline model on an approved training partition."
    )
    parser.add_argument("--experiment-config", required=True, type=Path)
    parser.add_argument("--feature-config", required=True, type=Path)
    parser.add_argument("--training-jsonl", required=True, type=Path)
    parser.add_argument("--source-manifest", required=True, type=Path)
    parser.add_argument("--dataset-version", required=True)
    parser.add_argument("--dataset-hash", required=True)
    parser.add_argument("--split-id", required=True)
    parser.add_argument("--preprocessing-version", required=True)
    parser.add_argument("--preprocessing-configuration-sha256", required=True)
    parser.add_argument("--notes", default="")
    parser.add_argument("--output-root", required=True, type=Path)
    args = parser.parse_args()

    assert_not_raw_path(args.training_jsonl)
    assert_not_raw_path(args.source_manifest)
    assert_experiment_output_path(args.output_root)
    experiment_config = ExperimentConfig.from_json_file(args.experiment_config)
    feature_config = FeatureConfig.from_json_file(args.feature_config)
    context = ExperimentContext(
        dataset_version=args.dataset_version,
        split_id=args.split_id,
        preprocessing_version=args.preprocessing_version,
        preprocessing_configuration_sha256=args.preprocessing_configuration_sha256,
        source_manifest_path=args.source_manifest,
        notes=args.notes,
        dataset_hash=args.dataset_hash,
    )
    experiment, artifacts = ExperimentRunner(experiment_config, feature_config).run_and_write(
        context=context,
        documents=tuple(_read_training_documents(args.training_jsonl)),
        output_root=args.output_root,
    )
    print(json.dumps({"experiment": experiment.to_dict(), "artifacts": artifacts}, ensure_ascii=False, indent=2))


def _read_training_documents(path: Path):
    required = {"document_id", "processed_text", "label"}
    permitted = required | {"group"}
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        value = json.loads(line)
        if set(value) not in {required, permitted}:
            raise ValueError(f"{path}:{line_number} does not match the approved training-document schema.")
        if (
            not isinstance(value["document_id"], str)
            or not isinstance(value["processed_text"], str)
            or value["label"] not in {0, 1}
        ):
            raise ValueError(f"{path}:{line_number} has invalid document_id, processed_text, or label values.")
        yield ExperimentDocument(
            document_id=value["document_id"],
            processed_text=value["processed_text"],
            label=value["label"],
            group=value.get("group"),
        )


if __name__ == "__main__":
    main()
