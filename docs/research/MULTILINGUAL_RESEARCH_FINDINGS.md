# Multilingual Research Findings - Phase 4.4

## Findings

1. **Data, not token acceptance, is the main boundary.** The existing derivative has 9,732 English BFNK-derived records but only 59 Devanagari-bearing records and no governed Hindi/Hinglish corpus. The evaluation cannot convert sparse script occurrence into multilingual fake-news evidence.
2. **The architecture can extend safely at the research layer.** The new preprocessor performs Unicode normalization, Devanagari-aware token extraction, conservative Hinglish detection, Roman-Hindi normalization, and language-specific cleanup in a separate module. The frozen service preprocessing, LinearSVC package, API, and XAI outputs are unchanged.
3. **Classical sparse ML is especially fragile across languages.** An English TF-IDF vocabulary can accept a Unicode string and still lack meaningful lexical coverage for Hindi or Roman-Hindi variation. Token overlap and nonzero features are compatibility indicators, not semantic coverage, fairness, or model quality.
4. **Code mixing needs explicit data design.** Hinglish changes spelling, grammar, named-entity form, English terminology, and social-media conventions within a single message. A conservative marker heuristic is inspectable for routing, but it is not a substitute for annotated language-ID or code-mix labels.
5. **A multilingual transformer remains a hypothesis, not a result.** IndicBERT is relevant in principle because it is a multilingual candidate, but the existing upstream-access failure produced no checkpoint, prediction, or metric. No result has been fabricated or substituted.

## Practical implications for Indian digital media

TruthLens should continue to describe the current classifier as an English research signal only. Hindi and Hinglish inputs can be preprocessed and audited without crashing or silently stripping script, but the interface must not imply validated multilingual detection, factual verification, confidence, or risk assessment. The existing human-review and non-deployment restrictions therefore remain in force.

## Next research gate

A future multilingual phase needs an approved dataset package for each language/code-mix cohort, source/licence documentation, a versioned split with leakage controls, language and source coverage analysis, a pre-specified baseline and transformer protocol, and no reuse of the current champion’s protected test. Transformer access and suitable compute must be resolved before any multilingual transformer comparison. No architectural ADR is needed now because no production boundary changed.
