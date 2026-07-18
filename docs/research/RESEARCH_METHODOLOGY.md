# TruthLens AI Research Methodology

**Scope:** Phase 3 — Milestone 3.1
**Status:** Approved planning baseline; no data or model artefacts have been created
**Last updated:** 2026-07-17
**Related decision record:** [RDL-001](../../research/decision-log/RDL-001-Research-Methodology-and-Reproducibility.md)

## 1. Purpose and research problem statement

TruthLens AI is an explainable, research-oriented text-classification platform for Indian digital media. Its research problem is that reported fake-news classifier performance is often difficult to interpret because datasets have unclear labels or licences, duplicates cross split boundaries, source and time leakage inflate scores, and explanation outputs are incorrectly presented as fact-check evidence.

The study will determine whether transparent, reproducible text-classification baselines can discriminate the project's approved binary misinformation labels in a governed Indian digital-media corpus. The platform is a decision-support and research tool, not an automated fact-checker: a model output is a probabilistic classification signal, never a finding that a publisher, author, or claim is true or false.

## 2. Objectives

1. Establish a defensible, versioned corpus protocol for Indian digital-media misinformation research.
2. Define a reproducible baseline benchmark using TF-IDF features with Multinomial Naive Bayes, Logistic Regression, and Linear SVM.
3. Measure performance under source, temporal, duplicate, and class-distribution controls rather than relying on a random row-level split.
4. Produce bounded feature-contribution explanations that describe model behaviour without claiming factual proof.
5. Preserve the exact data, configuration, environment, artefacts, and evaluation evidence needed to reproduce and compare every experiment.
6. Create a benchmark protocol that future contextual or multilingual models can use without changing the study's governance, split, or reporting rules.

## 3. Research questions and hypotheses

| ID | Research question |
| --- | --- |
| RQ1 | How well do transparent TF-IDF baseline models classify the approved misinformation labels for Indian digital-media text? |
| RQ2 | Which baseline offers the best balance of macro F1, per-class recall, calibration, latency, and explanation quality? |
| RQ3 | How much do results change when splits prevent source, temporal, and near-duplicate leakage? |
| RQ4 | Which preprocessing choices improve robustness without removing meaning-bearing news text, names, numbers, negation, or multilingual script content? |
| RQ5 | Are feature-contribution explanations stable, useful, and appropriately cautious for researchers and users? |
| RQ6 | What performance gap remains across available language, publisher/source, topic, and time cohorts? |

The hypotheses are pre-specified design expectations, not claims about a dataset that has not yet been selected.

| ID | Hypothesis | Testable interpretation |
| --- | --- | --- |
| H1 | At least one transparent baseline will outperform a documented majority-class baseline on the frozen test set. | Compare macro F1 and its bootstrap confidence interval; report the complete comparison even if H1 is unsupported. |
| H2 | Scores from grouped and, where feasible, temporal evaluation will be less optimistic than a naive row-level random split. | Use matched configuration comparisons and report the direction and magnitude without treating a lower leakage-controlled score as failure. |
| H3 | Error and performance variation will be detectable across available source, topic, time, and language cohorts. | Report valid cohort slices with support counts; mark insufficiently sized slices instead of making a claim. |
| H4 | The most useful initial explanations will be model-feature contributions rather than standalone verdict explanations. | Review feature stability, leakage indicators, and representative errors before presenting any explanation to users. |

## 4. Scope, assumptions, and limitations

### Scope

- The primary corpus must be demonstrably relevant to Indian digital media. Generic international data may be an explicitly labelled auxiliary or external-generalisation benchmark only.
- The first study is English-first because the planned baseline tooling is mature for that setting. Hindi and other Indian languages are future cohorts that require their own coverage and evaluation evidence; they must not be silently mixed into the initial claim.
- The first target is binary only after source-label review is approved. The operational convention is FAKE = 1, the positive class, and REAL = 0, the negative class. This does not authorise mapping ambiguous source labels.
- The study concerns text supplied in the approved corpus. It does not validate images, videos, publisher reputation, or real-time claims.

### Assumptions

- Candidate datasets can supply enough provenance, label evidence, and permitted text or stable identifiers to support a documented study.
- At least one approved source will contain enough independent groups in each class for grouped evaluation.
- Where a reliable publication or verification date exists, it can be used for temporal analysis; otherwise the limitation will be recorded.
- The future implementation can preserve immutable manifests, configuration, and artefact checksums.

### Limitations

- A corpus label is evidence about that corpus's review process, not an independent truth adjudication by TruthLens AI.
- An English-first cohort cannot support performance claims for all Indian languages or all Indian digital media.
- Publisher and fact-check source coverage may be incomplete or uneven, causing selection and temporal bias.
- Text-only models can learn stylistic or provenance cues and may fail under adversarial, novel, multilingual, or evolving misinformation patterns.
- Feature contributions explain a classifier's computation; they do not provide fact-checking evidence or causal explanations.

## 5. Dataset strategy and governance

No dataset is selected, downloaded, processed, or redistributed in this milestone. Candidates must be evaluated using [DATASET_SELECTION_STRATEGY.md](DATASET_SELECTION_STRATEGY.md) and entered into [DATASET_REGISTRY.md](DATASET_REGISTRY.md) before acquisition.

A candidate is eligible only when its Indian-media relevance, source and label provenance, language coverage, text availability, licence and terms, privacy implications, and collection period are documented. Copyright and redistribution rights are considered separately from a dataset licence. If full-text retention or redistribution is not permitted, the project will retain only the allowed identifiers, hashes, excerpts, and reproducible access instructions.

Each approved release will receive an immutable identifier, a dataset card, a manifest, a licence snapshot, row counts, exclusion counts, and SHA-256 checksums. Raw, cleaned, deduplicated, and split data are distinct artefacts with parent relationships. The [data provenance protocol](DATA_PROVENANCE.md), [data dictionary](DATA_DICTIONARY.md), and [label-mapping protocol](LABEL_MAPPING.md) define the required records.

## 6. Experimental workflow

The following workflow is mandatory and sequential. A later stage cannot overwrite the evidence from an earlier stage.

1. Register and review a dataset candidate; approve it only after legal, ethical, provenance, and methodological gates pass.
2. Create an immutable raw-data manifest and record acquisition and licence evidence.
3. Audit completeness, schema conformance, labels, duplicate clusters, source, language, topic, and time coverage.
4. Freeze a deduplicated dataset version and derive a grouped split manifest before model development.
5. Run configuration-controlled baseline experiments only on development data; record every completed and failed run.
6. Select a candidate using cross-validation and validation evidence, freeze its configuration, then evaluate the held-out test set once.
7. Perform error, cohort, calibration, and explanation-stability analysis on the frozen evaluation output.
8. Register the model and experiment release with complete metadata, reports, checksums, and limitations.

## 7. Split, cross-validation, and leakage-control design

The default outer split is 70% training, 15% validation, and 15% held-out test. The exact split is not created until the dataset card, quality audit, and duplicate policy are accepted.

Splits must be stratified by the documented target label where feasible and grouped so that a canonical URL, source/publisher, claim or article family, or near-duplicate cluster does not occur in more than one partition. If reliable timestamps and sufficient data exist, the preferred held-out test cohort is later in time; an unseen-source evaluation is added where corpus coverage permits. Any departure from these controls requires a documented limitation.

Within the training partition, model and feature configurations will be assessed with five-fold stratified group cross-validation. Group definitions must remain intact within every fold. If the smallest class does not have enough independent groups for five folds, the study will use the largest feasible number of grouped folds, never fewer than three without a documented exception. The validation partition is used for candidate and threshold confirmation after training-only cross-validation; the test partition is inaccessible during iterative decisions.

Mandatory leakage controls are:

- exact and near-duplicate detection before splitting, including syndicated, translated, and substantially overlapping text;
- group assignments based on canonical URL, publisher/source, article or claim family, and time metadata where available;
- removal or isolation of label-revealing verdict text, URLs, filenames, source IDs, post-publication corrections, and equivalent provenance features;
- fitting cleaning rules, vectorizers, feature selectors, normalisers, class-weight calculations, calibration, and resampling on training data only;
- applying frozen training artefacts to validation and test inputs only; and
- recording seed, grouping rule, group assignments, class distribution, inclusion/exclusion counts, and leakage-audit results with the split.

## 8. Baseline, evaluation, and explainability design

The initial benchmark contains Multinomial Naive Bayes, Logistic Regression, and Linear SVM using a shared TF-IDF feature protocol. TF-IDF settings, n-gram ranges, document-frequency limits, class weights, and model hyperparameters must be recorded as experiment parameters rather than hidden defaults. Class imbalance is measured first; class weights may be compared, while any resampling is restricted to the training partition and recorded.

Macro F1 is the primary model-selection metric because it gives each binary class equal importance under imbalance. Every experiment also reports accuracy, class-wise precision, recall and F1, weighted F1, balanced accuracy, support counts, a confusion matrix, training time, and inference time. ROC-AUC and precision-recall AUC are reported only where a comparable continuous score exists. Linear SVM decision scores are not presented as calibrated confidence. Calibration curves and calibration error must be assessed before any user-facing confidence band is trusted.

The evaluation report must include source, topic, language, time, text-length, and label-provenance slices where support and privacy permit. Small or unsafe slices are reported as insufficient. Final uncertainty estimates use a documented, class-stratified and group-aware bootstrap procedure over held-out predictions. Where grouped evaluation is used, the resampling unit must be the independent evaluation group rather than an individual row; if the available group count makes this unreliable, the limitation must be reported.

For linear baselines, explainability is limited to influential TF-IDF features and their direction of contribution. Explanations must identify the exact model, vectorizer, preprocessing configuration, label mapping, and input version. Personal data, publisher identity, labels, and potential leakage terms are filtered from display and trigger an audit. Future LIME and SHAP comparisons are permitted only as separately evaluated methods with their instability and runtime limitations reported.

## 9. Model versioning and experiment tracking

Every run receives an experiment identifier and an immutable record in [EXPERIMENT_REGISTRY.md](EXPERIMENT_REGISTRY.md). A training candidate becomes a model release only when its artefact, fitted feature artefact, label mapping, metadata, evaluation report, and checksums are stored together according to [MODEL_REGISTRY.md](MODEL_REGISTRY.md).

Required reproducibility evidence includes exact dataset and split identifiers, manifests and checksums; preprocessing, feature, model, evaluation, and threshold configuration; seeds and deterministic settings; code revision; dependency and operating-environment details; logs; metrics; plots; and known limitations. Failed runs remain in the registry with their cause, preventing selective reporting.

Notebooks may consume recorded artefacts for analysis and figures, but they must not be the sole implementation of preprocessing, training, or evaluation logic.

## 10. Success criteria

Phase 3.1 succeeds when the methodology and its linked registry specifications make a future study auditable before any data is acquired. A research result is eligible to be described as evaluated only when all of the following are available:

1. An approved, versioned dataset with licence, provenance, label, and quality evidence.
2. A frozen grouped split manifest and leakage-audit report.
3. A complete, versioned configuration and reproducible experiment record.
4. Held-out evaluation with macro F1, class-wise metrics, support, calibration/ranking evidence where applicable, cohort slices, and uncertainty estimates.
5. A model release record with artefact checksums, dataset/split references, explanation limitations, and a clear non-fact-checking disclaimer.

No performance threshold is required for the research to be valuable. If the baselines fail to outperform the majority-class baseline or show unsafe cohort behaviour, that finding is recorded as evidence against deployment readiness, not removed or reframed as success.

## 11. Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Labels are incomplete, subjective, or inconsistent. | Require source-label policy and provenance; retain uncertainty; sample-review labels; report limitations. |
| Corpus coverage is not representative of Indian digital media. | Enforce Indian-focus criteria; report source, language, topic, and time coverage; limit claims to the observed sample. |
| Licence, copyright, privacy, or platform terms prohibit a use. | Complete pre-acquisition review; retain only permitted content; store licence snapshots and attribution. |
| Duplicate, syndicated, translated, or source-linked text inflates scores. | Deduplicate and group before splitting; retain an immutable split manifest and leakage audit. |
| Class imbalance obscures minority-class failure. | Use macro and class-wise metrics, training-only class weighting/resampling, and error slices. |
| Temporal drift reduces validity. | Prefer later-period and unseen-source evaluation where feasible; version data/models and state validity limits. |
| Explanations create over-trust or expose leakage. | Describe explanations as model behaviour; filter unsafe terms; inspect stability and leakage indicators. |
| Reproduction fails. | Preserve manifests, seeds, configuration, environment, reports, code revision, and artefact hashes. |

## 12. Explicit non-goals for this milestone

- No dataset discovery, download, acquisition, processing, or redistribution.
- No preprocessing, notebooks, feature extraction, model training, evaluation, database schema, or inference implementation.
- No replacement of the deterministic mock-prediction path.
- No claim of model accuracy, fairness, generalisation, or factual adjudication.

Progression to Phase 3.2 requires user approval. The next milestone may create governance templates and candidate-review materials, but acquisition remains prohibited until a candidate is formally approved.
