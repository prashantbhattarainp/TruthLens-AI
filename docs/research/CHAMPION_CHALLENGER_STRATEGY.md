# Champion–Challenger Strategy

## Purpose and scope

This is a research comparison and release-control strategy, not an online experimentation or automatic deployment policy. The champion and challengers use identical frozen data lineage, TF-IDF representation, preprocessing configuration, grouped five-fold training protocol, seed 42, and the same validation partition.

## Selection rule

1. Rank by validation Macro F1 after training-only grouped CV search.
2. Treat candidates within 0.005 Macro F1 as a practical tie.
3. Break a practical tie using grouped OOF Macro F1 and its variability, MCC, FAKE-class recall, artifact/resource footprint, and train–validation gap.
4. Reject any candidate with a leakage violation, unrecorded data/configuration lineage, failed artifact integrity check, or unsupported usage claim.
5. Never use the historic Phase 3.8 protected-test result to select among tuned candidates.

The tuned Linear SVM is champion because it is practically tied with MNB on validation Macro F1 while showing stronger OOF Macro F1, MCC, and resource efficiency. MNB is not discarded: its FAKE recall and ranking metrics are better and it becomes the first challenger when a new evaluation protocol is approved.

## Promotion, rollback, and monitoring gates

Promotion is blocked until a future version has independently approved calibration, fairness/slice, robustness, legal/data-rights, security, human-review, and fresh protected-test evidence. Any source-distribution shift, language expansion, changed preprocessing/features, drift, or materially worse FAKE recall triggers investigation and a new version rather than an in-place update. Rollback means reclassifying a release record as retracted or superseded; it never changes its recorded metrics or lineage.
