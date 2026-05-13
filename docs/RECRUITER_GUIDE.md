# Recruiter Guide

AXE-LAB is a concise proof-of-work project for AI workflow, prompt evaluation, automation, QA, and product-operations roles.

## 30-second review

AXE-LAB is a deterministic evaluation harness that compares casual, structured, and recursive prompt strategies across controlled tasks. It runs repeatable experiments, validates outputs, scores results with a rubric, tags failure modes, estimates simulated cost, and generates a human-readable report.

## What to look at first

1. `README.md` — project summary and run instructions.
2. `run.py` — CLI entrypoint.
3. `src/evaluator.py` — experiment orchestration.
4. `src/metrics.py` — scoring rubric and task-level comparison logic.
5. `src/evaluation/validators/` — output validation layer.
6. `results/report.md` — generated report.
7. `docs/CLAIM_MAP.md` — resume-safe claim mapping.

## Skills demonstrated

- AI workflow design
- Prompt-system architecture
- Evaluation rubric design
- Failure taxonomy design
- Deterministic testing
- Reproducible experiment configuration
- Report generation
- Local-first tooling
- QA-minded documentation
- Careful claim control

## Role alignment

This project is most relevant to:

- AI Workflow Specialist
- AI Operations Assistant / Specialist
- Prompt Engineering Assistant
- LLM Evaluation Assistant
- Product Operations Associate
- Automation Systems Coordinator
- AI QA / Model Output Evaluator
- Marketing Automation / AI Systems Builder

## Important caveat

This repo uses deterministic stand-in clients for GPT, Claude, and local models. It is not claiming live commercial model benchmark results. It demonstrates the evaluation pipeline, prompt-system comparison method, reproducibility, and report logic.

## Suggested interview questions

- How would you replace deterministic stand-ins with real API adapters?
- How would you make this benchmark more statistically rigorous?
- What failure modes does the taxonomy detect?
- Where did HCM prompting help and where did it not help?
- How would this become an internal AI quality dashboard for a company?
- How would you adapt this to evaluate CRM, support, or marketing-automation workflows?

## Strongest project takeaway

The project shows the ability to build structured AI evaluation systems, not just write prompts. It demonstrates workflow thinking, controlled testing, documentation, and careful evidence-based conclusions.
