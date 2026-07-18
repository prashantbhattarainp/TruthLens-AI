# Feature Importance

Feature importance is reported in two complementary forms:

- **Global LinearSVC coefficients:** the largest signed fitted weights in the frozen classifier.
- **Global mean absolute SHAP values:** average absolute zero-reference contribution magnitude across the governed training-only reference cohort.
- **Local feature contributions:** bounded SHAP and LIME terms returned for an individual prediction.

The machine-readable [feature-importance report](XAI_FEATURE_IMPORTANCE.json) records the 20 leading coefficient and mean-absolute-SHAP terms, their signed directions, model version, dataset version, training-only partition, and 512-document reference count. The figures are under [figures](figures/README.md).

"Most influential" refers only to the model margin. "Least influential" local terms are active text features with the smallest absolute SHAP values; absent vocabulary terms are not presented as evidence.
