# Research Documentation

This directory is the canonical home for the Phase 3/4 research package. It defines governance, dataset selection, acquisition evidence, EDA, the frozen `TL-BFNK-EN-v1.0` experiment contract, and bounded XAI, transformer, ensemble, and multilingual evidence. Governed data/model artifacts remain outside this documentation directory and are intentionally not tracked in Git.

| Document | Purpose | Current status |
| --- | --- | --- |
| [Research methodology](RESEARCH_METHODOLOGY.md) | Defines the research question, design, hypotheses, evaluation, and success criteria. | Approved planning baseline |
| [Dataset selection strategy](DATASET_SELECTION_STRATEGY.md) | Defines how candidates will be reviewed before acquisition. | Approved planning baseline |
| [Dataset registry](DATASET_REGISTRY.md) | Register of screened candidates and later approved datasets. | DSR-001 r2 derivative materialized as `TL-BFNK-EN-v1.0`; other roles deferred |
| [Dataset landscape report](DATASET_SELECTION_REPORT.md) | Records the Phase 3.2 evidence review and conditional selection strategy. | Complete; no acquisition authorised |
| [Dataset comparison matrix](DATASET_COMPARISON_MATRIX.md) | Compares source, scope, labels, text, licensing, strengths, and limitations. | Complete |
| [Dataset scoring](DATASET_SCORING.md) | Defines the weighted framework and non-compensatory gate overlay. | Complete |
| [Dataset licences](DATASET_LICENSES.md) | Records licence and content-rights evidence for every screened candidate. | Complete; approval evidence pending |
| [Final dataset selection](FINAL_DATASET_SELECTION.md) | Defines the conditional primary, Indian-context, and external-evaluation roles. | Complete; all roles remain conditional |
| [Dataset acquisition report](DATASET_ACQUISITION_REPORT.md) | Records the immutable raw acquisition and deferred candidates. | Complete |
| [Data validation report](DATA_VALIDATION_REPORT.md) | Records read-only schema, missingness, encoding, and review findings. | Complete; findings carried into Phase 3.4 readiness gate |
| [Data integrity report](DATA_INTEGRITY_REPORT.md) | Records container health, checksums, and raw-artifact identity. | Complete |
| [EDA report](EDA_REPORT.md) | Read-only exploratory analysis, observations, and research interpretation. | Complete; historical raw assessment |
| [Data profile](DATA_PROFILE.md) | Documents raw schema, text, source, language, time, and formula characteristics. | Complete |
| [Dataset statistics](DATASET_STATISTICS.md) | Reconciled aggregate counts and descriptive statistics. | Complete |
| [Data quality assessment](DATA_QUALITY_ASSESSMENT.md) | Evaluates readiness risks and required mitigations. | Complete; conditional use only |
| [Dataset governance](DATASET_GOVERNANCE.md) | Freezes label semantics, formula/auxiliary treatment, duplicate handling, and leakage controls. | Complete for `TL-BFNK-EN-v1.0` |
| [Dataset manifest](DATASET_MANIFEST.md) | Identifies the frozen source, cohort, hashes, statistics, policies, and split contract. | Complete; governance manifest only |
| [Dataset versioning](DATASET_VERSIONING.md) | Defines immutable fields and the change-control process. | Effective for Phase 3 |
| [Experiment readiness](EXPERIMENT_READINESS.md) | Defines controlled derivative materialization and experiment preconditions. | Satisfied by corrected r2 Phase 3.8 run |
| [Preprocessing recommendations](PREPROCESSING_RECOMMENDATIONS.md) | Documents future, gated recommendations without implementing a data derivative. | Complete; superseded for the frozen cohort by RDL-008 controls |
| [Preprocessing pipeline](PREPROCESSING_PIPELINE.md) | Documents the modular spaCy pipeline, artifact boundary, and raw-data safeguards. | Implemented and exercised on r2 with zero failures |
| [Preprocessing configuration](PREPROCESSING_CONFIGURATION.md) | Defines the strict, versioned preprocessing configuration strategy. | Conservative English default recorded |
| [Preprocessing report](PREPROCESSING_REPORT.md) | Records fixture validation, runtime policy, validation, and logging evidence. | Complete; r2 result is in governed artifacts |
| [Feature engineering](FEATURE_ENGINEERING.md) | Documents modular sparse feature extraction, extension points, artifact contract, and safeguards. | Implemented and fixture-verified; controlled split-dependent run pending |
| [Feature configuration](FEATURE_CONFIGURATION.md) | Defines versioned Count and TF-IDF configuration controls and change policy. | Complete; two baseline configurations recorded |
| [Feature comparison plan](FEATURE_COMPARISON_PLAN.md) | Defines the future fair-comparison protocol without reporting results. | Complete; design only |
| [Feature validation report](FEATURE_VALIDATION_REPORT.md) | Records fixture validation and the future matrix-quality checks. | Complete; r2 feature artifact validated |
| [Experiment framework](EXPERIMENT_FRAMEWORK.md) | Documents baseline CV architecture, fold-level feature fitting, tracking, and artifact contract. | Implemented and exercised on governed r2 data |
| [Baseline model report](BASELINE_MODEL_REPORT.md) | Records the three allowed baseline implementations and their verification boundary. | Superseded for result reporting by Phase 3.8 evaluation |
| [Model comparison plan](MODEL_COMPARISON_PLAN.md) | Defines fair future comparison conditions and selection evidence. | Complete; design only |
| [Reproducibility guide](REPRODUCIBILITY_GUIDE.md) | Defines input lineage, configuration, seed, environment, and artifact replay requirements. | Applied to r2 execution |
| [EDA figures](figures/README.md) | Accessible vector figures generated from aggregate raw-data analysis. | Complete |
| [Data provenance](DATA_PROVENANCE.md) | Defines the source-to-derivative audit trail. | Approved planning baseline |
| [Data dictionary](DATA_DICTIONARY.md) | Defines the planned unified, implementation-neutral record schema. | Draft schema specification |
| [Label mapping](LABEL_MAPPING.md) | Defines the binary-label convention and BFNK v1 source-label mapping. | `LMAP-BFNK-v1.0` frozen |
| [Model evaluation report](MODEL_EVALUATION_REPORT.md) | Reports protocol, baseline results, selected test result, and limitations. | Complete; research candidate only |
| [Model comparison](MODEL_COMPARISON.md) | Compares comparable baseline outcomes and resource evidence. | Complete |
| [Statistical analysis](STATISTICAL_ANALYSIS.md) | Records uncertainty intervals and paired comparison evidence. | Complete; descriptive limits stated |
| [Error analysis](ERROR_ANALYSIS.md) | Documents aggregate protected-test error asymmetry and slices. | Complete |
| [Feature importance analysis](FEATURE_IMPORTANCE_ANALYSIS.md) | Documents aggregate linear-coefficient diagnostics and use limits. | Complete |
| [Experiment registry](EXPERIMENT_REGISTRY.md) | Reserves the comparable-experiment register and required fields. | Three r2 baseline entries recorded |
| [Model registry](MODEL_REGISTRY.md) | Defines model-release metadata and lifecycle requirements. | Phase 3.9 conditional champion and challengers recorded; no deployment approval |
| [Model Card](MODEL_CARD.md) | Documents intended research use, performance context, explainability, and responsible-AI limits. | Added in Phase 4.1; deployment remains prohibited |
| [Data Card](DATA_CARD.md) | Records the frozen derivative and Phase 4.2 data-handling boundary. | Added; no dataset version change |
| [Transformer benchmark](TRANSFORMER_BENCHMARK.md) | Defines the frozen-input transformer protocol and evidence state. | Evidence collection in progress; no automatic promotion |
| [Classical vs transformers](CLASSICAL_VS_TRANSFORMERS.md) | Separates incumbent validation evidence from transformer run outcomes. | In progress; incomplete candidates have no score |
| [Resource comparison](RESOURCE_COMPARISON.md) | Records host constraints and measured per-candidate resource evidence. | CPU-only execution; timings pending completed runs |
| [Model selection update](MODEL_SELECTION_UPDATE.md) | Documents the Phase 4.2 champion-challenger non-promotion boundary. | Current LinearSVC unchanged |
| [Ensemble evaluation](ENSEMBLE_EVALUATION.md) | Reports Phase 4.3 validation-only classical ensemble evidence and error aggregates. | Complete; no protected-test access or promotion |
| [Hybrid model analysis](HYBRID_MODEL_ANALYSIS.md) | Records classicalâ€“transformer hybrid feasibility and explainability limits. | Transformer hybrid excluded; no completed transformer artifact |
| [Ensemble comparison](ENSEMBLE_COMPARISON.md) | Compares ensemble trade-offs with individual classical models. | Complete; LinearSVC remains champion |
| [Production deployment impact](PRODUCTION_DEPLOYMENT_IMPACT.md) | Assesses resource, operational, and deployment implications of ensembles. | Complete; no ensemble integration/approval |
| [Multilingual evaluation](MULTILINGUAL_EVALUATION.md) | Records the Phase 4.4 compatibility protocol, full metric suite, and strict evidence boundary. | Complete; English benchmark retained, Hindi/Hinglish accuracy not validated |
| [Hindi dataset analysis](HINDI_DATASET_ANALYSIS.md) | Documents Devanagari appearance, data insufficiency, and future data-governance requirements. | Complete; no Hindi corpus acquired |
| [Hinglish analysis](HINGLISH_ANALYSIS.md) | Documents Roman-Hindi routing, normalization, code-mix risks, and data limitations. | Complete; no Hinglish corpus acquired |
| [Language comparison](LANGUAGE_COMPARISON.md) | Compares tokenization and vocabulary-compatibility aggregates by detector-defined slice. | Complete; diagnostic only |
| [Multilingual error analysis](MULTILINGUAL_ERROR_ANALYSIS.md) | Records aggregate language-appearance error diagnostics and limitations. | Complete; no language-wise rate claim |
| [Multilingual research findings](MULTILINGUAL_RESEARCH_FINDINGS.md) | Synthesizes multilingual implications and next evidence gate. | Complete; no architecture or champion change |
| [Explainable AI framework](EXPLAINABLE_AI.md) | Defines reusable local SHAP/LIME explanations and global research analysis. | Complete for the existing LinearSVC champion |
| [Explanation methodology](EXPLANATION_METHODOLOGY.md) | Freezes XAI data access, reference, configuration, and reproducibility controls. | Complete; training-only aggregation |
| [XAI evaluation report](XAI_EVALUATION_REPORT.md) | Records technical validation and bounded research artifacts. | Complete; no validation/protected-test access |
| [Hyperparameter optimization report](HYPERPARAMETER_OPTIMIZATION_REPORT.md) | Records bounded grouped-CV searches, results, uncertainty, and tuning limits. | Complete; protected test not reused |
| [Final model selection report](FINAL_MODEL_SELECTION_REPORT.md) | Documents the conditional champion, challengers, and selection evidence. | Complete; untested after tuning |
| [Model versioning](MODEL_VERSIONING.md) | Defines model identifier, immutability, and release controls. | Effective for Phase 3.9 candidates |
| [Champion–challenger strategy](CHAMPION_CHALLENGER_STRATEGY.md) | Defines fair comparison, tie-breaking, promotion, and rollback gates. | Complete; research governance only |
| [Production model specification](PRODUCTION_MODEL_SPECIFICATION.md) | Defines the conditional candidate and explicit non-approval boundary. | Complete; deployment prohibited |
| [Phase 3 summary](../PHASE3_SUMMARY.md) | Summarizes the research and internal integration boundary across all Phase 3 milestones. | Complete; public deployment remains blocked |

The existing [Research Decision Log](../../research/decision-log/README.md) records accepted methodological decisions. The [Engineering Journal](../engineering-journal/README.md) records work completed in each milestone. Neither is a substitute for a dataset or experiment record.
