"""Fixture-based tests for the Phase 3.5 preprocessing implementation."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


ML_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ML_ROOT / "src"))

from preprocessing.artifacts import RAW_DATA_DIRECTORY, assert_not_raw_input
from preprocessing.config import PreprocessingConfig
from preprocessing.exceptions import GovernanceError, ModelCapabilityError
from preprocessing.models import InputDocument
from preprocessing.pipeline import PreprocessingPipeline
from preprocessing.runner import PreprocessingRunner
from preprocessing.validation import validate_processing_result


CONFIG_PATH = ML_ROOT / "config" / "preprocessing" / "conservative-en-v1.json"


class PreprocessingPipelineTests(unittest.TestCase):
    def test_configured_text_operations_are_independent(self) -> None:
        config = _config(
            lowercasing={"enabled": True},
            special_character_handling={"enabled": True, "mode": "replace_with_space"},
            number_handling={"enabled": True, "mode": "remove"},
            punctuation_handling={"enabled": True, "mode": "replace_with_space"},
        )
        pipeline = PreprocessingPipeline(config)

        document = pipeline.process_document(
            InputDocument(
                document_id="fixture-1",
                text="<p>Breaking!!! Visit https://example.test Email tip@example.test 123\tNews</p>",
            )
        )

        self.assertEqual(document.processed_text, "breaking visit email news")
        self.assertEqual(document.tokens, ("breaking", "visit", "email", "news"))
        self.assertNotIn("example.test", document.processed_text)

    def test_stopword_removal_preserves_negation_when_configured(self) -> None:
        config = _config(stopword_removal={"enabled": True, "preserve_negations": True})
        pipeline = PreprocessingPipeline(config)

        document = pipeline.process_document(
            InputDocument(document_id="fixture-2", text="This is not a verified report.")
        )

        self.assertIn("not", document.tokens)
        self.assertIn("verified", document.tokens)
        self.assertNotIn("is", document.tokens)

    def test_lemmatization_requires_a_capable_spacy_model(self) -> None:
        config = _config(
            spacy={"model_name": "truthlens_missing_model_for_test", "allow_blank_fallback": True, "batch_size": 8},
            lemmatization={"enabled": True},
        )

        with self.assertRaises(ModelCapabilityError):
            PreprocessingPipeline(config)

    def test_validation_flags_documents_emptied_by_configured_removal(self) -> None:
        pipeline = PreprocessingPipeline(_config())
        result = pipeline.process_documents(
            [InputDocument(document_id="fixture-3", text="https://example.test")]
        )

        report = validate_processing_result(result, pipeline.config)

        self.assertFalse(report.is_valid)
        self.assertEqual(report.empty_processed_document_count, 1)
        self.assertEqual(report.failure_count, 0)

    def test_runner_writes_separate_processed_artifacts_and_structured_log(self) -> None:
        config = _config()
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source_manifest = root / "approved-derivative-manifest.json"
            source_manifest.write_text('{"fixture": true}\n', encoding="utf-8")
            output_directory = root / "processed" / "fixture-run"
            run, artifacts = PreprocessingRunner(config).run(
                run_id="fixture-run",
                dataset_version="fixture-derivative-v1",
                source_manifest_path=source_manifest,
                documents=[
                    InputDocument(document_id="one", text="A short verified report."),
                    InputDocument(document_id="two", text="Another report without a URL."),
                ],
                output_directory=output_directory,
            )

            self.assertTrue(run.validation.is_valid)
            self.assertEqual(run.processed_document_count, 2)
            self.assertEqual(run.error_count, 0)
            self.assertTrue(Path(artifacts["documents"]).is_file())
            self.assertTrue(Path(artifacts["manifest"]).is_file())
            run_record = json.loads(Path(artifacts["run"]).read_text(encoding="utf-8"))
            self.assertEqual(run_record["configuration_sha256"], config.sha256)
            self.assertEqual(run_record["configuration"], config.to_dict())
            log_entries = Path(artifacts["log"]).read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(log_entries), 2)
            self.assertIn("preprocessing_completed", log_entries[-1])

    def test_raw_paths_are_rejected_as_pipeline_inputs(self) -> None:
        with self.assertRaises(GovernanceError):
            assert_not_raw_input(RAW_DATA_DIRECTORY / "bharatfakenewskosh-v1.zip")


def _config(**overrides: object) -> PreprocessingConfig:
    payload = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    payload["spacy"]["model_name"] = "truthlens_missing_model_for_test"
    for key, value in overrides.items():
        payload[key] = value
    return PreprocessingConfig.from_mapping(payload)


if __name__ == "__main__":
    unittest.main()
