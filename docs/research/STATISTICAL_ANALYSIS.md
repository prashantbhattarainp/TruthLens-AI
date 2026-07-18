# Phase 3.8 Statistical Analysis

## Uncertainty method

Macro F1 confidence intervals use 1,000 deterministic percentile bootstrap resamples of the aligned out-of-fold training predictions, seed 42. They quantify uncertainty for this frozen training cohort; they are not population-wide claims.

| Model | OOF Macro F1 | 95% bootstrap interval |
| --- | ---: | ---: |
| Linear SVM | 0.5323 | [0.5199, 0.5444] |
| Logistic Regression | 0.4976 | [0.4855, 0.5091] |
| Multinomial NB | 0.4251 | [0.4158, 0.4353] |

## Paired comparisons

Linear SVM is the left-hand comparator. Fold-level Macro F1 comparisons use the five aligned grouped-CV folds. McNemar's exact binomial test uses aligned out-of-fold correctness, so it evaluates accuracy disagreement rather than the primary Macro F1 metric.

| Comparison | Mean Macro F1 difference | 95% t interval | Paired t p | Wilcoxon p | Cohen dz | McNemar direction |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Linear SVM − Logistic Regression | 0.0348 | [0.0158, 0.0538] | 0.0070 | 0.0625 | 2.2768 | Logistic Regression has more accuracy-only correct predictions (811 vs 520; p < 1e-8) |
| Linear SVM − Multinomial NB | 0.1071 | [0.0905, 0.1237] | 0.000057 | 0.0625 | 7.9973 | Multinomial NB has more accuracy-only correct predictions (1,093 vs 809; p < 1e-8) |

## Interpretation limits

The paired t results support the observed Macro F1 advantage within these five folds, but the exact two-sided Wilcoxon p-value is 0.0625 in both comparisons. With only five folds, this non-parametric test has coarse, low power. McNemar points in the opposite direction because the competing models' higher REAL-biased accuracy is not the selection objective. These tests should be read as descriptive supporting evidence, not as a broad claim of superiority. No multiple-comparison adjustment or hyperparameter search was performed.
