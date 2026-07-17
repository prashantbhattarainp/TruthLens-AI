# TruthLens AI Research Methodology

**Scope:** Phase 3 - Milestone 3.1  
**Status:** Approved planning baseline; no data or model artefacts have been created  
**Last updated:** 2026-07-17

## 1. Purpose and research scope

TruthLens AI is an explainable, research-oriented fake-news detection platform for Indian digital media. The initial study will evaluate whether transparent, reproducible text-classification baselines can identify the project's defined misinformation labels in a carefully governed Indian news corpus.

The platform is a decision-support and research tool, not an automated fact-checker. A model output is a probabilistic classification signal, not a determination that a publisher, author, or claim is true or false. User-facing disclaimers, documented label provenance, and human review remain required throughout the project.

The first research iteration is expected to focus on English-language Indian digital-media text because the selected baseline tooling is mature for that setting. This is a scope constraint, not a claim that Indian digital media is English-only. Hindi and other Indian-language support will be designed as explicitly evaluated future cohorts rather than silently mixed into the initial experiment.

## 2. Research objectives

1. Establish a defensible, versioned corpus protocol for Indian digital-media misinformation research.
2. Build reproducible TF-IDF baseline experiments using Logistic Regression, Linear SVM, and Multinomial Naive Bayes.
3. Measure performance honestly under source, time, duplicate, and class-distribution controls.
4. Produce intelligible, bounded explanations that identify model-influential text features without presenting them as evidence of factual truth.
5. Preserve the exact data, configuration, environment, artefacts, and evaluation report needed to reproduce and compare every experiment.
6. Create a modular benchmark that can later compare contextual models such as DistilBERT and IndicBERT without changing the research protocol.

## 3. Research questions

| ID  | Question                                                                                                                                                    |
| --- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| RQ1 | How well do transparent TF-IDF baseline models classify the agreed misinformation labels for Indian digital-media text?                                     |
| RQ2 | Which baseline offers the best balance of macro F1, per-class recall, calibration, latency, and explanation quality?                                        |
| RQ3 | How much do results change when splits prevent source, temporal, and near-duplicate leakage?                                                                |
| RQ4 | Which preprocessing choices improve robustness without removing meaning-bearing Indian news text, names, numbers, negation, or multilingual script content? |
| RQ5 | Are feature-contribution explanations stable, useful, and appropriately cautious for end users and researchers?                                             |
| RQ6 | What performance gap remains across language, publisher/source, topic, and time cohorts, and which gaps require further data rather than model tuning?      |

## 4. Dataset selection and governance

### 4.1 Selection strategy

No dataset is selected or downloaded in this milestone. Candidate sources will be assessed with a documented dataset register before any acquisition. A candidate must provide enough information to establish provenance, permitted use, label semantics, collection period, and the relationship of the text to Indian digital media.

The primary corpus should be Indian-focused. A generic international fake-news dataset may be considered only as an explicitly labelled auxiliary or external-generalization benchmark; it must not be represented as evidence of performance on Indian digital media.

### 4.2 Indian-focused inclusion criteria

A candidate dataset is preferred when it has:

- articles, headlines, or claims originating from Indian publishers, fact-checking organisations, public-information channels, or a clearly documented Indian-media sampling process;
- source URL, publisher/domain, publication or collection time, language, topic, and label provenance where available;
- labels tied to a documented verification process, correction, fact-check, or review rule rather than an undocumented source-level assumption;
- sufficient full text or a documented text-availability policy to support the intended headline-plus-article task;
- a known language/script distribution, with English handled as the initial cohort and other Indian languages retained as separate, documented cohorts;
- a legal basis for research use, retention, and any planned redistribution; and
- enough coverage and class counts to evaluate source, topic, and temporal bias.

Candidates will be excluded or held for manual review when labels are ambiguous, provenance is absent, text is substantially missing, duplicate ownership is unclear, or use conflicts with applicable licences or platform terms.

### 4.3 Label policy

Before acquisition, the project will publish a dataset card defining the binary labels, source of truth, annotation/review process, uncertainty treatment, and exclusions. The positive class will be explicitly named in all reports; it is not assumed merely because a metric library requires a positive label. Uncertain, disputed, satire, opinion, and partially verified material must have a documented policy rather than being silently forced into `Real` or `Fake`.

### 4.4 Licensing, copyright, privacy, and attribution

Each candidate requires a licence and terms-of-use review before download or use. The review will separately record:

- dataset licence, creator attribution requirements, and whether derivatives are allowed;
- copyright and redistribution rights for article text, headlines, images, and metadata;
- publisher, platform, API, or scraping terms, if applicable;
- data-retention and access restrictions; and
- personal-data or sensitive-content considerations.

The project will not scrape or redistribute protected full text by default. Where redistribution is not permitted, the project should retain only permitted identifiers, hashes, approved excerpts, and reproducible acquisition instructions, subject to the governing terms. Every report and model card must cite the dataset, licence, and known limitations.

### 4.5 Dataset versioning strategy

Every approved data release will receive an immutable identifier such as `indian-digital-media-YYYY.MM.DD-rN`. It will have a dataset card and manifest recording source, licence snapshot, acquisition date, schema, label policy, language/source coverage, row count, exclusions, and SHA-256 checksums.

Raw, cleaned, deduplicated, and split datasets are distinct artefacts. Their IDs, parent IDs, checksums, and transformation configuration must be recorded; a model may only reference exact immutable versions. Split assignment files will be versioned alongside the manifest. A future data-versioning tool may automate this process, but the manifest and hash requirements apply regardless of tool choice.

## 5. Experimental design and data integrity

### 5.1 Train, validation, and test strategy

After data auditing, the default development design is a 70% training, 15% validation, and 15% held-out test split. The exact split will be locked only after the dataset card and deduplication policy are accepted.

Splits must be stratified by the documented label where feasible and grouped so that one source/publisher, article family, canonical URL, or near-duplicate cluster does not appear in more than one partition. If timestamps are reliable, a temporal holdout will also be evaluated to approximate future-news generalization. A separate unseen-source or later-period evaluation set is preferred when corpus size permits. Hyperparameter selection occurs only on training and validation data; the held-out test set is evaluated once for each final, frozen experiment.

The split seed, grouping algorithm, group assignments, class distribution, and inclusion/exclusion counts are experiment artefacts. Any change to a split creates a new dataset/split version rather than overwriting prior results.

### 5.2 Data-leakage prevention

The following controls are mandatory:

- deduplicate exact and near-duplicate headlines/articles before splitting; review syndicated and translated copies;
- group by canonical URL, source, claim/article family, and time when metadata supports it;
- inspect label-dependent fields and remove or isolate obvious label leakage, including fact-check verdict text, URLs, filenames, source IDs, and post-publication corrections;
- fit cleaning rules, vectorizers, feature selectors, normalisers, class-weight calculations, and resampling only on training data;
- transform validation and test data with frozen training artefacts only;
- keep the held-out test set inaccessible during iterative feature and hyperparameter decisions;
- document any manual review rule before it is applied; and
- report source, topic, language, and time composition for every partition.

Potential leakage audits are first-class experiment outputs, not informal checks.

### 5.3 Class imbalance strategy

The initial response to imbalance is measurement, not synthetic text generation. Reports will include counts, prevalence, macro and per-class metrics, confusion matrices, and error slices. Logistic Regression and Linear SVM may be compared with documented class weights. Any resampling is confined to the training partition, recorded as an experiment parameter, and compared against an unresampled baseline. Synthetic text augmentation is out of scope until its effect on validity, provenance, and leakage can be separately studied.

## 6. Text preprocessing research protocol

Preprocessing will be a reusable, configuration-driven pipeline. The planned high-level flow is:

```text
Raw text
  -> cleaning
  -> Unicode normalisation
  -> URL removal
  -> HTML removal
  -> special-character handling
  -> spaCy tokenisation
  -> lemmatisation
  -> stopword removal
  -> feature extraction
```

spaCy is the primary library for tokenisation and lemmatisation. NLTK may provide stopword lists only when a documented language-specific need exists. Each stage must be independently enabled, disabled, and versioned in experiment configuration. Raw input is retained under its permitted governance rules; processed text never replaces it as the authoritative source artefact.

The protocol will preserve and test meaning-bearing tokens such as negation, named entities, numerals, currency, dates, and Indian-language script. Unicode normalisation form and language model choices require evaluation, particularly before multilingual expansion. Initial TF-IDF features are deliberately separate from preprocessing so that BERT embeddings, sentence transformers, or FastText can be introduced behind the same feature interface later.

## 7. Baseline model strategy

The first benchmark contains three transparent text-classification baselines using a shared split and feature protocol:

1. Multinomial Naive Bayes as a fast probabilistic benchmark.
2. Logistic Regression as an interpretable linear classifier with probability outputs.
3. Linear SVM as a strong sparse-text baseline, with decision scores clearly distinguished from calibrated probabilities.

TF-IDF configurations, n-gram ranges, document-frequency limits, class weights, and model hyperparameters will be experiment parameters rather than hard-coded defaults. Model selection will use validation performance and predefined criteria; no test-set-driven tuning is allowed. Later neural or gradient-boosted approaches must use the same dataset version, split logic, metrics, and reporting template for a fair comparison.

## 8. Evaluation methodology

Macro F1 is the primary selection metric because it gives both labels equal importance under imbalance. Each experiment will additionally report accuracy, precision, recall, F1 by class, weighted F1, balanced accuracy, a confusion matrix, support counts, and training/inference time.

ROC-AUC and precision-recall AUC will be reported where a comparable continuous score exists. For Linear SVM, decision scores may support ranking metrics but must not be presented as calibrated confidence. Probability calibration and calibration error/curves will be assessed before a user-facing confidence band is trusted. Confidence thresholds, positive-label definition, and aggregation method must appear in the evaluation report.

Performance must be sliced by available language, source/publisher, topic, time, text length, and label-provenance cohort. Small or unsafe slices are reported as insufficient rather than over-interpreted. The final report includes error analysis with a documented sample-selection method.

## 9. Explainability strategy

For the initial linear baselines, explanations will expose bounded feature contributions: influential TF-IDF terms, direction of contribution, and a short model-generated explanation template. These are explanations of model behaviour, not proof that a claim is false or true. Terms that expose personal data, labels, publisher identity, or leakage signals must be filtered and investigated rather than shown as persuasive evidence.

Explanation artefacts must be tied to the exact model, vectorizer, preprocessing configuration, label map, and input version. Stability and usefulness will be evaluated through error analysis and representative cases. LIME and SHAP are planned comparative explainability methods for later milestones; their approximation limits, runtime cost, and potential instability must be reported rather than assumed away.

## 10. Model versioning, reproducibility, and experiment tracking

### 10.1 Model versioning

Each trained candidate will receive a unique model version and immutable metadata file. Model metadata must include algorithm, feature extractor version, preprocessing version/configuration hash, dataset and split versions, training date, hyperparameters, random seed, evaluation metrics, code revision, environment/dependency versions, artefact checksums, and known limitations.

The model artefact, fitted feature artefact, label mapping, metadata, and evaluation report form one release unit. A new run never overwrites a prior release; corrected or retrained models receive a new version with an explicit parent relationship.

### 10.2 Reproducibility protocol

An experiment is reproducible only when another researcher can reconstruct its inputs and procedure. Every run must preserve:

- immutable dataset, manifest, and split identifiers with checksums;
- complete preprocessing, feature, model, evaluation, and threshold configuration;
- fixed random seeds and deterministic settings where supported;
- code revision, dependency lock/environment details, operating-system and hardware notes where material;
- a machine-readable metrics report, confusion matrix, plots, logs, and artefact checksums; and
- an experiment ID that links the report, model metadata, dataset version, and later database record.

Notebooks may explore and visualize results, but production preprocessing, training, and evaluation logic must live in versioned ML-service modules. The notebooks in `research/notebooks/` remain consumers of saved artefacts and reports, never the sole source of experimental logic.

### 10.3 Experiment tracking protocol

The planned experiments register starts with the project's `experiments` record and stores model, feature extraction, hyperparameters, accuracy, precision, recall, F1, ROC, training time, dataset version, notes, and creation time. It will also link to the split ID, preprocessing version, model version, run status, metric-report location, artefact checksums, and code revision.

An experiment is comparable only when its dataset/split scope and metric definitions are explicit. Comparison pages and research reports will group results by those conditions, never rank incompatible experiments as if they were identical. Failed runs are recorded with their cause to prevent accidental selective reporting.

## 11. Risks and mitigations

| Risk                                                                      | Mitigation                                                                                                              |
| ------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| Labels are incomplete, subjective, or inconsistent.                       | Publish label policy and provenance; retain uncertainty; sample-review labels; report limitations.                      |
| Corpus is not representative of Indian digital media.                     | Make Indian-focus criteria mandatory; report source/language/topic/time coverage; avoid broad claims beyond the sample. |
| Copyright, licence, or platform terms prohibit use or redistribution.     | Perform pre-acquisition review; retain only permitted content; keep licence snapshots and attribution.                  |
| Duplicate, syndicated, translated, or source-linked text inflates scores. | Deduplicate and group before splitting; audit leakage; keep immutable split manifests.                                  |
| Class imbalance hides failure on a minority class.                        | Use macro/per-class metrics, class weights, training-only resampling, and error slices.                                 |
| Temporal drift or changing misinformation tactics reduce validity.        | Evaluate later-period and unseen-source holdouts; timestamp data; version models and monitor drift in future work.      |
| Initial English scope excludes much of the target ecosystem.              | Treat language as a reported cohort; add Hindi and other languages as separately evaluated future work.                 |
| Feature explanations cause over-trust or reveal leakage.                  | Label them as model behaviour; filter unsafe terms; test stability; investigate leakage indicators.                     |
| Unrepeatable runs undermine a paper.                                      | Lock manifests, seeds, configuration, environment, code revision, reports, and artefact hashes.                         |
| Public use implies automated fact adjudication.                           | Use a clear disclaimer, conservative wording, human-review guidance, and no publisher-level claims.                     |

## 12. Phase 3 implementation sequence

The following milestones are proposed after this planning milestone. They are intentionally gated; none is authorised by this document alone.

| Milestone | Objective                                                                                     | Gate / deliverable                                           |
| --------- | --------------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| 3.2       | Create a candidate dataset register, dataset-card template, and licence-review checklist.     | No acquisition until governance review approves a candidate. |
| 3.3       | Acquire only approved data and create immutable manifests, hashes, and source/label audits.   | Dataset version and permission record accepted.              |
| 3.4       | Implement auditable quality checks, deduplication review, and locked grouped/temporal splits. | Split manifest and leakage-audit report.                     |
| 3.5       | Implement the configurable spaCy preprocessing layer and its tests.                           | Versioned preprocessing configuration and test report.       |
| 3.6       | Implement pluggable feature extraction and TF-IDF baseline training.                          | Versioned baseline artefacts and metadata.                   |
| 3.7       | Implement evaluation, experiment registration, and saved reports.                             | Reproducible comparison report for approved baselines.       |
| 3.8       | Implement bounded baseline explanations and structured error analysis.                        | Explanation-quality review and research report.              |
| 3.9       | Prepare model comparison, research notebooks, and paper-ready figures from saved artefacts.   | Reproducible figures and draft-results package.              |

## 13. Assumptions and non-goals for this milestone

- No dataset has been selected, downloaded, processed, or distributed.
- No ML, preprocessing, training, evaluation, database, or inference implementation is created in Milestone 3.1.
- The current distributed prediction path continues to use deterministic mock data and is not research evidence.
- The first baseline study is expected to be binary and English-first, subject to the dataset-card and label-policy approval described above.
- Existing platform architecture remains unchanged; therefore no Architecture Decision Record is required for this milestone.
