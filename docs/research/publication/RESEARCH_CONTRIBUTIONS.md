# Research Contributions

TruthLens AI contributes a governed, reproducible investigation of an English BFNK-derived fake-news classification signal for the Indian digital-media context. Its contribution is a transparent research and engineering package, not a production fact-checking capability.

## Contributions

1. **Governed champion-challenger evaluation.** The project preserves immutable data/split lineage, an explicit protected-test restriction after tuning, and a practical-tie rule rather than promoting a model on a small validation difference.
2. **Explainability without false confidence.** The integrated SHAP/LIME path explains the exact LinearSVC margin using frozen preprocessing, bounded response metadata, train-only global analysis, and a clear distinction between model behaviour and factual truth.
3. **Honest comparison under incomplete resources.** The transformer study reports access and CPU limits as `not_evaluated` rather than manufacturing zero scores or speculative comparisons. Ensemble results expose recall, false-positive, resource, and explanation trade-offs.
4. **Language-aware boundary work for Indian media.** Unicode, Devanagari, and conservative Hinglish processing can be audited without silently treating token acceptance as multilingual fake-news detection. The work makes the data gap visible: there is no governed Hindi/Hinglish benchmark in scope.
5. **Reliability-focused model assessment.** Deterministic perturbations, non-fitted margin-proxy diagnostics, descriptive slices, error aggregates, and inference-only ablations reveal substantial surface-form sensitivity while preserving the frozen model.
6. **Practical engineering safeguards.** The frontend-to-Node-to-FastAPI boundary, integrity-checked internal package, privacy-safe aggregate artifacts, registry records, figure manifests, and publication index make the research state inspectable and repeatable.

## Contribution to Indian fake-news-detection research

The project does not claim a validated India-wide detector. Instead, it identifies why that claim would be premature: English-derived data, sparse Devanagari/Hinglish appearance, source/template sensitivity, missing publisher/time metadata, weak absolute performance, and no completed multilingual transformer artifact. This negative evidence is useful research output because it defines the requirements for a credible next study.

## Limits on novelty claims

The work does not introduce a new classifier architecture, a new public dataset, or a validated multilingual benchmark. SHAP, LIME, TF-IDF, LinearSVC, and voting ensembles are established methods. The original value is their governed integration, comparative interpretation, reliability analysis, and disciplined non-promotion decision in this project context.
