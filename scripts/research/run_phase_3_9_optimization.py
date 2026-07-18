"""Run all approved Phase 3.9 baseline searches against the governed r2 split."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

import sys

sys.path.insert(0, str(PROJECT_ROOT / "ml" / "src"))

from experiments.config import ExperimentConfig
from features.config import FeatureConfig
from optimization import OptimizationConfig, OptimizationContext, OptimizationDocument, OptimizationRunner


DATASET_VERSION = "TL-BFNK-EN-v1.0"
SPLIT_ID = "SPL-TL-BFNK-EN-v1.0"
PREPROCESSING_SHA256 = "52ce7a78fa4892adf302e3c4dcc0633aebc9dfb55ca4347647f1d1cd87d3976f"
BASELINE_EXPERIMENT_IDS = {
    "logistic_regression": "EXP-20260717-logistic-regression-e7612c6153",
    "multinomial_naive_bayes": "EXP-20260717-multinomial-naive-bayes-7869d12afd",
    "linear_svm": "EXP-20260717-linear-svm-177d71e9c9",
}
BASELINE_CONFIG_NAMES = {
    "logistic_regression": "logistic-regression-bfnk-en-v1.json",
    "multinomial_naive_bayes": "multinomial-naive-bayes-bfnk-en-v1.json",
    "linear_svm": "linear-svm-bfnk-en-v1.json",
}


def main() -> None:
    derivative = PROJECT_ROOT / "ml" / "data" / "derived" / DATASET_VERSION / "DER-20260718-r2"
    processed = PROJECT_ROOT / "ml" / "data" / "processed" / DATASET_VERSION / "PRE-20260718-r2"
    split = _split_metadata(derivative / "split-documents.jsonl")
    train, validation = _processed_partitions(processed / "processed-documents.jsonl", split)
    dataset_hash = _sha256(derivative / "split-documents.jsonl")
    feature_config = FeatureConfig.from_json_file(
        PROJECT_ROOT / "ml" / "config" / "features" / "tfidf-unigram-bigram-v1.json"
    )
    summaries: list[dict[str, object]] = []
    for path in sorted((PROJECT_ROOT / "ml" / "config" / "optimization").glob("*.json")):
        optimization_config = OptimizationConfig.from_json_file(path)
        model = optimization_config.model
        baseline_config = ExperimentConfig.from_json_file(
            PROJECT_ROOT / "ml" / "config" / "experiments" / BASELINE_CONFIG_NAMES[model]
        )
        baseline_experiment = (
            PROJECT_ROOT
            / "ml"
            / "data"
            / "experiments"
            / DATASET_VERSION
            / "phase-3-8-r2"
            / BASELINE_EXPERIMENT_IDS[model]
            / "experiment-record.json"
        )
        context = OptimizationContext(
            dataset_version=DATASET_VERSION,
            dataset_hash=dataset_hash,
            split_id=SPLIT_ID,
            preprocessing_version="1.0.0",
            preprocessing_configuration_sha256=PREPROCESSING_SHA256,
            source_manifest_path=derivative / "derivative-manifest.json",
            baseline_experiment_path=baseline_experiment,
            baseline_validation_result_path=(
                PROJECT_ROOT / "ml" / "data" / "evaluation" / DATASET_VERSION / "EVAL-20260718-r2" / "evaluation-result.json"
            ),
        )
        result, artifacts = OptimizationRunner(
            optimization_config, baseline_config, feature_config
        ).run_and_write(
            context=context,
            train_documents=train,
            validation_documents=validation,
            output_root=PROJECT_ROOT / "ml" / "data" / "optimization" / DATASET_VERSION / "phase-3-9-r1",
        )
        summaries.append(
            {
                "optimization_id": result["optimization_id"],
                "model": model,
                "best_parameters": result["search_analysis"]["best_parameters"],
                "best_cv_macro_f1": result["search_analysis"]["best_cv_macro_f1"],
                "validation_macro_f1": result["overfitting_analysis"]["validation_metrics"]["macro_f1"],
                "artifacts": artifacts,
            }
        )
    print(json.dumps(summaries, ensure_ascii=False, indent=2))


def _split_metadata(path: Path) -> dict[str, dict[str, object]]:
    metadata: dict[str, dict[str, object]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        value = json.loads(line)
        metadata[value["document_id"]] = {
            "label": value["label"],
            "group": value["duplicate_cluster_id"],
            "partition": value["partition"],
        }
    return metadata


def _processed_partitions(
    path: Path, split: dict[str, dict[str, object]]
) -> tuple[tuple[OptimizationDocument, ...], tuple[OptimizationDocument, ...]]:
    partitions: dict[str, list[OptimizationDocument]] = {"train": [], "validation": []}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        value = json.loads(line)
        metadata = split[value["document_id"]]
        partition = metadata["partition"]
        if partition not in partitions:
            continue
        partitions[partition].append(
            OptimizationDocument(
                document_id=value["document_id"],
                processed_text=value["processed_text"],
                label=int(metadata["label"]),
                group=str(metadata["group"]),
            )
        )
    return tuple(partitions["train"]), tuple(partitions["validation"])


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


if __name__ == "__main__":
    main()
