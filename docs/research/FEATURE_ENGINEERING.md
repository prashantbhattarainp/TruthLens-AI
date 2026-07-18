# Feature Engineering and Representation

**Phase:** 3 - Milestone 3.6  
**Feature pipeline version:** `1.0.0`  
**Status:** Implemented and fixture-verified. No BharatFakeNewsKosh feature matrix exists; `TL-BFNK-EN-v1.0` permits a future controlled derivative run only after its split manifest is materialized.

## Purpose and boundary

The feature package converts already-preprocessed text into sparse numerical representations for an approved research cohort. It is implemented under `ml/src/features/`; it does not read the raw archive, clean text, map labels, choose a split, train a model, calculate model metrics, or change the mock prediction service. Phase 3.8 validated the r2 training representation at 20,000 TF-IDF features with no empty vectors.

A future data-bearing run must use an approved processed derivative and a frozen split. The vectorizer is fitted only on the documented training partition, then the saved fitted extractor is reused to transform validation and test partitions. This prevents vocabulary and inverse-document-frequency leakage from held-out text.

## Architecture

| Layer | Modules | Responsibility |
| --- | --- | --- |
| Configuration | `config.py` | Strict versioned configuration, semantic validation, canonical serialisation, and SHA-256 identity. |
| Common interface | `extractors/base.py` | Defines `FeatureExtractor`: `fit_transform`, `transform`, and ordered `feature_names`. |
| Baseline components | `extractors/count.py`, `extractors/tfidf.py` | Independent CountVectorizer and TF-IDF implementations. |
| Extension registry | `registry.py` | Registers method factories; new components can be added without editing the pipeline. |
| Orchestration | `pipeline.py` | Fits or applies one configured representation to `FeatureDocument` records. |
| Validation | `validation.py` | Checks vocabulary, dimensions, sparsity, empty vectors, sparse-matrix memory, and duration. |
| Tracking and artifacts | `runner.py`, `run_logging.py`, `artifacts.py` | Records experiment metadata, event logs, immutable manifests, and fitted extractor artifacts. |
| CLI adapter | `cli.py` | Reads only the approved processed-document JSONL contract and keeps command-line outputs under `ml/data/features/`. |

`FeatureDocument` contains only a record ID and `processed_text`. The feature package deliberately has no workbook reader and no raw-data access path.

## Supported baseline representations

| Method | Component | Representation | Configurable controls |
| --- | --- | --- | --- |
| Count | `CountFeatureExtractor` | Sparse word n-gram occurrence or binary-presence matrix. | `ngram_range`, `max_features`, `min_df`, `max_df`, `binary`, `normalization` |
| TF-IDF | `TfidfFeatureExtractor` | Sparse word n-gram term-frequency/inverse-document-frequency matrix. | `ngram_range`, `max_features`, `min_df`, `max_df`, `normalization`; `binary` is rejected because it is not applicable |

Both components consume the upstream whitespace-delimited token surface directly (`str.split`), disable vectorizer lowercasing, and retain punctuation or case already preserved by the approved preprocessing configuration. Feature extraction therefore does not silently perform a second text-cleaning pass.

## Extension design

The configuration accepts a validated generic method name and an extractor-specific `parameters` object. The registry binds that method to a factory at the composition root. A future Word2Vec, FastText, GloVe, Doc2Vec, BERT, or IndicBERT component can implement the same interface and register itself without modifying the pipeline, baseline components, or validation contract.

Those methods are design targets only. They are not implemented, downloaded, fitted, or evaluated in this milestone.

## Reproducible artifact contract

For a future approved run, the CLI writes a new directory at `ml/data/features/<dataset-version>/<experiment-id>/` containing:

| Artifact | Contents |
| --- | --- |
| `feature-matrix.npz` | Compressed CSR sparse matrix. |
| `feature-vocabulary.json` | Fitted feature names in exact column order. |
| `feature-record-ids.json` | Record IDs in exact matrix-row order. |
| `feature-configuration.json` | Full frozen feature configuration. |
| `feature-validation-report.json` | Matrix-quality checks and acceptance outcome. |
| `feature-experiment.json` | Dataset, split, configuration, timing, notes, and validation metadata. |
| `fitted-feature-extractor.joblib` | Reusable fitted vectorizer, including vocabulary and TF-IDF weights where applicable. |
| `feature-run-log.jsonl` | Structured start and completion events. |
| `manifest.json` | SHA-256 checksums for every generated artifact. |

Raw text is never copied into this artifact set. Feature outputs and feature logs are git-ignored, while their directory placeholders are retained.

## Future invocation

After governance approval, place `ml/src` on the Python module path (or install the package equivalently) and invoke the CLI with a frozen training-partition input:

```text
python -m features.cli --config <feature-config.json> --input-jsonl <processed-training-documents.jsonl> --source-manifest <processed-manifest.json> --experiment-id <EXP-id> --dataset-version <version> --split-id <SPL-id> --fit-partition train --notes <rationale> --output-directory ml/data/features/<version>/<EXP-id>
```

The CLI rejects `ml/data/raw/` inputs and rejects output paths outside `ml/data/features/`. This command is an execution contract, not authorisation to create features from the currently gated dataset.
