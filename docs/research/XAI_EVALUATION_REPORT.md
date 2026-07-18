# XAI Evaluation Report

## Result

Phase 4.1 successfully generated SHAP and LIME metadata for a synthetic ML-service request using the packaged champion. The SHAP additivity residual was within floating-point precision (`2.8e-17` in the synthetic smoke check). The LIME local surrogate returned a finite fidelity score (`0.824` in that check) using the fixed 1,000-sample default.

## Global artifact run

The report generator processed 512 class-balanced training records from `DER-20260718-r2`; it did not access validation or protected-test records. It generated five 300-DPI PNG figures, a manifest, and an aggregate feature-importance JSON record. Figure terms demonstrate strong vocabulary/template sensitivity and must not be turned into claims about facts, sources, or people.

## Quality checks

| Check | Outcome |
| --- | --- |
| Existing package load | Passed |
| Frozen preprocessing smoke case | Passed |
| SHAP local additivity | Passed |
| LIME deterministic metadata | Passed |
| Confidence remains unavailable | Passed |
| Backend lint | Passed |
| Validation/protected-test access | None |

The result is research explainability evidence, not a production-release gate.
