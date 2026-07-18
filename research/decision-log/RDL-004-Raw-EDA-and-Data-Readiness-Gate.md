# RDL-004: Raw EDA and Data-Readiness Gate

**Status:** Superseded for DSR-001 Phase 3 experimentation by RDL-008; retained as the historical raw-EDA decision  
**Date:** 2026-07-17  
**Related documents:** [EDA Report](../../docs/research/EDA_REPORT.md), [Data Quality Assessment](../../docs/research/DATA_QUALITY_ASSESSMENT.md), [Preprocessing Recommendations](../../docs/research/PREPROCESSING_RECOMMENDATIONS.md)

## Context

Phase 3.3 manifested and structurally validated the immutable BharatFakeNewsKosh v1 archive, retaining three unresolved findings: public/raw label-count disagreement, formula-backed primary fields, and undocumented auxiliary content. Phase 3.4 was authorised to understand the release without preprocessing or creating a derivative.

## Decisions

1. Use the 26,232 declared rows in raw sheet `A` solely as the descriptive EDA population. `Sheet1` remains retained undocumented auxiliary content and `Sheet3` remains empty; neither is silently discarded or added to a dataset derivative.
2. Retain raw `True` and `False` values without mapping them to REAL/FAKE. Although no unexpected raw labels occur, the release-statistic discrepancy remains a blocking semantic-review finding.
3. Treat the EDA as an aggregate, read-only audit. No data copy, cleaned dataset, label conversion, duplicate removal, source normalisation, date conversion, split, feature, notebook, or model is created or approved.
4. Require an approved exact/near-duplicate clustering rule and a source/time grouping policy before any split. Unique IDs and zero duplicate complete rows do not remove the leakage risk from repeated bodies and text pairs.
5. Require a formula-provenance and auxiliary-sheet review before a derivative relies on cached values or expands the analytical population.
6. Treat non-ASCII source text as expected in a nine-language corpus. The isolated text-representation diagnostic indicators are retained for review; no decoding is authorised from this audit alone.
7. Keep DSR-002 and DSR-003 deferred. This raw EDA does not reopen their licence gates or alter the role-separated selection strategy.

## Consequences

- The project has a reproducible raw-data profile and publication-ready aggregate figures, but no model-ready corpus.
- The future primary English study must evidence native-English eligibility and text-unit fit; it cannot silently rely on translation fields.
- Source, date, language, category, and platform fields remain governance/audit variables until a future decision explicitly approves their use.
- Any later derivative must identify this raw parent, its checksum, the approved mappings and clustering method, exclusions, and resulting row/class counts.

## Architecture impact

None. This decision governs data readiness and research evidence only. It changes no service boundary, API, runtime, deployment, or current mock inference path; no ADR is created.

## Resolution record

RDL-008 resolves this gate only for `TL-BFNK-EN-v1.0`. It freezes documented `True`/`False` semantics, excludes formula-backed and auxiliary content from the cohort, defines exact/near-duplicate and source/time leakage controls, and fixes a grouped-stratified split strategy. The raw archive and this EDA record remain unchanged; a governed derivative and split manifest are still required before data-bearing execution.
