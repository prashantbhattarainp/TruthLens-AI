"""Unit checks for the governed Phase 4.3 ensemble benchmark contract."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from ml.ensemble_benchmark.protocol import BASE_MODELS, DATASET_SHA256, EnsembleProtocol, protocol_dict
from ml.ensemble_benchmark.run_ensemble import _unit_score


class EnsembleBenchmarkTests(unittest.TestCase):
    def test_protocol_reuses_frozen_data_and_excludes_test(self) -> None:
        protocol = protocol_dict()
        self.assertEqual(protocol["dataset_sha256"], DATASET_SHA256)
        self.assertEqual(protocol["ensemble"]["evaluation_partition"], "validation only")
        self.assertIn("no prediction", protocol["ensemble"]["protected_test_policy"])
        self.assertIn("transformer_hybrid_status", protocol["ensemble"])
        self.assertEqual(set(BASE_MODELS), {"linear_svm", "multinomial_naive_bayes", "logistic_regression"})

    def test_only_svm_margin_is_mapped_for_meta_features(self) -> None:
        margin = np.asarray([-2.0, 0.0, 2.0])
        mapped = _unit_score("linear_svm", margin)
        self.assertTrue(np.all((mapped > 0.0) & (mapped < 1.0)))
        values = np.asarray([0.1, 0.9])
        self.assertTrue(np.array_equal(_unit_score("logistic_regression", values), values))

    def test_protocol_does_not_implicitly_add_blending_or_transformer_hybrid(self) -> None:
        protocol = EnsembleProtocol()
        self.assertIn("excluded", protocol.blending_status)
        self.assertIn("no transformer prediction artifact", protocol.transformer_hybrid_status)


if __name__ == "__main__":
    unittest.main()
