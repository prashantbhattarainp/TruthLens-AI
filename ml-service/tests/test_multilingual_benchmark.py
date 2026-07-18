"""Unit checks for Phase 4.4 multilingual preprocessing and protocol boundaries."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
ML_SOURCE = REPOSITORY_ROOT / "ml/src"
for location in (REPOSITORY_ROOT, ML_SOURCE):
    if str(location) not in sys.path:
        sys.path.insert(0, str(location))

from ml.multilingual_benchmark.protocol import DATASET_SHA256, MultilingualProtocol, protocol_dict
from preprocessing.multilingual import MultilingualPreprocessor


class MultilingualBenchmarkTests(unittest.TestCase):
    def setUp(self) -> None:
        self.preprocessor = MultilingualPreprocessor()

    def test_hindi_detection_and_tokenization_preserve_devanagari(self) -> None:
        result = self.preprocessor.process_document(
            document_id="fixture-hi",
            text="स्वास्थ्य मंत्रालय ने वायरल दावे पर स्पष्टीकरण जारी किया।",
        )
        self.assertEqual(result.language, "hindi")
        self.assertGreaterEqual(len(result.tokens), 4)
        self.assertTrue(any("\u0900" <= character <= "\u097f" for token in result.tokens for character in token))

    def test_hinglish_normalization_is_explicit_and_conservative(self) -> None:
        result = self.preprocessor.process_document(
            document_id="fixture-hg",
            text="Kyu nahi source check karna zaroori hai?",
        )
        self.assertEqual(result.language, "hinglish")
        self.assertIn("kyun", result.tokens)
        self.assertIn("nahin", result.tokens)
        self.assertEqual(result.hinglish_normalization_count, 2)

    def test_uppercase_aap_acronym_does_not_trigger_hinglish(self) -> None:
        result = self.preprocessor.process_document(
            document_id="fixture-en",
            text="AAP released a statement after the image was shared online.",
        )
        self.assertEqual(result.language, "english")

    def test_protocol_excludes_protected_test_and_model_changes(self) -> None:
        protocol = protocol_dict()
        self.assertEqual(protocol["dataset_sha256"], DATASET_SHA256)
        self.assertEqual(protocol["multilingual_assessment"]["evaluation_partition"], "validation only")
        self.assertIn("no prediction", protocol["multilingual_assessment"]["protected_test_policy"])
        self.assertIn("no retraining", MultilingualProtocol().champion_policy)

    def test_synthetic_probe_has_no_fake_news_labels(self) -> None:
        probe_path = REPOSITORY_ROOT / "ml/fixtures/multilingual/phase-4-4-language-probe.json"
        payload = json.loads(probe_path.read_text(encoding="utf-8"))
        self.assertEqual(payload["status"], "synthetic_preprocessing_fixture_only")
        self.assertTrue(payload["records"])
        self.assertTrue(all("label" not in record for record in payload["records"]))
        for record in payload["records"]:
            result = self.preprocessor.process_document(document_id=record["record_id"], text=record["text"])
            self.assertEqual(result.language, record["expected_language"])


if __name__ == "__main__":
    unittest.main()
