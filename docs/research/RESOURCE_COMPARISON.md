# Resource Comparison - Phase 4.2

**Scope:** Measured local execution context and candidate resource evidence.  
**Measurement date:** 2026-07-18.

## Local execution environment

| Resource | Observed value |
| --- | --- |
| Accelerator | No CUDA-visible NVIDIA GPU (`nvidia-smi` unavailable; PyTorch CUDA false) |
| CPU | 12 logical processors; PyTorch reported 8 execution threads |
| Memory | 15.6 GiB total; 4.2 GiB available at pre-run measurement |
| Disk | 271.6 GiB free on the repository and temporary-runtime volume |
| Runtime | CPU PyTorch 2.13.0, Transformers 5.14.1, Accelerate 1.14.0, scikit-learn 1.9.0 |

The project’s OneDrive path caused a Windows filename-length error while PyTorch unpacked third-party license files. The transformer runtime therefore uses a short temporary virtual environment. Source dependencies remain declared in `ml-service/requirements.txt`; individual artifact manifests preserve the resolved package versions and hardware evidence needed to reproduce a run on an equivalent environment.

## Candidate resource state

| Candidate | Download/load state | Training state | Measured training / inference | Resource conclusion |
| --- | --- | --- | --- | --- |
| IndicBERT | Upstream gated access rejected | Not started | None | Access-limited, not a performance result |
| DistilBERT | Public model load initiated | Stopped before checkpoint | >86 CPU-minutes; no validation/test result | Lower-cost challenger still exceeded the practical CPU benchmark window |
| BERT base | Not invoked | Not started | None | Larger encoder not attempted after lower-cost CPU limitation |
| RoBERTa base | Not invoked | Not started | None | Larger encoder not attempted after lower-cost CPU limitation |
| LinearSVC incumbent | Existing package | Not retrained | Existing service timing is not a comparable Phase 4.2 measurement | Retained as a low-resource internal baseline |

The runner records elapsed training seconds, training examples/second, validation and test inference seconds, and inference examples/second once a candidate completes. No candidate completed on this host, so no estimate is substituted for those metrics. The observed `>86 CPU-minutes` is a lower bound at interruption, not a completed training time.

## Interpretation limits

CPU-only timing is host-specific and must not be generalized to server, GPU, mobile, or batch-serving environments. A faster candidate is not automatically safer, more accurate, calibrated, or deployable. Likewise, a run prevented by access or resource limits is simply unevaluated rather than worse-performing.
