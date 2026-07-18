"""Unit tests for the governed transformer benchmark helpers."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from ml.transformer_benchmark.metrics import classification_metrics, error_slice_summary
from ml.transformer_benchmark.protocol import DATASET_SHA256, MODELS, protocol_dict


class TransformerBenchmarkTests(unittest.TestCase):
    def test_protocol_is_bound_to_the_frozen_derivative(self) -> None:
        protocol = protocol_dict()
        self.assertEqual(protocol["dataset_sha256"], DATASET_SHA256)
        self.assertEqual(protocol["split_id"], "SPL-TL-BFNK-EN-v1.0")
        self.assertEqual(set(MODELS), {"indicbert", "distilbert", "bert_base", "roberta"})

    def test_metric_suite_and_error_slices_do_not_return_raw_text(self) -> None:
        metrics = classification_metrics([0, 1, 0, 1], [1, 1, 0, 0], [0.9, 0.8, 0.2, 0.1])
        self.assertEqual(metrics["confusion_matrix"], [[1, 1], [1, 1]])
        self.assertIn("macro_f1", metrics)
        analysis = error_slice_summary(
            [
                {"document_id": "one", "label": 0, "prediction": 1, "raw_text": "Breaking government claim"},
                {"document_id": "two", "label": 1, "prediction": 0, "raw_text": "A short vaccine note"},
            ]
        )
        self.assertEqual(analysis["error_counts"]["false_positive"]["all"], 1)
        self.assertEqual(analysis["error_counts"]["false_negative"]["health"], 1)
        self.assertNotIn("Breaking government claim", repr(analysis))
        self.assertNotIn("A short vaccine note", repr(analysis))


if __name__ == "__main__":
    unittest.main()
