"""Fixture-based tests for the Phase 3.6 feature-engineering implementation."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np
from scipy.sparse import csr_matrix


ML_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ML_ROOT / "src"))

from features.artifacts import RAW_DATA_DIRECTORY
from features.config import FeatureConfig
from features.exceptions import FeatureGovernanceError
from features.extractors.base import FeatureExtractor
from features.models import FeatureDocument
from features.pipeline import FeaturePipeline
from features.registry import FeatureExtractorRegistry
from features.runner import FeatureRunner
from features.validation import validate_feature_matrix


COUNT_CONFIG_PATH = ML_ROOT / "config" / "features" / "count-unigram-v1.json"
TFIDF_CONFIG_PATH = ML_ROOT / "config" / "features" / "tfidf-unigram-bigram-v1.json"


class FeatureEngineeringTests(unittest.TestCase):
    def test_count_vectorizer_respects_binary_and_ngram_configuration(self) -> None:
        config = _config(COUNT_CONFIG_PATH, parameters={
            "ngram_range": [1, 2],
            "max_features": 50,
            "min_df": 1,
            "max_df": 1.0,
            "binary": True,
            "normalization": "none",
        })
        matrix = FeaturePipeline(config).fit_transform(_documents())

        self.assertEqual(matrix.method, "count")
        self.assertEqual(matrix.matrix.shape[0], 3)
        self.assertIn("verified claim", matrix.feature_names)
        self.assertEqual(matrix.matrix.data.max(), 1)

    def test_tfidf_vectorizer_respects_l2_normalization(self) -> None:
        matrix = FeaturePipeline(_config(TFIDF_CONFIG_PATH)).fit_transform(_documents())
        row_norms = np.sqrt(matrix.matrix.multiply(matrix.matrix).sum(axis=1)).A1

        self.assertEqual(matrix.method, "tfidf")
        self.assertTrue(np.allclose(row_norms, np.ones(3), atol=1e-6))
        self.assertGreater(matrix.vocabulary_size, 0)

    def test_custom_extractor_can_be_registered_without_changing_pipeline_code(self) -> None:
        config = FeatureConfig.from_mapping(
            {
                "feature_pipeline_version": "1.0.0",
                "method": "future-embedding",
                "parameters": {"dimension": 1},
                "validation": {
                    "max_empty_feature_vector_rate": 0.0,
                    "max_matrix_memory_mb": 1,
                    "require_nonempty_vocabulary": True,
                },
            }
        )
        registry = FeatureExtractorRegistry()
        registry.register("future-embedding", _FixtureExtractor)
        matrix = FeaturePipeline(config, registry).fit_transform(_documents())

        self.assertEqual(matrix.matrix.shape, (3, 1))
        self.assertEqual(matrix.feature_names, ("fixture_dimension",))

    def test_validation_flags_empty_feature_vectors(self) -> None:
        feature_matrix = FeaturePipeline(_config(COUNT_CONFIG_PATH)).fit_transform(
            (FeatureDocument("blank", ""), FeatureDocument("content", "verified claim"))
        )
        report = validate_feature_matrix(feature_matrix, _config(COUNT_CONFIG_PATH), processing_duration_ms=1)

        self.assertFalse(report.is_valid)
        self.assertEqual(report.empty_feature_vector_count, 1)
        self.assertFalse(report.checks["empty_feature_vector_rate_within_limit"])

    def test_runner_writes_matrix_validation_experiment_and_manifest_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source_manifest = root / "approved-preprocessing-manifest.json"
            source_manifest.write_text('{"fixture": true}\n', encoding="utf-8")
            output_directory = root / "features" / "fixture-run"
            experiment, artifacts = FeatureRunner(_config(TFIDF_CONFIG_PATH)).fit_and_write(
                experiment_id="EXP-FIXTURE-001",
                dataset_version="fixture-derivative-v1",
                split_id="SPL-FIXTURE-001",
                fit_partition="train",
                source_manifest_path=source_manifest,
                documents=_documents(),
                notes="Synthetic fixture only; not a research experiment.",
                output_directory=output_directory,
            )

            self.assertTrue(experiment.validation.is_valid)
            self.assertEqual(experiment.feature_method, "tfidf")
            self.assertTrue(Path(artifacts["matrix"]).is_file())
            self.assertTrue(Path(artifacts["extractor"]).is_file())
            manifest = json.loads(Path(artifacts["manifest"]).read_text(encoding="utf-8"))
            self.assertEqual(manifest["experiment_id"], "EXP-FIXTURE-001")
            self.assertEqual(len(Path(artifacts["log"]).read_text(encoding="utf-8").splitlines()), 2)

    def test_runner_rejects_raw_manifest_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            with self.assertRaises(FeatureGovernanceError):
                FeatureRunner(_config(COUNT_CONFIG_PATH)).fit_and_write(
                    experiment_id="EXP-FIXTURE-RAW",
                    dataset_version="fixture-derivative-v1",
                    split_id="SPL-FIXTURE-001",
                    fit_partition="train",
                    source_manifest_path=RAW_DATA_DIRECTORY / "bharatfakenewskosh-v1.zip",
                    documents=_documents(),
                    notes="Fixture raw-path safeguard.",
                    output_directory=Path(temporary_directory) / "features",
                )


class _FixtureExtractor(FeatureExtractor):
    method = "future-embedding"

    def __init__(self, _config: FeatureConfig) -> None:
        self._fitted = False

    def fit_transform(self, documents: list[str] | tuple[str, ...]) -> csr_matrix:
        self._fitted = True
        return csr_matrix(np.ones((len(documents), 1), dtype=np.float32))

    def transform(self, documents: list[str] | tuple[str, ...]) -> csr_matrix:
        if not self._fitted:
            raise RuntimeError("fixture extractor is not fitted")
        return csr_matrix(np.ones((len(documents), 1), dtype=np.float32))

    @property
    def feature_names(self) -> tuple[str, ...]:
        if not self._fitted:
            raise RuntimeError("fixture extractor is not fitted")
        return ("fixture_dimension",)


def _config(path: Path, **overrides: object) -> FeatureConfig:
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload.update(overrides)
    return FeatureConfig.from_mapping(payload)


def _documents() -> tuple[FeatureDocument, ...]:
    return (
        FeatureDocument("fixture-1", "verified claim verified"),
        FeatureDocument("fixture-2", "false claim detected"),
        FeatureDocument("fixture-3", "verified report detected"),
    )


if __name__ == "__main__":
    unittest.main()
