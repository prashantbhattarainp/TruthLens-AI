# Dataset Scoring Framework

**Scope:** Phase 3.2 preliminary, evidence-bound comparison  
**Rule:** A total score ranks candidates; it cannot override a failed mandatory gate.

## Weighted framework

Scores use a 0-5 evidence scale: 0 = absent or incompatible, 1 = weak/unverified, 2 = limited, 3 = adequate with material limitations, 4 = strong, 5 = strong and well documented. The weighted contribution is `weight x score / 5`.

| Criterion | Weight | What is evaluated |
| --- | ---: | --- |
| Indian digital-media relevance | 20 | Direct Indian source/event coverage, rather than language alone |
| Label quality and mapping readiness | 15 | Item-level label evidence, verification process, ambiguity and correction information |
| Licence compatibility | 15 | Explicit terms that permit the stated non-commercial research, retention, derivative, and publication use |
| Text task fit and full-content availability | 15 | Permitted title/claim/body text aligned to the declared task; not URLs alone |
| Dataset quality and metadata | 10 | Documented fields for source, time, language, topic, identifiers, and auditability |
| Public availability | 10 | Stable public location, transparent access conditions, and no prohibited scraping requirement |
| Reproducibility and provenance | 5 | Versioning, checksums, source release, and data-card quality |
| Sample size and class support | 5 | Plausible support for grouped, stratified evaluation after exclusions |
| Academic adoption | 5 | Peer-reviewed dataset paper, shared-task use, or clear subsequent research use |
| **Total** | **100** | **Preliminary ranking only** |

## Mandatory gate overlay

The following existing gates are non-compensatory: documented Indian relevance for the primary corpus, label provenance, legal/licence review, copyright/privacy review, task/metadata suitability, coverage/independence, and reproducibility. A candidate with a missing licence is therefore **not approved**, even if its numerical total is high.

## Scored comparison

| Candidate | Indian (20) | Label (15) | Licence (15) | Text (15) | Quality (10) | Public (10) | Provenance (5) | Size (5) | Adoption (5) | Total | Gate result |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| BharatFakeNewsKosh | 20 | 12 | 10 | 14 | 8 | 9 | 4 | 5 | 4 | **86** | Conditional: declared CC BY-NC 4.0, but source-content rights and release schema must be verified |
| FactDrill | 20 | 13 | 0 | 8 | 10 | 10 | 5 | 5 | 5 | **76** | Fails licence gate: no explicit reuse licence located |
| IFND | 20 | 5 | 0 | 15 | 6 | 7 | 3 | 5 | 4 | **65** | Fails licence gate and label/leakage suitability; rejected |
| FakeNewsIndia | 20 | 8 | 0 | 5 | 6 | 10 | 4 | 3 | 4 | **60** | Fails licence gate and binary-label requirement; deferred |
| Multilingual Zenodo dataset | 17 | 6 | 0 | 14 | 5 | 10 | 5 | 0 | 1 | **58** | Fails licence and published-provenance gates; deferred |
| COVID-19 Fake News Dataset | 2 | 13 | 0 | 11 | 7 | 6 | 4 | 4 | 5 | **52** | Fails explicit-licence gate; conditional external-test candidate only |
| FakeNewsNet | 0 | 13 | 0 | 5 | 7 | 3 | 4 | 5 | 5 | **42** | Fails Indian, rights, and reproducibility requirements; rejected |

## Interpretation

BharatFakeNewsKosh leads because it combines a balanced binary target, Indian fact-check context, body-text fields, and an explicit non-commercial licence. Its 86 is not a declaration of fitness or approval: it is a priority for the next review gate. FactDrill's high contextual score confirms its value as a separate Indian evidence source, but the missing licence makes it unavailable until resolved. The external COVID corpus is selected for a different purpose--testing domain transfer--so its low Indian-relevance score is expected rather than a defect.

The scores intentionally penalise unavailable terms, unverifiable sample counts, synthetic augmentation, and non-distributable content. They do not estimate model accuracy and must not be used as a benchmark result.
