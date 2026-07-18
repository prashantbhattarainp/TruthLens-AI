# Preprocessing Pipeline

**Phase:** 3 - Milestone 3.5  
**Pipeline version:** `1.0.0`  
**Status:** Implemented and fixture-verified. `TL-BFNK-EN-v1.0` now permits a future controlled derivative run; direct raw-archive input remains blocked.

## Purpose and boundary

The pipeline provides modular, reproducible text preparation for approved data derivatives. It is implemented in `ml/src/preprocessing/`; it does not read the raw XLSX archive, alter `ml/data/raw/`, map labels, remove records, create features, train a model, or change the mock prediction API. Phase 3.8 exercised it on governed r2 with no failures or empty processed documents.

Direct raw paths are rejected by the CLI. A real run requires an already-approved JSONL derivative and its source manifest. Outputs are written only to a new directory below `ml/data/processed/`, while the immutable raw archive remains the authoritative parent.

## Architecture

| Layer | Modules | Responsibility |
| --- | --- | --- |
| Configuration | `config.py` | Strict JSON schema, validation, canonical serialisation, and SHA-256 configuration identity. |
| Text components | `components.py` | Independent Unicode, HTML, URL, email, whitespace, case, special-character, number, and punctuation transforms. |
| spaCy runtime | `spacy_runtime.py` | Loads the configured spaCy model or records an explicit blank-language fallback. |
| Orchestration | `pipeline.py` | Applies enabled text transforms in a fixed order, then spaCy tokenisation and optional token-level operations. |
| Validation | `validation.py` | Detects empty processed documents, token/vocabulary statistics, processing failures, and unexpected residual output. |
| Artifacts and logging | `artifacts.py`, `run_logging.py`, `runner.py` | Writes separate processed artifacts, manifests, reports, and structured JSONL events without overwriting a run. |
| CLI adapter | `cli.py` | Reads only approved derivative JSONL input and binds it to a configuration, source manifest, and output directory. |

## Processing sequence

The ordering is fixed and every operation can be disabled through configuration:

1. Unicode normalisation.
2. HTML removal.
3. URL removal.
4. Email removal.
5. Optional special-character, number, and punctuation handling.
6. Whitespace normalisation and optional lowercasing.
7. spaCy tokenisation.
8. Optional stop-word filtering, with configurable preservation of negations.
9. Optional lemmatisation.

Each operation is a small component with one responsibility. Text transforms never access labels, sources, dates, or other metadata. Token-level steps use spaCy `Doc` and `Token` objects.

## spaCy model policy

The configured model is `en_core_web_sm`. It was not installed in the local implementation environment, so the conservative configuration uses an explicit `spacy.blank("en")` fallback for tokenisation and stop-word metadata. The run record exposes `runtime_model` and `model_fallback_used`; a fallback is never silent.

Lemmatisation is disabled by default. If it is enabled, the pipeline requires a loaded spaCy model with a lemmatiser and fails before processing if that capability is unavailable. This prevents an unreviewed fallback from silently changing lexical meaning.

## Processed-output contract

For a future approved run, the output directory is `ml/data/processed/<dataset-version>/<run-id>/` and contains:

| Artifact | Contents |
| --- | --- |
| `processed-documents.jsonl` | Record ID, source-text SHA-256, processed text, and tokens; no raw input text. |
| `processing-failures.json` | Retained document-level error type/message records. |
| `preprocessing-run.json` | Dataset version, pipeline/configuration identity and snapshot, spaCy runtime, timing, counts, and validation outcome. |
| `preprocessing-report.json` | Empty-document, token, vocabulary, failure, and unexpected-output checks. |
| `run-log.jsonl` | `preprocessing_started` and `preprocessing_completed` structured events. |
| `manifest.json` | SHA-256 checksums for the generated run files and the source-manifest identity. |

Processed outputs and operational logs are git-ignored. The pipeline refuses to overwrite an existing run directory and refuses writes beneath `ml/data/raw/`.

## Future invocation

After governance approval, the CLI may be invoked with an approved derivative, its manifest, a frozen configuration, a stable dataset version, and a new run ID. The package is source-rooted at `ml/src`, so the execution environment must place that directory on its module path (or install the package equivalently):

```text
python -m preprocessing.cli --config <config.json> --input-jsonl <approved-derivative.jsonl> --source-manifest <manifest.json> --dataset-version <version> --run-id <new-run-id> --output-directory <new-processed-output-directory>
```

This is an execution contract only. It does not authorise direct use of the BharatFakeNewsKosh raw archive; a future run must first materialize the frozen `TL-BFNK-EN-v1.0` derivative and split manifest.
