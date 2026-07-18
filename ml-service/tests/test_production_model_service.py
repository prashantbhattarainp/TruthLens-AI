"""Focused safeguards for runtime package loading and configuration."""

from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SERVICE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SERVICE_ROOT))

from config import get_settings
from inference.production_model_service import ModelPackageError, ProductionModelService


class ProductionModelServiceTests(unittest.TestCase):
    def tearDown(self) -> None:
        get_settings.cache_clear()

    def test_missing_package_is_explicitly_not_ready(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            service = ProductionModelService(Path(temporary_directory) / 'missing-package')
            with self.assertRaisesRegex(ModelPackageError, 'Model package is incomplete') as caught:
                service.ensure_loaded()
            self.assertEqual(caught.exception.code, 'MODEL_PACKAGE_MISSING')
            self.assertEqual(service.status, 'failed')

    def test_production_defaults_to_eager_loading_and_other_environments_to_lazy(self) -> None:
        with patch.dict(os.environ, {'ML_SERVICE_ENV': 'production'}, clear=True):
            get_settings.cache_clear()
            self.assertEqual(get_settings().model_loading_mode, 'eager')
        with patch.dict(os.environ, {'ML_SERVICE_ENV': 'testing'}, clear=True):
            get_settings.cache_clear()
            self.assertEqual(get_settings().model_loading_mode, 'lazy')


if __name__ == '__main__':
    unittest.main()
