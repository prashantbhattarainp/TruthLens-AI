# Explanation Strategy

## Local request path

1. The ML service composes `headline + "\n\n" + article` and applies the frozen Phase 3 preprocessing policy once.
2. It produces one TF-IDF row, prediction label, and LinearSVC decision margin.
3. SHAP uses that same row. LIME perturbs the already processed text and repeatedly reuses the packaged vectorizer/classifier.
4. The service returns at most the configured number of supporting and countervailing terms, plus method metadata and a disclaimer.

No request text is logged or retained after the response. The `keywords` field now contains the bounded top feature names for existing lightweight clients; detailed contribution scores are in the optional `explainability` object.

## Interpretation convention

Positive values increase the Fake-class margin; negative values increase the Real-class margin. They are directions within the classifier, not proof that a claim is fake or real. `confidence` remains `null`, `confidence_status` remains `unavailable`, and `decision_score` remains an uncalibrated margin.

## Extension boundary

Future model families implement the same local-explanation interface and return the same feature-contribution contract. A transformer-specific explainer may replace the internal algorithm, but it must retain privacy, provenance, method metadata, and the non-fact-checking warning.
