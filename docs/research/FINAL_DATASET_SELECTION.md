# Final Dataset Selection Strategy

**Scope:** Phase 3 - Milestone 3.2  
**Decision status:** Conditional research strategy; **no candidate is approved for acquisition, no files have been downloaded, and no data has been processed.**

## Decision

TruthLens AI will use a **role-separated, three-dataset strategy**. Datasets will never be concatenated by default, and metrics across roles will never be presented as one pooled result. This preserves provenance, avoids hidden domain or source imbalance, and makes generalisation claims falsifiable.

| Role | Selected source | Intended use after approval | Explicit boundary |
| --- | --- | --- | --- |
| Primary training dataset | **BharatFakeNewsKosh (DSR-001)** | Derive a versioned, English-first binary training/validation/test corpus from rows whose text, label, source, language, and rights satisfy the audit. | Main reported result is restricted to verified native-English content. Machine-translated English fields are excluded from the primary claim and may be evaluated only in a separately labelled analysis. |
| Indian context dataset | **FactDrill (DSR-002)** | Run a separate Indian-context transfer and error-analysis study after licence confirmation and an approved mapping from fact-check verdicts to the binary target. | It is not merged with BFNK and is not used to tune the primary model. Social-content/fact-check unit differences must remain visible in reporting. |
| External evaluation dataset | **COVID-19 Fake News Dataset (DSR-003)** | Conduct one frozen out-of-domain English evaluation to measure topic/source transfer after the final primary model is frozen. | It is never used for feature selection, threshold choice, calibration, or training; COVID-specific performance is not general-purpose performance. |

## Why this combination

BFNK is the strongest provisional primary source because it is Indian, balanced, fact-check-aware, and has a declared CC BY-NC 4.0 licence plus reported body-text fields. Its design directly supports the project question, subject to a strict native-English, provenance, and source-group audit.

FactDrill adds richer Indian contextual coverage--13 languages, multiple domains, and fact-check reasoning--without diluting the primary corpus. Keeping it separate exposes rather than hides task and language shift. It is particularly useful for testing whether an English-first primary model is transferable to fact-check/social content, while preventing an invalid combined training claim.

The COVID-19 shared-task corpus is deliberately external: its manual binary annotation and topic shift make it a useful stress test. A model that only performs well in the primary corpus must not be presented as generally robust until it is evaluated under this locked, out-of-domain condition.

## Non-selected alternatives

- **FakeNewsIndia:** retains value as a false-only Indian incident resource, but cannot form a binary train/test set.
- **IFND:** rejected because synthetic fake augmentation and different source ecosystems for the classes can create label/source shortcuts.
- **Multilingual Zenodo dataset:** deferred pending explicit licence, annotation/provenance evidence, and reconciliation of inconsistent public descriptions.
- **FakeNewsNet:** rejected because the authors do not distribute complete content and warn of publisher/Twitter rights restrictions; it is also outside the Indian scope.

## Risks and mitigations

| Risk | Mitigation and approval gate |
| --- | --- |
| Dataset-level licence does not cover third-party articles, translations, platform content, or derivatives. | Preserve exact terms and source-rights evidence; retain only permitted representations; reject a source if rights remain ambiguous. |
| BFNK's English translations produce translation artefacts or duplicate original/translated records. | Record original language and translation provenance; restrict primary study to verified native-English rows; keep translated analysis separate and group linked records. |
| Labels are inconsistent across fact-check sources or include partially true/disputed claims. | Preserve raw verdicts and mapping evidence; apply [Label Mapping Policy](LABEL_MAPPING.md); exclude ambiguous rows. |
| Source, fact-checker, URL, topic, time, or duplicate clusters leak into partitions. | Derive duplicate and group manifests before splitting; remove provenance fields from features; prefer source/time-separated tests where support permits. |
| FactDrill and the external dataset use different content units. | Report each evaluation role separately; do not pool scores or use transfer-test results for tuning. |
| The primary native-English subset is too small after lawful exclusions. | Stop rather than supplement it with translated or external rows; revisit a documented candidate under the same selection framework. |
| Non-commercial licensing prevents product deployment. | Keep Phase 3 claims research-only; conduct a separate deployment-data and model-rights review before any production phase. |

## Acquisition roadmap for Phase 3.3

1. **Freeze this selection report.** Record candidate IDs, public source URLs, access dates, selection rationale, and the intended role. No acquisition occurs before written governance approval.
2. **Complete rights review.** For BFNK, capture the exact Kaggle version and CC BY-NC 4.0 terms, then inspect source-content and translation rights. For FactDrill and the COVID corpus, obtain or locate explicit research-use terms before any download. Reject rather than assume permission.
3. **Approve a release-specific scope.** State allowed files, content types, retention period, access controls, attribution, and whether any derived model/report may be shared. Update the registry status only after every mandatory gate passes.
4. **Acquire once and manifest immediately.** After approval, record source files, byte sizes, SHA-256 hashes, acquisition time, access method, licence snapshot, and permitted content types. Do not transform files at this point.
5. **Audit before preparation.** Only the later quality milestone may inspect schema, missingness, labels, duplicates, source/time/language coverage, and group feasibility before any preprocessing or split creation.

This decision changes research governance only. It creates no architecture, API, runtime, storage, or deployment decision; therefore no ADR is required.
