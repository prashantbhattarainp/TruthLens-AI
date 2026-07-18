# Ensemble Evaluation - Phase 4.3

**Status:** Complete, validation-only research evidence.  
**Decision authority:** [RDL-014](../../research/decision-log/RDL-014-Ensemble-Evaluation-and-Validation-Only-Boundary.md).  
**Artifact:** ignored `P43-classical-ensemble-20260718T125724Z`; code revision `c8a9733`.

## Protocol

The frozen `TL-BFNK-EN-v1.0` derivative and `SPL-TL-BFNK-EN-v1.0` split remain unchanged. All component pipelines received frozen Phase 3.9 preprocessing. Only validation (1,461 records) was evaluated. The protected test was not transformed, predicted, or used in any selection.

- Hard vote: FAKE when at least two of LinearSVC, MultinomialNB, and Logistic Regression output FAKE.
- Weighted hard vote: the same labels with fixed normalized train-only grouped-OOF Macro F1 weights: LinearSVC 0.3340, MultinomialNB 0.3291, Logistic Regression 0.3369.
- Soft vote: mean FAKE probability from MultinomialNB and Logistic Regression at threshold 0.5. LinearSVC is excluded because its margin is uncalibrated.
- Stacking: Logistic Regression (`C=1.0`, `lbfgs`, seed 42) fit on 6,813 aligned train-only OOF records. Its LinearSVC feature is a clipped sigmoid margin for scaling only, not a probability.

## Validation metrics

Precision and recall below are macro averages. Confusion matrices use `[REAL→REAL, REAL→FAKE; FAKE→REAL, FAKE→FAKE]`.

| Variant | Accuracy | Precision | Recall | Macro F1 | Weighted F1 | ROC-AUC | PR-AUC | MCC | Kappa | Confusion matrix |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| LinearSVC incumbent | 0.5941 | 0.5563 | 0.5457 | 0.5398 | 0.5734 | 0.5576 | 0.4641 | 0.1014 | 0.0971 | [685, 201; 392, 183] |
| MultinomialNB | 0.5647 | 0.5405 | 0.5397 | 0.5399 | 0.5626 | 0.5652 | 0.4672 | 0.0802 | 0.0802 | [582, 304; 332, 243] |
| Logistic Regression | 0.5585 | 0.5372 | 0.5371 | 0.5371 | 0.5583 | 0.5599 | 0.4620 | 0.0743 | 0.0743 | [565, 321; 324, 251] |
| Hard voting | 0.5825 | 0.5505 | 0.5459 | **0.5447** | 0.5726 | 0.5513 | 0.4353 | 0.0962 | 0.0949 | [636, 250; 360, 215] |
| Weighted voting | 0.5825 | 0.5505 | 0.5459 | **0.5447** | 0.5726 | 0.5509 | 0.4384 | 0.0962 | 0.0949 | [636, 250; 360, 215] |
| Soft voting | 0.5674 | 0.5447 | 0.5441 | 0.5443 | 0.5662 | **0.5688** | **0.4769** | 0.0888 | 0.0888 | [579, 307; 325, 250] |
| Stacking | **0.6092** | **0.6170** | 0.5053 | 0.3944 | 0.4712 | 0.5659 | 0.4722 | 0.0498 | 0.0128 | [880, 6; 565, 10] |

The accuracy-leading stacker is not a better fake-news detector: its high accuracy follows a near-universal REAL prediction and a FAKE recall of 10/575. Macro F1, recall, MCC, and the error review reject it as a practical challenger.

## Error analysis

| Variant | False positives | False negatives | Ambiguous FP / FN | Health FP / FN | Political FP / FN | Short FP / FN | Long FP / FN |
| --- | ---: | ---: | --- | --- | --- | --- | --- |
| LinearSVC | 201 | 392 | 87 / 189 | 28 / 55 | 63 / 113 | 19 / 60 | 26 / 48 |
| Hard / weighted vote | 250 | 360 | 107 / 175 | 36 / 48 | 69 / 111 | 23 / 58 | 33 / 45 |
| Soft vote | 307 | 325 | 132 / 158 | 44 / 41 | 79 / 99 | 35 / 55 | 37 / 40 |
| Stacking | 6 | 565 | 2 / 266 | 0 / 82 | 2 / 159 | 0 / 82 | 2 / 87 |

The cohorts overlap and are descriptive keyword/length heuristics, not topic, demographic, or factual labels. Source-level aggregate errors remain concentrated in higher-volume Indian fact-check-source cohorts such as Boomlive and India Today; no raw articles are published. Hard voting lowers false negatives by 32 versus the incumbent but adds 49 false positives. Soft voting lowers false negatives by 67 but adds 106 false positives. Stacking is unsuitable because its false-negative burden is extreme.

## Limits

These are one frozen-validation results, not post-tuning test evidence, confidence calibration, factual verification, fairness proof, or deployment approval. The small Macro F1 gain is within the incumbent's pre-existing practical-tie threshold and must not be promoted automatically.
