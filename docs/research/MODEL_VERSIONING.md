# Model Versioning

## Convention

Model identifiers use `TL-<algorithm>-<representation>-v<major>.<minor>.<patch>-<stage>`.

- **Major** changes when dataset version, label semantics, split contract, or task definition changes.
- **Minor** changes for a governed hyperparameter/configuration change on the same dataset and split.
- **Patch** changes only for an identical-model artifact rebuild with verified identical inputs.
- **Stage** is `rc.N` until a release gate is independently satisfied. `rc` does not mean production approval.

## Phase 3 records

| Identifier | Parent evidence | Status |
| --- | --- | --- |
| `TL-LSVM-TFIDF-v1.0.0` | Phase 3.8 baseline `EXP-20260717-linear-svm-177d71e9c9` | Historical evaluated research candidate; protected test was consumed once. |
| `TL-LSVM-TFIDF-v1.1.0-rc.1` | Phase 3.9 optimization `OPT-20260718-linear-svm-faafafe15e` | Conditional champion, untested after tuning. |
| `TL-MNB-TFIDF-v1.1.0-rc.1` | `OPT-20260718-multinomial-naive-bayes-60fad40e22` | Primary challenger. |
| `TL-LR-TFIDF-v1.1.0-rc.1` | `OPT-20260718-logistic-regression-15115d5c12` | Recall/fairness challenger. |

Every version binds the dataset hash, derivative release, split, label mapping, preprocessing configuration hash, feature configuration hash, seed, environment, exact hyperparameters, artifact hash, and evidence location. Reusing the frozen dataset with modified code or tuning creates at least a minor candidate version; changing data governance creates a new major version.

## Immutability and release prohibition

The Phase 3.9 candidates are immutable research artifacts. They cannot be overwritten, silently retrained, or promoted using the Phase 3.8 protected test result. A deployment decision requires a new release record with newly authorized evidence; absence of such a record means the version is not deployable.
