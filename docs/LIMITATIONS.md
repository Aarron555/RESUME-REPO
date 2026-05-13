# Limitations

This project is intentionally scoped. The limits below are documented so the repo remains useful, honest, and professional.

## 1. Deterministic stand-ins, not live API benchmarking

AXE-LAB currently uses deterministic stand-in clients for GPT, Claude, and local models. This keeps the repo reproducible and runnable without API keys. It does not measure real commercial model performance.

## 2. Small benchmark task set

The current task catalog is intentionally compact. It covers summarization, reasoning, code transformation, constrained output, and adversarial instruction conflict. It should not be treated as a broad universal benchmark.

## 3. Rubric scoring is heuristic

The rubric is useful for controlled comparison, but it is still heuristic. It does not replace human expert review, production observability, or real-world user testing.

## 4. Simulated cost model

Token-to-cost calculations use configurable pricing values. They demonstrate cost-aware evaluation design but should not be treated as official vendor billing estimates.

## 5. No universal HCM claim

The report only supports narrow task-level conclusions. If HCM outperforms both baselines on a task, it is marked helpful for that task. If it does not outperform both baselines, the repo does not claim improvement.

## 6. Dashboard is local review tooling

The Streamlit dashboard is intended for local inspection of generated artifacts. It is not deployed, authenticated, hardened, or production-ready.

## 7. Future production needs

A production-grade version would require:

- real API adapters
- response caching
- stronger statistical design
- larger task catalog
- model/version metadata
- trace IDs
- experiment registry
- artifact retention policy
- human review interface
- security and privacy review

## Safe public claim

Safe claim: AXE-LAB is a deterministic local evaluation harness for comparing prompt strategies and demonstrating AI workflow evaluation design.

Unsafe claim: AXE-LAB proves that one prompt system universally outperforms another across commercial LLMs.
