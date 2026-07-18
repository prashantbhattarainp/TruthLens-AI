"""Focused tests for the Phase 3.8 governed materialization and hold-out evaluator."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd


ML_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ML_ROOT / "src"))

from datasets.materialize import _assign_partitions, _text_or_empty, _validate_partition_integrity
from evaluation import BaselineEvaluationRunner, EvaluationDocument
from experiments.config import ExperimentConfig
from features.config import FeatureConfig


class DatasetMaterializationAndEvaluationTests(unittest.TestCase):
    def test_missing_spreadsheet_text_is_empty_not_literal_nan(self) -> None:
        self.assertEqual(_text_or_empty(float("nan")), "")
        self.assertEqual(_text_or_empty(pd.NA), "")
        self.assertEqual(_text_or_empty("statement"), "statement")

    def test_grouped_allocator_preserves_groups_and_distributes_strata(self) -> None:
        records = []
        for label in (0, 1):
            for number in range(20):
                group = f"group-{label}-{number}"
                records.append({"duplicate_cluster_id": group, "label": label})
                if number < 5:
                    records.append({"duplicate_cluster_id": group, "label": label})
        _assign_partitions(records, {"ratios": {"train": 0.7, "validation": 0.15, "test": 0.15}, "random_seed": 42})
        _validate_partition_integrity(records)
        partitions = {record["partition"] for record in records}
        self.assertEqual(partitions, {"train", "validation", "test"})
        grouped = {}
        for record in records:
            grouped.setdefault(record["duplicate_cluster_id"], set()).add(record["partition"])
        self.assertTrue(all(len(value) == 1 for value in grouped.values()))

    def test_holdout_evaluator_selects_on_validation_and_writes_once(self) -> None:
        config_directory = ML_ROOT / "config" / "experiments"
        configs = tuple(
            ExperimentConfig.from_json_file(config_directory / name)
            for name in (
                "logistic-regression-bfnk-en-v1.json",
                "multinomial-naive-bayes-bfnk-en-v1.json",
                "linear-svm-bfnk-en-v1.json",
            )
        )
        feature_config = FeatureConfig.from_json_file(ML_ROOT / "config" / "features" / "tfidf-unigram-bigram-v1.json")
        train = tuple(_document("train", index, index % 2) for index in range(16))
        validation = tuple(_document("validation", index, index % 2) for index in range(6))
        test = tuple(_document("test", index, index % 2) for index in range(6))
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "evaluation"
            result = BaselineEvaluationRunner(feature_config).run_and_write(
                configs=configs,
                train=train,
                validation=validation,
                test=test,
                dataset_version="fixture-v1",
                split_id="SPL-FIXTURE-001",
                output_directory=output,
            )
            self.assertIn(result["selected_model"]["model"], {config.model for config in configs})
            self.assertTrue((output / "evaluation-result.json").exists())
            self.assertTrue((output / "selected-model.joblib").exists())
            self.assertIn("normalized_confusion_matrix", result["selected_model"]["test_result"]["metrics"])


def _document(partition: str, index: int, label: int) -> EvaluationDocument:
    class_token = "fake alert hoax" if label else "verified report factual"
    return EvaluationDocument(
        document_id=f"{partition}-{index}",
        processed_text=f"{class_token} repeated token {index % 3}",
        label=label,
        duplicate_cluster_id=f"{partition}-group-{index}",
        partition=partition,
        source="fixture-source",
        raw_character_count=64,
    )
