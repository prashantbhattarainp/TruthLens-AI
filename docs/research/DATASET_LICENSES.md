# Dataset Licence and Rights Assessment

**Scope:** Phase 3.2 public-metadata assessment  
**Status:** DSR-001 was acquired under a recorded CC BY-NC 4.0 research scope; all other candidates remain unapproved. A public URL or an Open badge is not a licence.

## Decision rule

TruthLens AI may retain, transform, train on, evaluate with, or publish derived results from a dataset only after the dataset's own terms, underlying content rights, platform terms, attribution, privacy constraints, and retention conditions are recorded against the exact source release. The most restrictive applicable condition governs. The project must not assume that a model or research exception transfers publisher rights or permits redistribution.

| Candidate | Licence / terms evidence found | Preliminary research compatibility | Required Phase 3.3 evidence | Current decision |
| --- | --- | --- | --- | --- |
| BharatFakeNewsKosh | The public Kaggle record declares [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/). | Conditional for non-commercial research with attribution; not a licence for unrestricted product/commercial use. | Snapshot of exact Kaggle release and terms; attribution; confirmation of rights to the news bodies/translations; permitted retention, derivatives, and publication use. | Acquired under Phase 3.3 research scope; raw archive remains local and validation review is required. |
| FactDrill | The [Precog catalogue](https://precog.iiit.ac.in/datasets/) provides a public download and checksums, but no explicit reuse licence was located. | Unknown. Public access alone is insufficient. | Written or published reuse/derivative/redistribution terms; fact-check-source and social-platform terms; treatment of media URLs and investigation reasoning. | Hold. |
| COVID-19 Fake News Dataset | The [official repository](https://github.com/parthpatwa/covid19-fake-news-detection) points to competition access but shows no dataset licence. | Unknown. | Shared-task terms and permitted research-use/retention conditions; release/version identity; terms for posts and articles. | Hold. |
| FakeNewsIndia | Public catalogue download located; no explicit reuse licence located. | Unknown. | Dataset terms; terms for fact-check incident content, tweet IDs, and video references. | Hold. |
| IFND | Paper publicly describes the dataset; no author-controlled archival release and explicit reuse licence were verified. | Unknown and unsuitable on quality grounds. | Author-controlled release, source terms, redistribution rights, and augmentation provenance. | Do not pursue for this study. |
| Multilingual Zenodo dataset | The [Zenodo record](https://doi.org/10.5281/zenodo.11408513) states Open but no explicit licence was displayed. | Unknown. Zenodo hosting status is not a reuse grant. | Explicit licence, source/annotation methods, data card, and reconciliation of record/paper discrepancies. | Hold. |
| FakeNewsNet | The [authors' repository](https://github.com/KaiDMML/FakeNewsNet) explicitly says complete data cannot be distributed because of publisher copyright and Twitter privacy policy. | Incompatible with the required static, rights-safe corpus. | Not applicable unless a new, independent, permitted acquisition protocol is approved. | Reject. |

## Publication and deployment boundary

The Phase 3 study is research-oriented and can only use data under terms that allow the planned non-commercial research. A future public product, API, model redistribution, or commercial use requires a separate rights review. Model weights, feature vocabularies, example explanations, and paper excerpts must also be assessed for memorisation, personal-data exposure, and source-term constraints.

## Required licence snapshot fields

For every approved source release, preserve the URL, access date/time, licence identifier and full text or immutable copy, attribution wording, access restrictions, permitted uses, derivative/redistribution limits, content-type restrictions, related platform terms, reviewer, and approval decision. A changed web page or changed licence creates a new review event.
