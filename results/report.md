# AXE-LAB v4 Benchmark Report

## Efficiency Ranking (Primary Metrics)
| Rank | System | Success Rate | Cost/Success | Avg Attempts |
|---:|---|---:|---:|---:|
| 1 | structured | 1.0000 | $0.00005976 | 1.2133 |
| 2 | axiom | 1.0000 | $0.00009024 | 1.2600 |
| 3 | baseline | 0.9667 | $0.00006932 | 1.2623 |

## Cost Comparison by Model × System
| Model | System | Success Rate | Failure Persistence | Cost/Success | Efficiency Gain vs Baseline |
|---|---|---:|---:|---:|---:|
| gpt | baseline | 0.9800 | 0.0200 | $0.00010484 | 0.00000000 |
| gpt | structured | 1.0000 | 0.0000 | $0.00009164 | 0.00001320 |
| gpt | axiom | 1.0000 | 0.0000 | $0.00013804 | -0.00003320 |
| claude | baseline | 0.9800 | 0.0200 | $0.00008667 | 0.00000000 |
| claude | structured | 1.0000 | 0.0000 | $0.00007470 | 0.00001197 |
| claude | axiom | 1.0000 | 0.0000 | $0.00011182 | -0.00002515 |
| local | baseline | 0.9400 | 0.0600 | $0.00001646 | 0.00000000 |
| local | structured | 1.0000 | 0.0000 | $0.00001294 | 0.00000352 |
| local | axiom | 1.0000 | 0.0000 | $0.00002085 | -0.00000439 |

## Retry Reduction Comparison
| Model | Baseline Attempts | Structured Attempts | AXIOM Attempts |
|---|---:|---:|---:|
| gpt | 1.2449 | 1.2000 | 1.2200 |
| claude | 1.2653 | 1.2000 | 1.2200 |
| local | 1.2766 | 1.2400 | 1.3400 |

## Statistical Conclusions
- claude: AXIOM vs BASELINE (Δsuccess=0.02, Δcost=-2.688e-05, p=0.547151, d=0.2); AXIOM vs STRUCTURED (Δsuccess=0.0, Δcost=-3.712e-05, p=1.0, d=0.0)
- gpt: AXIOM vs BASELINE (Δsuccess=0.02, Δcost=-3.53e-05, p=0.524492, d=0.2); AXIOM vs STRUCTURED (Δsuccess=0.0, Δcost=-4.64e-05, p=1.0, d=0.0)
- local: AXIOM vs BASELINE (Δsuccess=0.06, Δcost=-5.38e-06, p=0.106964, d=0.3537); AXIOM vs STRUCTURED (Δsuccess=0.0, Δcost=-7.91e-06, p=1.0, d=0.0)

## AXIOM_STATUS: **PARTIAL**
