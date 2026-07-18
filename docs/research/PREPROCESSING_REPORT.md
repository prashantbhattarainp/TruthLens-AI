# Preprocessing Report

**Phase:** 3 - Milestone 3.5  
**Pipeline version:** `1.0.0`  
**Report type:** Implementation and fixture-validation report; not a BharatFakeNewsKosh preprocessing result.

## Execution boundary

No BharatFakeNewsKosh row, workbook member, or raw archive was read by the Phase 3.5 pipeline tests. No processed BFNK dataset, run log, or output manifest has been generated. This preserves the Phase 3.4 data-readiness gate while providing a tested implementation ready for a later approved derivative.

## Implementation environment

| Item | Result |
| --- | --- |
| Python runtime | Project virtual environment |
| spaCy | 3.8.14 |
| Configured model | `en_core_web_sm` |
| Configured model availability | Not installed locally |
| Default runtime behaviour | Explicit `blank:en` fallback; recorded in any future run |
| Default configuration hash | `52ce7a78fa4892adf302e3c4dcc0633aebc9dfb55ca4347647f1d1cd87d3976f` |
| Default enabled operations | Unicode NFC, HTML removal, URL removal, email removal, whitespace normalisation, spaCy tokenisation |

Lemmatisation is not enabled in the default configuration and is rejected if the configured spaCy runtime lacks a lemmatiser.

## Fixture validation

The standard-library test suite completed successfully: **6 tests passed**.

| Check | Result |
| --- | --- |
| Independent text operations | Pass: HTML, URL, email, whitespace, case, special-character, number, and punctuation controls produce the configured result. |
| spaCy tokenisation and stop-word policy | Pass: tokenisation uses spaCy and configured negation preservation retains `not`. |
| Lemmatisation capability guard | Pass: a missing model with lemmatisation enabled fails explicitly rather than silently falling back. |
| Empty-output validation | Pass: a URL-only fixture becomes an invalid empty processed document under the default zero-empty threshold. |
| Artifact and manifest separation | Pass: a temporary fixture run creates processed JSONL, validation report, run record, checksummed manifest, and JSONL log outside raw data. |
| Raw-path safeguard | Pass: a path below `ml/data/raw/` is rejected before input processing. |

## Validation strategy

Every future run calculates and records:

- processed-document, empty-processed-document, and processing-failure counts;
- minimum, median, mean, and maximum token counts;
- vocabulary size from retained token forms;
- residual URLs/emails when their removal is enabled;
- repeated whitespace when normalisation is enabled;
- empty token values; and
- failure summaries by exception type.

The configured acceptance thresholds are `max_empty_document_rate` and `max_failures`. A report remains persisted even when validation is not acceptable, so failures are not hidden.

## Logging strategy

Each run records structured `preprocessing_started` and `preprocessing_completed` JSONL events. The events and run record include dataset version, pipeline version, full configuration plus hash, source-manifest hash, spaCy version/runtime, fallback status, processing duration, attempted/processed counts, errors, validation status, and vocabulary size. Logs deliberately do not copy raw text.

## Outstanding conditions

Before a data-bearing preprocessing run, the project must resolve the Phase 3.4 gates: raw-label reconciliation and mapping, formula and auxiliary-sheet provenance, approved text unit and native-English rule, duplicate/group controls, and temporal policy. The implementation does not resolve or bypass any of them.
