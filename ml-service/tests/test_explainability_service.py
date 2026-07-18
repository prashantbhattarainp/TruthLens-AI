"""Synthetic integration checks for explainability safeguards."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

SERVICE_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = SERVICE_ROOT.parent
sys.path.insert(0, str(SERVICE_ROOT))

from explainability.configuration import ExplainabilityConfiguration
from explainability.service import ExplanationService
from inference.production_model_service import ProductionModelService
from main import app


PACKAGE_DIRECTORY = (
    SERVICE_ROOT / 'artifacts' / 'candidate' / 'TL-LSVM-TFIDF-v1.1.0-rc.1'
).resolve()
SYNTHETIC_ARTICLE = (
    'This synthetic article contains sufficient neutral content to verify local explanations without '
    'reading governed evaluation documents or storing submitted text in an artifact.'
)


class ExplainabilityServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.model_service = ProductionModelService(PACKAGE_DIRECTORY)
        self.service = ExplanationService(
            self.model_service,
            ExplainabilityConfiguration(
                top_feature_count=5,
                lime_sample_count=100,
                lime_random_seed=42,
            ),
        )

    def test_frozen_preprocessing_contract_is_available_to_the_package(self) -> None:
        processed = self.model_service.preprocess_text(
            document_id='synthetic',
            text='A  Test <b>Headline</b> with URL https://example.com and Email Me@Example.com!',
        )
        self.assertEqual(processed, 'A Test Headline with URL and Email !')

    def test_shap_and_lime_explain_the_uncalibrated_margin_without_confidence(self) -> None:
        result = self.service.predict_and_explain(
            headline='Synthetic explanation test',
            article=SYNTHETIC_ARTICLE,
        )

        self.assertEqual(result.explainability.metadata.status, 'available')
        self.assertEqual(result.explainability.metadata.prediction_confidence_status, 'unavailable')
        self.assertIsNotNone(result.explainability.shap)
        self.assertIsNotNone(result.explainability.lime)
        assert result.explainability.shap is not None
        assert result.explainability.lime is not None
        self.assertAlmostEqual(result.explainability.shap.additive_residual, 0.0, places=10)
        self.assertEqual(result.explainability.lime.random_seed, 42)
        self.assertEqual(result.explainability.lime.sample_count, 100)
        self.assertLessEqual(len(result.keywords), 5)
        self.assertGreater(result.processing_time_ms, 0)

    def test_prediction_endpoint_adds_explanation_metadata(self) -> None:
        with TestClient(app) as client:
            response = client.post(
                '/predict',
                json={
                    'headline': 'Synthetic API explanation test',
                    'article': SYNTHETIC_ARTICLE,
                },
            )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload['explainability']['metadata']['status'], 'available')
        self.assertEqual(payload['explainability']['shap']['method'], 'linear_shap')
        self.assertEqual(payload['explainability']['lime']['method'], 'lime_text_margin_surrogate')


if __name__ == '__main__':
    unittest.main()
