# RDL-015 - Multilingual Evaluation and Data Boundary

**Date:** 2026-07-18
**Status:** Accepted
**Phase:** 4.4

## Decision

Phase 4.4 may add a separate modular preprocessing layer for Unicode-aware English, Hindi (Devanagari), and Hinglish (Romanized Hindi) research assessment. It may use conservative script/marker routing, Hindi token extraction, bounded Hinglish spelling normalization, and language-specific cleaning. This layer must not replace or alter the immutable Phase 3 preprocessing package, integrated LinearSVC candidate, prediction-service path, API, explanation service, or confidence semantics.

The existing `TL-BFNK-EN-v1.0` derivative may be scanned for language appearance and its frozen validation partition may be evaluated descriptively with the unchanged champion. The full derivative SHA-256 and split counts must be verified. Train and protected-test rows may be counted only for split integrity; their text, labels, features, and predictions must not be retained or used by this Phase 4.4 audit. Any appearance slice remains an exploratory diagnostic unless a separately governed dataset supplies verified language labels, source/rights lineage, and a suitable split.

A manually authored language-processing fixture is permitted only when it has no REAL/FAKE label and is explicitly documented as synthetic. It may validate routing, normalization, and tokenization, but it must not train a model, generate fake-news metrics, represent translation quality, or support selection. No external Hindi/Hinglish corpus, machine translation, transliteration of derivative records, relabelling, or split mutation is authorised by this decision.

## Model and transformer consequence

The English LinearSVC remains `integrated_not_deployment_approved`, uncalibrated, and untested after tuning. It may not be retrained, calibrated, threshold-tuned, promoted, or described as Hindi/Hinglish-capable from the Phase 4.4 audit. Its decision margin remains neither probability nor confidence.

IndicBERT remains `not_evaluated_access_limited` because the Phase 4.2 attempt produced no authenticated model access, checkpoint, or prediction artifact. No replacement transformer result is implied. Every incomplete transformer remains without a performance claim.

## Consequences

Phase 4.4 records aggregate compatibility and descriptive validation evidence only. A real multilingual comparison requires a new governed data/model scope: dataset source and licence evidence, versioned derivative, language and code-mix annotation policy, split and leakage controls, pre-specified metrics, accessible model/runtime evidence, and a separate decision before any training or protected-test plan. The production architecture does not change, so ADR-009 and ADR-010 remain sufficient and no new ADR is required.
