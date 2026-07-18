# Phase 4 Summary

## Completion status

**Phase 4 is complete.** It concludes with a publication-oriented research package and no model, dataset, architecture, API, calibration, threshold, or deployment change.

## Milestones and key findings

| Milestone | Outcome |
| --- | --- |
| 4.1 Explainable AI | Integrated bounded SHAP/LIME explanations for the existing LinearSVC margin; global analysis uses training only. |
| 4.2 Transformer benchmark | Protocol complete, but no candidate completed: IndicBERT access-limited; DistilBERT CPU-limited; BERT/RoBERTa not started. |
| 4.3 Hybrid/ensembles | Best Macro F1 0.5447 from hard/weighted vote, inside the 0.005 practical-tie tolerance; no champion change. |
| 4.4 Multilingual assessment | Unicode/Hindi/Hinglish processing audit completed; evidence remains insufficient for language-wise fake-news performance. |
| 4.5 Reliability assessment | Capitalization and expansion sensitivity, uncalibrated margin, descriptive slice variation, and inference-only ablation limits documented. |
| 4.6 Research finalization | Results, comparisons, figures index, reproducibility guide, contributions, validity threats, and final documentation synchronized. |

## Final research state

`TL-LSVM-TFIDF-v1.1.0-rc.1` remains the final **internal research champion**, not a production model. It has validation Macro F1 0.5398 and MCC 0.1014; no post-tuning protected-test evidence, calibrated confidence, validated Hindi/Hinglish performance, completed transformer alternative, external-generalization claim, or deployment approval exists.

## Lessons learned

- Small validation metric gains must be interpreted alongside false-positive burden, inference/operational cost, explainability, and release gates.
- Unicode compatibility and sparse appearance slices do not create multilingual validity.
- Explainability helps inspect a classifier’s margin but cannot prove factual truth or repair data/model limitations.
- Calibration, robustness, fairness, and external validity require independently designed evidence, not retrospective proxies.
- Maintaining immutable identifiers, explicit non-results, aggregate-only artifacts, and decision logs is essential for credible applied-ML research.

## Phase 5 completion and remaining work

Phase 5 is complete through the controlled `v1.0.0-RC1` integration/release-candidate milestone. It improves the frontend, existing API integration, dashboards, validation, documentation, and deployment readiness without changing Phase 4 research evidence or approving the model for deployment. Phase 6 requires approval and governed work on data, multilingual/external evaluation, calibration, robustness/fairness, transformer compute/access, human review, and any separate public-release decision. See the [Phase 5 summary](PHASE5_SUMMARY.md) and [publication future-work plan](research/publication/FUTURE_WORK.md).
