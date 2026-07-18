# Model Limitations - Phase 4.5

- The integrated LinearSVC is an English BFNK-derived research candidate, not a fact checker, factual-verdict system, calibrated probability model, or general Indian-media reliability assessor.
- It remains untested after Phase 3.9 tuning, uncalibrated, and `integrated_not_deployment_approved`; its margin is not confidence.
- Robustness is uneven: capitalization, added context, shortened text, and stop-word changes can alter predictions materially in synthetic stress tests.
- Validation behaviour varies across source, length, temporal-appearance, and keyword-topic slices. These are descriptive correlations with uneven/overlapping cohorts, not fairness findings.
- Hindi/Devanagari and Hinglish evidence remains inadequate: 9 and 2 validation appearance records respectively are not language benchmarks.
- Publisher-level and clean temporal generalization cannot be evaluated because the derivative has no publisher field and lacks a normalized publication-date field.
- Keyword-based political, health, financial, satire, opinion, and social/media-style categories are not human topic labels; small cohorts cannot establish category performance.
- No completed transformer or hybrid artifact exists for a robustness comparison. Ensemble results remain validation-only and do not replace the champion.
- SHAP/LIME explain the model margin only. Sparse explanation-feature overlap under perturbations is a stability proxy, not a factual explanation or semantic-consistency guarantee.

These limitations require new governed data, release planning, calibration, robustness/fairness design, monitoring, human-review controls, and rights review before any deployment consideration.
