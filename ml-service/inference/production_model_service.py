"""Integrity-checked lazy loading and inference for the governed internal model package."""

from __future__ import annotations

import hashlib
import json
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import joblib

from preprocessing import InputDocument, PreprocessingConfig, PreprocessingPipeline


class ModelPackageError(RuntimeError):
    """A package-integrity or model-readiness failure safe to expose as a stable code."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


@dataclass(frozen=True)
class ProductionPrediction:
    label: str
    decision_score: float
    latency_ms: int


@dataclass(frozen=True)
class PreparedPrediction:
    """Ephemeral inference context shared with the explainability service."""

    prediction: ProductionPrediction
    processed_text: str
    feature_vector: Any


class ProductionModelService:
    """A process-local lazy singleton; it never stores or logs submitted text."""

    REQUIRED_FILES = frozenset({
        'model-pipeline.joblib', 'vectorizer.joblib', 'classifier.joblib', 'label-mapping.json',
        'feature-configuration.json', 'preprocessing-configuration.json', 'model-metadata.json', 'manifest.json',
    })

    def __init__(self, package_directory: Path) -> None:
        self.package_directory = package_directory
        self._lock = threading.Lock()
        self._pipeline: Any | None = None
        self._preprocessor: PreprocessingPipeline | None = None
        self._metadata: dict[str, Any] | None = None
        self._load_error: ModelPackageError | None = None

    @property
    def is_loaded(self) -> bool:
        return self._pipeline is not None and self._preprocessor is not None and self._metadata is not None

    @property
    def status(self) -> str:
        if self.is_loaded:
            return 'ready'
        if self._load_error:
            return 'failed'
        return 'not_loaded'

    def metadata(self, *, load: bool = False) -> dict[str, Any]:
        if load:
            self.ensure_loaded()
        if self._metadata is not None:
            return dict(self._metadata)
        return {
            'model_version': None,
            'deployment_status': 'package_not_loaded',
            'package_directory': str(self.package_directory),
        }

    def ensure_loaded(self) -> None:
        if self.is_loaded:
            return
        with self._lock:
            if self.is_loaded:
                return
            try:
                self._load()
                self._load_error = None
            except ModelPackageError as error:
                self._load_error = error
                raise
            except Exception as error:
                package_error = ModelPackageError('MODEL_LOAD_FAILED', 'Model package could not be loaded.')
                self._load_error = package_error
                raise package_error from error

    def predict(self, *, headline: str, article: str) -> ProductionPrediction:
        return self.predict_with_context(headline=headline, article=article).prediction

    def predict_with_context(self, *, headline: str, article: str) -> PreparedPrediction:
        self.ensure_loaded()
        assert self._pipeline is not None and self._preprocessor is not None
        started = time.perf_counter()
        combined_text = f'{headline}\n\n{article}'
        processed = self._preprocessor.process_document(InputDocument(document_id='request', text=combined_text))
        if not processed.processed_text.strip():
            raise ModelPackageError('EMPTY_PROCESSED_INPUT', 'Input becomes empty under the frozen preprocessing policy.')
        vectorizer = self._pipeline.named_steps['tfidf']
        classifier = self._pipeline.named_steps['classifier']
        feature_vector = vectorizer.transform([processed.processed_text])
        predicted = int(classifier.predict(feature_vector)[0])
        score = float(classifier.decision_function(feature_vector)[0])
        labels = {'0': 'Real', '1': 'Fake'}
        if str(predicted) not in labels:
            raise ModelPackageError('INVALID_MODEL_OUTPUT', 'Model returned an unsupported label.')
        return PreparedPrediction(
            prediction=ProductionPrediction(
                label=labels[str(predicted)],
                decision_score=score,
                latency_ms=round((time.perf_counter() - started) * 1000),
            ),
            processed_text=processed.processed_text,
            feature_vector=feature_vector,
        )

    def explainability_components(self) -> tuple[Any, Any]:
        """Expose immutable package components to trusted in-process explainers only."""

        self.ensure_loaded()
        assert self._pipeline is not None
        return self._pipeline.named_steps['tfidf'], self._pipeline.named_steps['classifier']

    def preprocess_text(self, *, document_id: str, text: str) -> str:
        """Apply the frozen policy for offline, train-only global XAI aggregation."""

        self.ensure_loaded()
        assert self._preprocessor is not None
        return self._preprocessor.process_document(
            InputDocument(document_id=document_id, text=text)
        ).processed_text

    def _load(self) -> None:
        missing = sorted(name for name in self.REQUIRED_FILES if not (self.package_directory / name).is_file())
        if missing:
            raise ModelPackageError('MODEL_PACKAGE_MISSING', f'Model package is incomplete: {", ".join(missing)}.')
        manifest = _read_json(self.package_directory / 'manifest.json')
        file_hashes = manifest.get('files')
        if not isinstance(file_hashes, dict):
            raise ModelPackageError('MODEL_MANIFEST_INVALID', 'Model package manifest has no file hashes.')
        for filename, expected_hash in file_hashes.items():
            path = self.package_directory / filename
            if not path.is_file() or _sha256(path) != expected_hash:
                raise ModelPackageError('MODEL_INTEGRITY_CHECK_FAILED', f'Model package integrity check failed for {filename}.')
        metadata = _read_json(self.package_directory / 'model-metadata.json')
        required_metadata = {'model_version', 'dataset_version', 'feature_engineering_version', 'preprocessing_version', 'deployment_status'}
        if not required_metadata <= set(metadata):
            raise ModelPackageError('MODEL_METADATA_INVALID', 'Model metadata is incomplete.')
        pipeline = joblib.load(self.package_directory / 'model-pipeline.joblib')
        if set(getattr(pipeline, 'named_steps', {})) != {'tfidf', 'classifier'}:
            raise ModelPackageError('MODEL_PIPELINE_INVALID', 'Model pipeline has unexpected steps.')
        preprocessor = PreprocessingPipeline(PreprocessingConfig.from_json_file(self.package_directory / 'preprocessing-configuration.json'))
        self._pipeline = pipeline
        self._preprocessor = preprocessor
        self._metadata = metadata


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError) as error:
        raise ModelPackageError('MODEL_METADATA_INVALID', 'Model package metadata is unreadable.') from error
    if not isinstance(value, dict):
        raise ModelPackageError('MODEL_METADATA_INVALID', 'Model package metadata must be an object.')
    return value


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()
