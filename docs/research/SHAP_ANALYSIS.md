# SHAP Analysis

## Method

`shap.LinearExplainer` is used with the packaged LinearSVC and an all-zero TF-IDF reference. For this linear model, each active feature contribution is additive with the classifier intercept; the reported residual checks that the contributions reconstruct the decision margin.

The zero reference is explicit and computationally tractable for the 20,000-feature sparse vocabulary. It answers: *relative to an absence of TF-IDF features, which active n-grams move this model margin?* It does not estimate causal effects or population probabilities.

## Global analysis

The global report uses 512 deterministic, class-balanced records from the frozen training partition only. Mean absolute SHAP values aggregate the magnitude of zero-reference feature contributions; coefficient rankings expose the fitted LinearSVC weights. The generated [global ranking data](XAI_FEATURE_IMPORTANCE.json) and [figures](figures/README.md) expose no raw documents.

The leading terms should be read as signals of corpus composition and model sensitivity, not semantic markers of misinformation. The prominence of generic wording and source-style phrases reinforces the known source/template-sensitivity limitation.

## Outputs

- `shap-global-summary.png`: aggregate mean absolute contributions.
- `shap-feature-importance.png`: signed aggregate contribution directions.
- `shap-local-waterfall-example.png`: additive synthetic local example.
