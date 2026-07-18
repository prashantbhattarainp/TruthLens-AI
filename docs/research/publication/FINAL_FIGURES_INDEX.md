# Final Figures Index

All listed PNGs are tracked aggregate assets under [`../figures/`](../figures/README.md), rendered at 300 DPI, and exclude raw article text and document identifiers. They are publication-quality presentation assets, but their captions and use must retain the evidence limits below.

| No. | Figure | Description | Source / related experiment | Interpretation boundary |
| ---: | --- | --- | --- | --- |
| 1 | `shap-global-summary.png` | Mean absolute zero-reference SHAP values | Phase 4.1, 512 training-only records | Model-margin behaviour, not truth or causality |
| 2 | `shap-feature-importance.png` | Signed aggregate SHAP directions | Phase 4.1 | Aggregate vocabulary sensitivity only |
| 3 | `top-feature-rankings.png` | Signed global LinearSVC coefficient ranking | Phase 4.1 | Fitted sparse-feature weights only |
| 4 | `lime-local-example.png` | Synthetic local LIME margin-surrogate example | Phase 4.1 | Synthetic illustration; not probability |
| 5 | `shap-local-waterfall-example.png` | Synthetic additive SHAP waterfall | Phase 4.1 | Synthetic illustration; not factual evidence |
| 6 | `phase-4-5-calibration-curve.png` | Sigmoid-margin calibration-curve diagnostic | Phase 4.5, `P45-reliability-assessment-20260718T140601Z` | Non-fitted proxy; not calibration |
| 7 | `phase-4-5-reliability-diagram.png` | Margin-proxy reliability bins and histogram | Phase 4.5 | Non-fitted proxy; not confidence |
| 8 | `phase-4-5-robustness-comparison.png` | Perturbation coverage and label-flip rates | Phase 4.5 | Inherited-label stress diagnostic |
| 9 | `phase-4-5-perturbation-performance.png` | Synthetic-stress accuracy and Macro F1 | Phase 4.5 | Not an independently labelled benchmark |
| 10 | `phase-4-5-error-distribution.png` | Aggregate descriptive-theme error counts | Phase 4.5 | Overlapping keyword heuristics |
| 11 | `phase-4-5-bias-analysis.png` | Length/topic Macro-F1 diagnostics | Phase 4.5 | Descriptive slices, not demographic fairness |
| 12 | `phase-4-5-ablation-study.png` | Inference-only preprocessing/bigram diagnostics | Phase 4.5 | No components were retrained or refit |
| 13 | `phase-4-5-explanation-stability.png` | Top linear-contribution overlap under perturbations | Phase 4.5 | Feature-overlap proxy, not semantic consistency |

The [XAI manifest](../XAI_ARTIFACT_MANIFEST.json) records the Phase 4.1 generator, training-only cohort, seed, and method configuration. The [Phase 4.5 manifest](../PHASE_4_5_ARTIFACT_MANIFEST.json) records SHA-256 hashes for Figures 6-13. Cite the experiment and the corresponding limitation alongside every figure.
