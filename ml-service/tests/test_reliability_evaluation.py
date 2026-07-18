"""Unit checks for the Phase 4.5 reliability research boundary."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from ml.reliability_evaluation.perturbations import perturbations
from ml.reliability_evaluation.protocol import DATASET_SHA256, ReliabilityProtocol, protocol_dict
from ml.reliability_evaluation.run_evaluation import _margin_proxy, calibration_diagnostic


class ReliabilityEvaluationTests(unittest.TestCase):
    def test_protocol_reuses_validation_only_and_forbids_model_change(self) -> None:
        protocol = protocol_dict()
        self.assertEqual(protocol["dataset_sha256"], DATASET_SHA256)
        self.assertEqual(protocol["reliability_assessment"]["evaluation_partition"], "validation only")
        self.assertIn("no prediction", protocol["reliability_assessment"]["protected_test_policy"])
        self.assertIn("no retraining", ReliabilityProtocol().model_policy)

    def test_margin_proxy_is_bounded_but_not_a_fitted_probability(self) -> None:
        values = _margin_proxy(np.asarray([-2.0, 0.0, 2.0]))
        self.assertTrue(np.all((values > 0.0) & (values < 1.0)))
        result = calibration_diagnostic([0, 1, 1], [-2.0, 0.0, 2.0], bins=3)
        self.assertEqual(result["status"], "diagnostic_not_fitted_calibration")
        self.assertIn("no learned", result["mapping"])

    def test_fixed_perturbation_set_covers_requested_stressors(self) -> None:
        items = {item.key: item for item in perturbations()}
        self.assertEqual(
            set(items),
            {"typos", "punctuation", "capitalization", "emoji", "url_removal", "stop_words", "synonyms", "paraphrase", "shortened", "expanded"},
        )
        self.assertTrue(items["punctuation"].transform("A claim")[1])
        self.assertIn("https://", "https://example.test")
        without_url, changed = items["url_removal"].transform("Read https://example.test now")
        self.assertTrue(changed)
        self.assertNotIn("https://", without_url)

    def test_perturbation_interpretation_does_not_claim_semantic_equivalence(self) -> None:
        items = {item.key: item for item in perturbations()}
        self.assertIn("not guaranteed", items["synonyms"].label_preservation)
        self.assertIn("original label", items["shortened"].label_preservation)


if __name__ == "__main__":
    unittest.main()
