# XAI Limitations

- SHAP and LIME explain the classifier's learned margin, not factual truth, causality, source credibility, or user safety.
- The LinearSVC decision score is uncalibrated; neither method produces prediction confidence or probability.
- The zero-TFIDF SHAP reference is a transparent baseline, not a full correlated-language distribution.
- LIME is a local stochastic surrogate. Fixed seeds make a run reproducible, but do not prove explanation stability across inputs or alternative perturbation designs.
- TF-IDF n-grams lack semantic context and may reflect data templates, annotation artefacts, source phrasing, or generic wording.
- The current English BFNK-derived cohort, weak absolute model performance, source/template sensitivity, licence constraints, and lack of post-tuning protected-test evidence still apply.
- Figures contain aggregate vocabulary terms. They must not be used to identify people, assess individual articles, or make general claims about Indian digital media.
- Multilingual and transformer explainability require a separate governed protocol, tokenization review, fairness/robustness study, and validation evidence.
