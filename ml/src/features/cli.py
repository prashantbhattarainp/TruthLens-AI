"""Command-line adapter for approved, preprocessed-document feature inputs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from features.artifacts import assert_feature_output_path, assert_not_raw_path
from features.config import FeatureConfig
from features.models import FeatureDocument
from features.runner import FeatureRunner


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fit a TruthLens feature representation on an approved preprocessed training partition."
    )
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--input-jsonl", required=True, type=Path)
    parser.add_argument("--source-manifest", required=True, type=Path)
    parser.add_argument("--experiment-id", required=True)
    parser.add_argument("--dataset-version", required=True)
    parser.add_argument("--split-id", required=True)
    parser.add_argument("--fit-partition", required=True)
    parser.add_argument("--notes", default="")
    parser.add_argument("--output-directory", required=True, type=Path)
    args = parser.parse_args()

    assert_not_raw_path(args.input_jsonl)
    assert_not_raw_path(args.source_manifest)
    assert_feature_output_path(args.output_directory)
    config = FeatureConfig.from_json_file(args.config)
    experiment, artifacts = FeatureRunner(config).fit_and_write(
        experiment_id=args.experiment_id,
        dataset_version=args.dataset_version,
        split_id=args.split_id,
        fit_partition=args.fit_partition,
        source_manifest_path=args.source_manifest,
        documents=tuple(_read_preprocessed_documents(args.input_jsonl)),
        notes=args.notes,
        output_directory=args.output_directory,
    )
    print(json.dumps({"experiment": experiment.to_dict(), "artifacts": artifacts}, ensure_ascii=False, indent=2))


def _read_preprocessed_documents(path: Path):
    required = {"document_id", "source_text_sha256", "processed_text", "tokens"}
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        value = json.loads(line)
        if set(value) != required:
            raise ValueError(
                f"{path}:{line_number} must contain exactly the approved processed-document schema."
            )
        if not isinstance(value["document_id"], str) or not isinstance(value["processed_text"], str):
            raise ValueError(f"{path}:{line_number} has invalid document_id or processed_text values.")
        yield FeatureDocument(document_id=value["document_id"], processed_text=value["processed_text"])


if __name__ == "__main__":
    main()
