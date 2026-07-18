# Experiment Framework

**Phase:** 3 - Milestone 3.7  
**Framework version:** `1.0.0`  
**Status:** Implemented and synthetic-fixture verified. No BharatFakeNewsKosh experiment has run.

## Purpose and boundary

The framework under `ml/src/experiments/` orchestrates reproducible cross-validated baseline-model experiments. It accepts only already-preprocessed, labelled training-partition records and a Phase 3.6 feature configuration. It does not read raw workbooks, assign source labels, create a derivative or split, train on BharatFakeNewsKosh, evaluate a held-out research test set, or alter the mock prediction service.

The implementation is verified with synthetic fixtures and was exercised in Phase 3.8 on governed derivative r2. It accepts only an approved derivative and frozen split rather than the raw archive. Its temporary fixture models, vectorizers, metrics, and candidate records are removed automatically after tests.

## Architecture

| Responsibility | Modules | Design |
| --- | --- | --- |
| Configuration | `experiments/config.py` | Strict, SHA-256-hashed model/CV/metric/seed configuration. |
| Approved models | `models/registry.py`, `models/factory.py` | Closed allowlist and configuration-driven construction of Logistic Regression, Multinomial Naive Bayes, and Linear SVM only. |
| Cross validation | `experiments/cross_validation.py` | Five-fold Stratified K-Fold by default; Stratified Group K-Fold is available when approved group IDs are supplied. |
| Feature fitting | `experiments/runner.py` plus `features/pipeline.py` | Fits a new Phase 3.6 feature extractor inside each CV training fold and transforms only its validation fold. |
| Metrics | `experiments/metrics.py` | Computes required comparable classification metrics and serializable reports. |
| Randomness | `experiments/seed.py` | Applies and records Python/NumPy seeds; model/CV seeds derive deterministically from the configured seed. |
| Tracking | `experiments/tracking.py`, `experiments/models.py` | Generates collision-resistant experiment IDs and immutable structured records/events. |
| Candidate registry | `experiments/model_registry.py` | Creates one candidate model-registry record bound to its experiment artifact bundle. |
| Artifacts and CLI | `experiments/artifacts.py`, `experiments/cli.py` | Writes checksummed evidence bundles outside raw data; CLI rejects raw paths and noncanonical output roots. |

## Cross-validation execution sequence

1. Validate the binary labelled cohort and source-manifest path.
2. Apply the configured random seed and generate a unique `EXP-YYYYMMDD-<model>-<nonce>` identifier.
3. Build five stratified folds by default, or the configured stratified-group folds when groups are provided.
4. For each fold, fit the feature extractor only on the fold's training text, transform the fold's validation text, construct the configured baseline model, fit it, and predict held-out rows.
5. Aggregate out-of-fold predictions once all rows have been held out exactly once.
6. Store fold metrics, aggregate metrics, timings, predictions, fitted fold models/vectorizers, registry record, JSONL events, and checksums in a new artifact directory.

Fitting vocabulary and inverse-document-frequency weights inside each training fold is mandatory. A pre-fitted matrix from the entire cross-validation cohort would leak validation-document frequency and vocabulary information.

## Experiment record

Every completed run records: generated experiment ID; dataset and split versions; an approved dataset/derivative SHA-256 hash; preprocessing version/configuration hash; feature-engineering version/configuration hash; model/version/hyperparameters; seed and deterministic settings; source-manifest hash; cross-validation plan; timestamps; model-fit and inference times; aggregate and per-fold metrics; notes; and artifact checksums.

The command-line adapter requires a future approved JSONL training-partition schema of `document_id`, `processed_text`, `label`, and optional `group`. It generates the experiment ID and writes to a new directory beneath `ml/data/experiments/<dataset-version>/`.

## Artifact contract

| Artifact | Purpose |
| --- | --- |
| `experiment-record.json` | Complete immutable run metadata and aggregate/per-fold metrics. |
| `config.json` | One self-contained, canonical summary of dataset/split, preprocessing, feature, model, seed, and CV settings. |
| `metrics.json` | Aggregate primary/supporting metrics and timing summary. |
| `classification_report.json` | Serializable per-class classification report. |
| `confusion_matrix.json` and `confusion_matrix.png` | Numeric matrix plus a portable review visual. |
| `notes.md` | Immutable run rationale supplied at creation. |
| `cross-validation-results.json` | Comparable metric and timing summaries. |
| `out-of-fold-predictions.jsonl` | Record ID, held-out fold, true/predicted label, and optional continuous score; no text. |
| `feature-configuration.json` | Frozen Phase 3.6 representation configuration. |
| `model-configuration.json` | Model version, hyperparameters, seed, CV plan, and configuration hash. |
| `folds/*.joblib` | Fold-specific fitted model and feature extractor pairs. |
| `model-registry-record.json` | Candidate entry with artifact location and aggregate performance evidence. |
| `experiment-registry-entry.json` | Discoverable local registry sidecar with lineage, status, primary metric, and artifact location. |
| `experiment-log.jsonl` | Start, fold-completion, and completion lifecycle events. |
| `manifest.json` | SHA-256 checksums for the artifact bundle. |

No artifact contains raw or processed text. A five-fold CV run deliberately stores `folds/fold-<n>-model.joblib` and its paired fitted extractor rather than a misleading single `model.pkl`: no one of the CV fold models is a final deployable model. Experiment artifacts and logs are git-ignored.

## Local experiment registry

The framework uses MLflow-inspired principles—immutable identifiers, explicit lineage, self-contained evidence, and reviewable artifacts—without a tracking service or mutable central database. `LocalExperimentRegistry` discovers `experiment-registry-entry.json` sidecars below `ml/data/experiments/`; the tracked [`ml/metadata/experiment-registry.json`](../../ml/metadata/experiment-registry.json) defines the empty registry and discovery contract. Synthetic fixture outputs are temporary and expressly excluded from this registry.
