# RDL-002: Dataset Landscape and Conditional Selection

**Status:** Accepted for Phase 3.2 planning  
**Date:** 2026-07-17  
**Related documents:** [Dataset Selection Report](../../docs/research/DATASET_SELECTION_REPORT.md), [Final Dataset Selection](../../docs/research/FINAL_DATASET_SELECTION.md)

## Context

Phase 3.1 required a documented, licence-aware dataset protocol before any acquisition or ML work. Phase 3.2 assessed publicly described candidates for an English-first study of Indian digital-media misinformation. The review found no candidate that should be treated as automatically approved merely because it is public.

## Decisions

1. Use a role-separated dataset strategy rather than a merged corpus. Dataset identity, label policy, content unit, provenance, and metrics remain separate in every experiment and report.
2. Record BharatFakeNewsKosh (DSR-001) as the conditional primary training source because it has direct Indian relevance, reported binary labels/body fields, and a declared CC BY-NC 4.0 licence. The primary result must use only a future audited native-English derivative. Translation-derived English is a separate, explicitly labelled analysis or is excluded.
3. Record FactDrill (DSR-002) as the conditional Indian-context source. It may be used only after explicit licence confirmation and source-verdict mapping review; it is never pooled with the primary training data.
4. Record the COVID-19 Fake News Dataset (DSR-003) as the conditional external evaluation source. It is frozen until the primary model is final and may not influence training, feature selection, calibration, thresholding, or model choice.
5. Defer FakeNewsIndia and the Zenodo multilingual dataset. Reject IFND for synthetic-fake/source-leakage risk and FakeNewsNet for non-Indian scope plus non-distributable complete content.
6. Treat licence, copyright, privacy, source-rights, release-version, label-mapping, and data-quality confirmation as non-compensatory gates. No candidate is approved for acquisition by this decision.

## Consequences

- The project has a justified candidate strategy but no training corpus, external test file, dataset manifest, or model result.
- Phase 3.3 can start only after role-specific rights and release evidence pass review. It must not download, process, or transform a candidate that remains under review.
- Reports will distinguish in-domain primary performance, Indian-context transfer, and external domain transfer instead of producing a misleading pooled score.
- The initial study's claim remains limited to its approved native-English Indian corpus; it cannot claim multilingual or all-India generalisation.

## Alternatives considered

| Alternative | Reason not selected |
| --- | --- |
| Merge all available Indian sources for maximum sample count. | Would conflate content units, labels, translations, source distributions, and licence conditions; it also hides leakage and provenance problems. |
| Make IFND the primary corpus because it is large and Indian. | The paper reports generated fake augmentation and distinct source ecosystems for classes, making shortcut learning and label validity unacceptable for the baseline study. |
| Use FakeNewsIndia as the primary corpus. | It is false-only and cannot create the required binary target. |
| Use FakeNewsNet as an external benchmark. | The authors state that the complete corpus cannot be distributed; reproducing it would require later collection under separate publisher/platform terms. |
| Approve all public candidates now. | Public availability does not establish permission, provenance, or label fitness. |

## Architecture impact

None. This is a research-governance decision. The frontend, Node.js backend, Python mock service, contracts, and deployment architecture remain unchanged, so no ADR is created.
