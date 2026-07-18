"""Synthetic-fixture tests for the Phase 3.7 baseline experiment framework."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


ML_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ML_ROOT / "src"))

from experiments.artifacts import RAW_DATA_DIRECTORY, assert_experiment_output_path
from experiments.config import ExperimentConfig
from experiments.cross_validation import build_cross_validation_folds
from experiments.exceptions import ExperimentConfigurationError, ExperimentGovernanceError, ExperimentInputError
from experiments.models import ExperimentDocument
from experiments.runner import ExperimentContext, ExperimentRunner
from experiments.registry import LocalExperimentRegistry
from experiments.tracking import generate_experiment_id
from features.config import FeatureConfig
from models.factory import BaselineModelFactory


EXPERIMENT_CONFIG_DIRECTORY = ML_ROOT / "config" / "experiments"
FEATURE_CONFIG_PATH = ML_ROOT / "config" / "features" / "tfidf-unigram-bigram-v1.json"


class ExperimentFrameworkTests(unittest.TestCase):
    def test_model_factory_allows_only_the_three_approved_baselines(self) -> None:
        factory = BaselineModelFactory()
        self.assertEqual(
            factory._registry.names,
            ("linear_svm", "logistic_regression", "multinomial_naive_bayes"),
        )
        invalid = _experiment_config("logistic-regression-v1.json", model="random_forest")

        with self.assertRaises(ExperimentConfigurationError):
            factory.create(invalid, seed=42)

    def test_default_cross_validation_is_five_fold_stratified_and_reproducible(self) -> None:
        config = _experiment_config("logistic-regression-v1.json")
        labels = tuple(document.label for document in _documents())
        first = build_cross_validation_folds(labels, config.cross_validation, config.random_seed)
        second = build_cross_validation_folds(labels, config.cross_validation, config.random_seed)

        self.assertEqual(len(first), 5)
        self.assertEqual(first, second)
        self.assertEqual({index for fold in first for index in fold.validation_indices}, set(range(len(labels))))

    def test_grouped_cross_validation_never_splits_a_group_across_train_and_validation(self) -> None:
        config = _experiment_config(
            "logistic-regression-v1.json",
            cross_validation={"strategy": "stratified_group_kfold", "n_splits": 3, "shuffle": True},
        )
        documents = _documents()
        groups = tuple(document.group for document in documents)
        folds = build_cross_validation_folds(
            tuple(document.label for document in documents),
            config.cross_validation,
            config.random_seed,
            groups,
        )

        for fold in folds:
            train_groups = {groups[index] for index in fold.train_indices}
            validation_groups = {groups[index] for index in fold.validation_indices}
            self.assertFalse(train_groups & validation_groups)

    def test_all_three_baselines_train_cross_validate_and_write_candidate_records(self) -> None:
        feature_config = FeatureConfig.from_json_file(FEATURE_CONFIG_PATH)
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source_manifest = root / "approved-training-manifest.json"
            source_manifest.write_text('{"fixture": true}\n', encoding="utf-8")
            context = ExperimentContext(
                dataset_version="fixture-derivative-v1",
                split_id="SPL-FIXTURE-001",
                preprocessing_version="1.0.0",
                preprocessing_configuration_sha256="fixture-preprocessing-config-sha256",
                source_manifest_path=source_manifest,
                notes="Synthetic fixture only; not a research model result.",
                dataset_hash="a" * 64,
            )
            completed_models: set[str] = set()
            for filename in (
                "logistic-regression-v1.json",
                "multinomial-naive-bayes-v1.json",
                "linear-svm-v1.json",
            ):
                experiment, artifacts = ExperimentRunner(
                    _experiment_config(filename), feature_config
                ).run_and_write(
                    context=context,
                    documents=_documents(),
                    output_root=root / "experiments",
                )
                completed_models.add(experiment.model)
                self.assertTrue(experiment.experiment_id.startswith("EXP-"))
                self.assertEqual(len(experiment.fold_results), 5)
                self.assertIsNotNone(experiment.aggregate_metrics.roc_auc)
                self.assertTrue(Path(artifacts["manifest"]).is_file())
                self.assertTrue(Path(artifacts["config"]).is_file())
                self.assertTrue(Path(artifacts["metrics"]).is_file())
                self.assertTrue(Path(artifacts["classification_report"]).is_file())
                self.assertTrue(Path(artifacts["notes"]).is_file())
                self.assertEqual(Path(artifacts["confusion_matrix"]).read_bytes()[:8], b"\x89PNG\r\n\x1a\n")
                registry = json.loads(Path(artifacts["model_registry"]).read_text(encoding="utf-8"))
                self.assertEqual(registry["status"], "candidate")
                self.assertEqual(registry["experiment_id"], experiment.experiment_id)
                self.assertEqual(registry["dataset_hash"], "a" * 64)
                self.assertEqual(registry["feature_engineering_version"], "1.0.0")
            experiment_entries = LocalExperimentRegistry().discover(root / "experiments")
            self.assertEqual(len(experiment_entries), 3)
            self.assertTrue(all(entry.dataset_hash == "a" * 64 for entry in experiment_entries))
            self.assertEqual(
                completed_models,
                {"logistic_regression", "multinomial_naive_bayes", "linear_svm"},
            )

    def test_experiment_ids_are_unique(self) -> None:
        self.assertNotEqual(
            generate_experiment_id("logistic_regression"),
            generate_experiment_id("logistic_regression"),
        )

    def test_raw_paths_and_noncanonical_cli_output_roots_are_rejected(self) -> None:
        config = _experiment_config("logistic-regression-v1.json")
        feature_config = FeatureConfig.from_json_file(FEATURE_CONFIG_PATH)
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            context = ExperimentContext(
                dataset_version="fixture-derivative-v1",
                split_id="SPL-FIXTURE-001",
                preprocessing_version="1.0.0",
                preprocessing_configuration_sha256="fixture-preprocessing-config-sha256",
                source_manifest_path=RAW_DATA_DIRECTORY / "bharatfakenewskosh-v1.zip",
                notes="Fixture safeguard.",
                dataset_hash="a" * 64,
            )
            with self.assertRaises(ExperimentGovernanceError):
                ExperimentRunner(config, feature_config).run_and_write(
                    context=context,
                    documents=_documents(),
                    output_root=root / "experiments",
                )
            with self.assertRaises(ExperimentGovernanceError):
                assert_experiment_output_path(root / "outside-canonical-root")

    def test_dataset_hash_must_be_a_sha256_value(self) -> None:
        config = _experiment_config("logistic-regression-v1.json")
        feature_config = FeatureConfig.from_json_file(FEATURE_CONFIG_PATH)
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source_manifest = root / "approved-training-manifest.json"
            source_manifest.write_text('{"fixture": true}\n', encoding="utf-8")
            context = ExperimentContext(
                dataset_version="fixture-derivative-v1",
                split_id="SPL-FIXTURE-001",
                preprocessing_version="1.0.0",
                preprocessing_configuration_sha256="fixture-preprocessing-config-sha256",
                source_manifest_path=source_manifest,
                notes="Fixture validation safeguard.",
                dataset_hash="not-a-sha256",
            )
            with self.assertRaises(ExperimentInputError):
                ExperimentRunner(config, feature_config).run_and_write(
                    context=context,
                    documents=_documents(),
                    output_root=root / "experiments",
                )


def _experiment_config(filename: str, **overrides: object) -> ExperimentConfig:
    payload = json.loads((EXPERIMENT_CONFIG_DIRECTORY / filename).read_text(encoding="utf-8"))
    payload.update(overrides)
    return ExperimentConfig.from_mapping(payload)


def _documents() -> tuple[ExperimentDocument, ...]:
    documents: list[ExperimentDocument] = []
    for index in range(6):
        documents.append(
            ExperimentDocument(
                document_id=f"real-{index}",
                processed_text=f"verified official report confirmed source{index}",
                label=0,
                group=f"real-group-{index // 2}",
            )
        )
        documents.append(
            ExperimentDocument(
                document_id=f"fake-{index}",
                processed_text=f"fabricated viral rumor false claim{index}",
                label=1,
                group=f"fake-group-{index // 2}",
            )
        )
    return tuple(documents)


if __name__ == "__main__":
    unittest.main()
