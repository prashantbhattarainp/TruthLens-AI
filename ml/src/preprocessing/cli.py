"""Minimal command-line adapter for approved JSONL derivative inputs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from preprocessing.artifacts import assert_not_raw_input
from preprocessing.config import PreprocessingConfig
from preprocessing.models import InputDocument
from preprocessing.runner import PreprocessingRunner


def main() -> None:
    parser = argparse.ArgumentParser(description="Run TruthLens preprocessing on an approved derivative.")
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--input-jsonl", required=True, type=Path)
    parser.add_argument("--source-manifest", required=True, type=Path)
    parser.add_argument("--dataset-version", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--output-directory", required=True, type=Path)
    args = parser.parse_args()

    assert_not_raw_input(args.input_jsonl)
    assert_not_raw_input(args.source_manifest)
    config = PreprocessingConfig.from_json_file(args.config)
    documents = tuple(_read_documents(args.input_jsonl))
    run, artifacts = PreprocessingRunner(config).run(
        run_id=args.run_id,
        dataset_version=args.dataset_version,
        source_manifest_path=args.source_manifest,
        documents=documents,
        output_directory=args.output_directory,
    )
    print(json.dumps({"run": run.to_dict(), "artifacts": artifacts}, ensure_ascii=False, indent=2))


def _read_documents(path: Path):
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        value = json.loads(line)
        if set(value) != {"id", "text"} or not isinstance(value["id"], str) or not isinstance(value["text"], str):
            raise ValueError(f"{path}:{line_number} must contain exactly string id and text fields.")
        yield InputDocument(document_id=value["id"], text=value["text"])


if __name__ == "__main__":
    main()
