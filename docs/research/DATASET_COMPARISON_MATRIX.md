# Dataset Comparison Matrix

**Scope:** Phase 3 - Milestone 3.2 landscape analysis  
**Evidence cut-off:** 2026-07-17  
**Boundary:** Public descriptions, source papers, and repository metadata only. No file was downloaded, opened, processed, or used for modelling.

## Reading this matrix

The matrix is a candidate screen, not an acquisition approval. "Public" means that a public landing page or download route was observed; it does not establish that the underlying news text, platform data, or derivatives may be retained or redistributed. "Full text" distinguishes a news/claim body from a headline, URL, or social-engagement pointer. Every candidate remains subject to the mandatory gates in [Dataset Selection Strategy](DATASET_SELECTION_STRATEGY.md).

| ID | Candidate and original source | Official public location | Reported sample count and languages | Label schema | Headline / full text | Licence evidence | Indian relevance and research adoption | Preliminary outcome |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DSR-001 | **BharatFakeNewsKosh (BFNK)** - Singh et al., Springer SmartCom 2023 | [Maintainer's Kaggle dataset record](https://www.kaggle.com/datasets/man2191989/bharatfakenewskosh); [publication DOI](https://doi.org/10.1007/978-981-99-0838-7_24) | 26,232: 13,721 true and 12,511 false; 9 Indian languages; 60 categories | TRUE / FALSE, reportedly assigned with fact-check context and human annotation | `Statement`, `News_Body`, title and English-translation fields are reported; actual release schema and source-text rights require audit | CC BY-NC 4.0 is declared on the dataset record; it supports non-commercial research only and does not settle third-party news rights | Direct Indian fact-check corpus, 2013-2022, 19 fact-check sources. Emerging rather than a long-established benchmark | **Provisionally selected as primary training source**, restricted to a verified English-language derivative; no acquisition approval |
| DSR-002 | **FactDrill** - Singhal, Shah and Kumaraguru, ICWSM 2022 | [IIIT-Hyderabad/Precog dataset catalogue](https://precog.iiit.ac.in/datasets/); [dataset paper](https://ojs.aaai.org/index.php/ICWSM/article/view/19384) | 22,435 fact-checked social-media content items; 2013-2020; 13 Indian languages (9,058 English, 5,155 Hindi, remainder regional) | Fact-check-source verdict information; exact binary mapping must be reviewed | Textual/social content and fact-check reasoning attributes; **not** a guaranteed full publisher-article corpus | No explicit reuse licence located on the catalogue or paper | Excellent Indian and multilingual context; peer-reviewed ICWSM dataset paper | **Provisionally selected as Indian-context source**; blocked from acquisition/use pending licence and label-mapping review |
| DSR-003 | **COVID-19 Fake News Dataset** - Patwa et al., CONSTRAINT/AAAI 2021 | [Authors' official repository](https://github.com/parthpatwa/covid19-fake-news-detection); repository directs access through the [shared-task competition](https://competitions.codalab.org/competitions/26655) | 10,700 manually annotated English social-media posts and articles | REAL / FAKE | Mixed posts and articles; no guarantee that every row is a full news article or has a headline | No explicit dataset licence identified; shared-task access conditions must be retained and reviewed | Non-Indian, COVID-only, but a recognised shared-task resource with documented baselines | **Provisionally selected as external evaluation source**; held out from all training and blocked pending rights confirmation |
| DSR-004 | **FakeNewsIndia** - Dhawan et al., *Computer Communications* 2022 | [Precog dataset catalogue](https://precog.iiit.ac.in/datasets/); [publication DOI](https://doi.org/10.1016/j.comcom.2022.01.003) | 4,803 English false-news incidents, June 2016-December 2019; with 5,031 linked tweets and 866 linked YouTube videos | False incidents and impact labels; no matched TRUE class | Fact-check incident metadata and linked platform references; not a balanced full-article corpus | No explicit reuse licence located | Strong Indian relevance and an established publication, but a false-only corpus cannot support the binary study | **Deferred**; may support false-class contextual/error analysis only after rights review |
| DSR-005 | **IFND (Indian Fake News Dataset)** - Sharma and Garg, *Complex & Intelligent Systems* | [Original dataset paper](https://link.springer.com/article/10.1007/s40747-021-00552-1); no author-controlled archival download was independently verified | 56,868 reported records: 37,809 real and 19,059 fake; Indian events, 2013-2021 | REAL / FAKE; fake class includes generated augmentation after a reported 7,271 collected fake items | Headline/text and image links are reported | No explicit source-data or redistribution licence verified | Indian and widely discussed, but class construction and source separation risk leakage | **Rejected for this study**: synthetic fake augmentation and source-derived class cues conflict with the planned leakage and label protocol |
| DSR-006 | **Multilingual Fake News Detection Dataset: Gujarati, Hindi, Marathi, and Telugu** - Patil et al., Zenodo 2024 | [Zenodo DOI record](https://doi.org/10.5281/zenodo.11408513) | Sample count is not declared on the Zenodo record; four language archives, 194.2 MB total | FAKE / REAL claimed by the record | News articles are claimed; actual fields must be inspected only after approval | Zenodo marks the record Open but does not show an explicit reuse licence on the record | Indian-language relevance is high; peer-reviewed provenance and adoption are unclear | **Deferred**: missing licence and insufficient published label/provenance detail; later literature also reports inconsistent language/size claims against the record |
| DSR-007 | **FakeNewsNet** - Shu et al., ASU | [Authors' repository](https://github.com/KaiDMML/FakeNewsNet) | 23,196 commonly used PolitiFact/GossipCop reference entries; English, United States | FAKE / REAL from PolitiFact and GossipCop | Redistributable release contains IDs, URLs, titles and tweet IDs; authors state the complete article/social corpus cannot be distributed | Repository states copyright and platform-privacy restrictions; no compatible dataset licence established | Very high academic adoption but no Indian relevance and reproducibility depends on future crawling/API access | **Rejected** as a project dataset; it cannot satisfy the current public, rights-safe, reproducible corpus requirement |

## Candidate observations

### DSR-001 - BharatFakeNewsKosh

**Strengths:** It is the only screened candidate with a declared research-compatible licence, a balanced binary count, direct Indian focus, substantial scale, fact-check context, language metadata, and reported body-text fields. Later published use also identifies `title`, `News_Body`, `Eng_Trans_News_Body`, language, and fact-check links as fields.

**Weaknesses:** The source publication describes 16 attributes while the current Kaggle record describes 19. Non-English material was translated to English for annotation, so a model could learn translation artefacts. CC BY-NC 4.0 is incompatible with an unrestricted commercial deployment, and the dataset licence does not itself prove rights to every source article. These facts require a release-specific schema, provenance, and rights audit.

### DSR-002 - FactDrill

**Strengths:** FactDrill is a well-documented, multi-domain, multilingual Indian fact-check resource with 14 attributes and investigation reasoning. It is especially valuable for contextual, source, language, and error analysis.

**Weaknesses:** It is social-media/fact-check content rather than a conventional full-news-article corpus. The public catalogue gives checksums but no explicit reuse licence, and the raw verdict taxonomy must be reviewed before binary mapping. It must not be silently mixed with the primary training data.

### DSR-003 - COVID-19 Fake News Dataset

**Strengths:** A documented, manually annotated English dataset with 10,700 real/fake posts and articles, released through a shared task and accompanied by baseline evidence. Its topic and source shift make it a useful external-generalisation challenge.

**Weaknesses:** It is COVID-specific, not Indian-media specific, and has no explicit licence found in the author repository. Its content unit mixes posts and articles. It can only be a frozen, separately reported external test, never a source of training examples.

### Deferred or rejected candidates

FakeNewsIndia is valuable evidence of Indian misinformation incidents, but its false-only design makes binary training/evaluation invalid. IFND offers scale and article text but reports synthetic fake augmentation and real/fake collection from different source ecosystems, producing unacceptable label and source-leakage risk for the first study. The Zenodo multilingual record is promising for a later Indic-language study but lacks an explicit licence and reproducible, consistent data-card evidence: its four-language record differs from a later [five-language, 74,000-article description](https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2025.1690616/full) associated with the same DOI. FakeNewsNet is academically prominent but its own authors say complete content cannot be redistributed because of publisher copyright and Twitter policy.

## Sources consulted

- [BharatFakeNewsKosh dataset record](https://www.kaggle.com/datasets/man2191989/bharatfakenewskosh) and [original publication](https://doi.org/10.1007/978-981-99-0838-7_24)
- [FactDrill dataset paper](https://ojs.aaai.org/index.php/ICWSM/article/view/19384) and [Precog catalogue](https://precog.iiit.ac.in/datasets/)
- [COVID-19 Fake News Dataset paper](https://arxiv.org/abs/2011.03327) and [authors' repository](https://github.com/parthpatwa/covid19-fake-news-detection)
- [IFND paper](https://link.springer.com/article/10.1007/s40747-021-00552-1), [Multilingual Zenodo record](https://doi.org/10.5281/zenodo.11408513), and [FakeNewsNet repository](https://github.com/KaiDMML/FakeNewsNet)

The linked sources support candidate discovery and preliminary assessment only. Licence text, access conditions, source terms, data schema, and row-level provenance remain Phase 3.3 review artefacts.
