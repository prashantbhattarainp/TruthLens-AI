# Ensemble Comparison - Phase 4.3

| Variant | Macro F1 delta vs LinearSVC | Main benefit | Main cost | Disposition |
| --- | ---: | --- | --- | --- |
| Hard voting | +0.0049 | 32 fewer false negatives | 49 more false positives; lower accuracy/MCC | Research challenger only |
| Weighted voting | +0.0049 | Deterministic OOF-derived weighting | Same labels as hard vote because weights are near-equal | Research challenger only |
| Soft voting | +0.0045 | Best ROC-AUC (0.5688) and PR-AUC (0.4769); 67 fewer false negatives | 106 more false positives; excludes uncalibrated LinearSVC | Research challenger only |
| Stacking | -0.1453 | Higher raw accuracy from REAL bias | 565 false negatives; Macro F1 0.3944 | Rejected as challenger |

The hard/soft gains are descriptive and small. Neither beats the incumbent across Macro F1, weighted F1, accuracy, MCC, precision/recall balance, explainability, and operational simplicity simultaneously. The metrics support a trade-off investigation, not a new champion.

Blending is excluded because it would require an additional development holdout that the frozen protocol does not provide. Transformer-based combinations are excluded because Phase 4.2 has no completed transformer predictions. See [ENSEMBLE_EVALUATION.md](ENSEMBLE_EVALUATION.md) and [HYBRID_MODEL_ANALYSIS.md](HYBRID_MODEL_ANALYSIS.md).
