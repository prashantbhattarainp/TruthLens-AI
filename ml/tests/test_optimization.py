"""Unit tests for Phase 3.9 bounded optimization configuration safeguards."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ML_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ML_ROOT / "src"))

from optimization.config import OptimizationConfig


CONFIG_DIRECTORY = ML_ROOT / "config" / "optimization"


class OptimizationConfigTests(unittest.TestCase):
    def test_approved_searches_are_bounded_and_use_the_frozen_protocol(self) -> None:
        expected = {
            "linear_svm": 32,
            "logistic_regression": 24,
            "multinomial_naive_bayes": 12,
        }
        observed = {}
        for path in CONFIG_DIRECTORY.glob("*.json"):
            configuration = OptimizationConfig.from_json_file(path)
            observed[configuration.model] = configuration.configuration_count
            self.assertEqual(configuration.search_strategy, "grid")
            self.assertEqual(configuration.scoring, "macro_f1")
            self.assertEqual(configuration.random_seed, 42)
            self.assertEqual(configuration.n_splits, 5)
        self.assertEqual(observed, expected)

    def test_unapproved_model_or_protocol_is_rejected(self) -> None:
        payload = json.loads((CONFIG_DIRECTORY / "linear-svm-tfidf-bfnk-en-v1.json").read_text(encoding="utf-8"))
        payload["model"] = "random_forest"
        with self.assertRaises(ValueError):
            OptimizationConfig.from_mapping(payload)
        payload = json.loads((CONFIG_DIRECTORY / "linear-svm-tfidf-bfnk-en-v1.json").read_text(encoding="utf-8"))
        payload["n_splits"] = 3
        with self.assertRaises(ValueError):
            OptimizationConfig.from_mapping(payload)


if __name__ == "__main__":
    unittest.main()
