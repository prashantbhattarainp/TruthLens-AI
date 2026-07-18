# Final Experiment Summary

## Phase 4 experiment record

| Milestone | Experiment / artifact | What was completed | Result | Scope boundary |
| --- | --- | --- | --- | --- |
| 4.1 Explainable AI | `phase_4_1_xai_report` | Same-model SHAP/LIME service path and training-only global analysis | Additivity smoke residual `2.8e-17`; LIME synthetic fidelity 0.824 | Does not retrain, calibrate, or prove truth/confidence |
| 4.2 Transformers | `P42-*` | Fixed protocol and candidates | IndicBERT access-limited; DistilBERT stopped before checkpoint; BERT/RoBERTa not started | No transformer metric, checkpoint, or test access |
| 4.3 Ensembles | `P43-classical-ensemble-20260718T125724Z` | Hard, weighted, soft, and stacked classical variants | Best Macro F1 0.5447; stacker rejected | Validation only; no promotion or integration |
| 4.4 Multilingual | `P44-multilingual-assessment-20260718T133030Z` | Unicode/Hindi/Hinglish audit module and fixture | 12/12 fixture routes; no valid Hindi/Hinglish benchmark | English derivative; validation appearance slices only |
| 4.5 Reliability | `P45-reliability-assessment-20260718T140601Z` | Stress, calibration-proxy, slice, error, and inference-only ablation diagnostics | Capitalization 29.0% flips; expansion 27.0% flips | Validation only; no fitted calibration or model change |
| 4.6 Finalization | `P46-research-finalization-20260718` | Consolidation, publication tables, reproducibility guide, and consistency QA | Phase 4 package complete | Documentation and verification only; no new model/data/architecture |

## Final evidence hierarchy

1. The only integrated candidate is `TL-LSVM-TFIDF-v1.1.0-rc.1`, selected on frozen validation evidence (Macro F1 0.5398; MCC 0.1014).
2. Phase 4.3 evaluated alternatives but did not satisfy the practical, operational, explainability, or release gates for replacement.
3. Phase 4.2 and 4.4 establish research constraints, not transformer or multilingual performance.
4. Phase 4.5 narrows the interpretation further: the incumbent is surface-form sensitive and uncalibrated.

Every experiment retained the frozen derivative identity `TL-BFNK-EN-v1.0` / `DER-20260718-r2` / `SPL-TL-BFNK-EN-v1.0` (SHA-256 `978931f41ece219a3e3e27d052cfb35dfe557af02a604d6f913d4ad8e6ca59ad`). Phase 4.1 uses training only; Phase 4.3-4.5 use validation only; the protected test is not used after tuning.
