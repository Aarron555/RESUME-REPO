# HCM Evaluation Council Report

## Condition Means (Rubric)
- Casual: 0.9153
- Structured: 0.9598
- HCM: 0.9414

## Task-by-Task Evidence
| Task | Casual | Structured | HCM | HCM vs Casual % | HCM vs Structured % | HCM Helped | Narrow Valid Condition |
|---|---:|---:|---:|---:|---:|---|---|
| adversarial_injection | 0.9883 | 0.9850 | 0.9900 | 0.17% | 0.51% | True | valid when instruction/risk constraints are explicit |
| code_transformation | 0.8417 | 0.9367 | 0.8892 | 5.64% | -5.07% | False | not supported for this task |
| constrained_output | 0.9455 | 0.9514 | 0.9950 | 5.24% | 4.58% | True | valid when instruction/risk constraints are explicit |
| reasoning | 0.9761 | 0.9883 | 0.9828 | 0.68% | -0.56% | False | not supported for this task |
| summarization | 0.8250 | 0.9375 | 0.8500 | 3.03% | -9.33% | False | not supported for this task |

## Failures by Category
- format_failure
- instruction_miss
- hallucination_proxy_trigger
- adversarial_breakdown
- structural_violation

## Final Evidence-backed Conclusion
HCM improves quality only on tasks where scores exceed both baselines; no universal claim.