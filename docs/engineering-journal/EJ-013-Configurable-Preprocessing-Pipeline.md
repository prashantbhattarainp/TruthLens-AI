# EJ-013: Configurable Preprocessing Pipeline

**Phase:** 3  
**Milestone:** 3.5 - Text Preprocessing Pipeline  
**Date:** 2026-07-17  
**Status:** Complete

## Objective

Implement a modular, configurable spaCy preprocessing pipeline with validation and run logging while preserving the immutable raw dataset and respecting the Phase 3.4 readiness gate.

## Completed work

- Added independent preprocessing components under `ml/src/preprocessing/` for Unicode, HTML, URL, email, whitespace, lowercasing, special-character, number, punctuation, tokenisation, stop-word, and lemmatisation controls.
- Added a strict conservative configuration at `ml/config/preprocessing/conservative-en-v1.json`; configurations are serialised and SHA-256-hashed for every future run.
- Added spaCy runtime management with an explicit `blank:en` fallback and a strict lemmatisation capability guard.
- Added separate processed-output writing, per-run manifests, validation reports, structured JSONL logs, failure retention, and raw-path/write safeguards.
- Added six standard-library fixture tests covering operation controls, negation preservation, lemmatisation guard, validation, artifact/log writing, and raw-data rejection.
- Added the [Preprocessing Pipeline](../research/PREPROCESSING_PIPELINE.md), [Preprocessing Configuration](../research/PREPROCESSING_CONFIGURATION.md), [Preprocessing Report](../research/PREPROCESSING_REPORT.md), and [RDL-005](../../research/decision-log/RDL-005-Configurable-Preprocessing-Implementation.md).

## Deliberately not implemented

- No BharatFakeNewsKosh raw-data read, extraction, processed derivative, label mapping, deduplication, split, feature engineering, model training, evaluation, or notebook.
- No automatic spaCy language-model download; the uninstalled configured model is recorded and the default fallback is explicit.
- No change to the FastAPI mock inference service or an ADR.

## Verification

The fixture-only test suite passed all six tests. The recorded implementation metadata is [preprocessing-pipeline-implementation.json](../../ml/metadata/preprocessing-pipeline-implementation.json). No data-bearing output exists because Phase 3.4 prerequisites are still open.
