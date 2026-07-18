# LIME Analysis

## Method

LIME provides a complementary local explanation by hiding terms from the already processed request text and fitting a local linear surrogate. The explainer calls a two-column signed-margin adapter: Real direction is `-margin` and Fake direction is `margin`.

This adapter is deliberately not a probability conversion. Standard LIME classifier examples commonly use probabilities, but applying a sigmoid or softmax here would falsely imply calibrated confidence. The response therefore labels the target `fake_margin`, records `local_fidelity`, sample count, and random seed, and keeps `confidence_status: unavailable`.

## Configuration and reproducibility

`XAI_TOP_FEATURE_COUNT`, `XAI_LIME_SAMPLE_COUNT`, and `XAI_LIME_RANDOM_SEED` are bounded ML-service settings. Defaults are 10 terms, 1,000 perturbations, and seed 42. They are service configuration, not user-controlled request parameters, preventing clients from changing compute cost or explanation protocol.

## Output

`lime-local-example.png` is generated from a synthetic input and demonstrates positive and negative surrogate contributions. It is illustrative only and contains no governed document text.
