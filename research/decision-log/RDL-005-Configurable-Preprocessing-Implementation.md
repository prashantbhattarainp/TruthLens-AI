# RDL-005: Configurable Preprocessing Implementation

**Status:** Accepted for Phase 3.5  
**Date:** 2026-07-17  
**Related documents:** [Preprocessing Pipeline](../../docs/research/PREPROCESSING_PIPELINE.md), [Preprocessing Configuration](../../docs/research/PREPROCESSING_CONFIGURATION.md), [Preprocessing Report](../../docs/research/PREPROCESSING_REPORT.md)

## Context

Phase 3.4 specified a preservation-first future preprocessing policy but retained a data-readiness gate: the raw label discrepancy, formula and auxiliary-sheet provenance, text-unit eligibility, duplicate/group control, and temporal policy are unresolved. Phase 3.5 therefore needs an implementable, research-grade pipeline without silently creating a BharatFakeNewsKosh derivative.

## Decisions

1. Implement preprocessing as independently enabled components under `ml/src/preprocessing/`, with strict JSON configuration and a SHA-256 configuration identity.
2. Use spaCy for tokenisation, stop-word metadata, and optional lemmatisation. A missing configured model may use an explicit blank-language fallback only when lemmatisation is disabled; fallback status is recorded in the run metadata.
3. Adopt the conservative English configuration as the initial code default: NFC normalisation, HTML/URL/email removal, whitespace normalisation, and tokenisation enabled; lowercasing, symbol/number/punctuation changes, stop-word removal, and lemmatisation disabled.
4. Preserve negations when stop-word removal is enabled by configuration unless a future evaluated configuration explicitly changes that rule.
5. Require every data-bearing run to use an approved derivative JSONL input plus source manifest, create a new output directory outside `ml/data/raw/`, and record configuration, source-manifest hash, runtime, validation, timing, counts, failures, and output checksums.
6. Validate implementations with fixtures while the Phase 3.4 gate remains unresolved. No raw archive read, processed BFNK derivative, label mapping, split, feature, or model is authorised by this decision.

## Consequences

- The project has a tested preprocessing implementation but no preprocessed research dataset.
- Future runs are reproducible through frozen configuration snapshots, hashes, run logs, validation reports, and manifests.
- A language model is a separately versioned runtime dependency; lemmatisation cannot silently degrade to token text.
- The current mock prediction service remains independent from the research preprocessing pipeline.

## Architecture impact

None. This is a research-pipeline implementation below the existing ML boundary. It changes no public API, service interaction, deployment boundary, or mock inference contract; no ADR is created.
