# AXE-LAB v4 — Deterministic LLM Evaluation Harness

AXE-LAB is a reproducible local evaluation harness for comparing prompt-system strategies across task types. It benchmarks casual, structured, and HCM recursive prompting patterns using deterministic model stand-ins, rubric scoring, failure taxonomy tagging, cost simulation, generated reports, and a Streamlit-ready dashboard.

This project is designed as professional proof of work for AI workflow, prompt evaluation, AI operations, QA, product operations, and automation roles.

## Recruiter summary

Built AXE-LAB, a deterministic LLM evaluation harness that compares casual, structured, and recursive prompt strategies across task types using rubric scoring, failure taxonomy tagging, reproducible experiment runs, cost modeling, and generated reports to support evidence-based AI workflow evaluation.

## Scope note

AXE-LAB currently uses deterministic stand-in model clients for GPT, Claude, and local models. This keeps the project runnable without external API keys and makes test results reproducible. It should be evaluated as a deterministic evaluation harness simulator, not as a live production benchmark of commercial model APIs.

Future versions can add real OpenAI, Anthropic, and local model adapters behind the same ModelClient interface.

## What this project demonstrates

- Structured LLM workflow design
- Prompt-system comparison across task categories
- Deterministic test harness design
- Human-readable report generation
- Failure taxonomy and risk tagging
- Rubric-based AI output evaluation
- Cost-aware execution modeling
- Local-first reproducibility without API keys
- Automated tests and CI-ready project structure
- Documentation suitable for technical and non-technical review

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

## Run tests

```bash
python -m pytest -q
```

## Optional dashboard

```bash
python run.py --dashboard
```

## Repository map

```text
config/          experiment and pricing configuration
benchmarks/      generated JSON benchmark artifacts
docs/            architecture, method, limitations, and claim map
results/         generated Markdown report and report generator
src/analysis/    cost and statistics logic
src/core/        model stand-ins and retry loop
src/dashboard/   Streamlit dashboard entrypoint
src/evaluation/  validators and failure taxonomy
src/reporting/   live explanation helpers
tests/           reproducibility and pipeline tests
run.py           CLI entrypoint
```

## Example conclusion

The generated report is intentionally conservative: HCM improves quality only on tasks where scores exceed both baselines. No universal claim is made.

## Professional positioning

This project supports roles such as AI Workflow Specialist, AI Operations Specialist, LLM Evaluation Assistant, Prompt Engineering Assistant, Product Operations Associate, Automation Systems Coordinator, AI QA / Model Output Evaluator, and AI Systems Builder.

## What is intentionally not claimed

This repo does not claim production-grade commercial LLM benchmarking, universal superiority of recursive prompting, real API performance measurements, security certification, or enterprise deployment readiness.

It does demonstrate evaluation system design, reproducible local experiments, structured output validation, rubric design, failure analysis, careful claim control, and evidence-backed reporting.

## Review path for hiring teams

1. Read docs/RECRUITER_GUIDE.md
2. Run python -m pytest -q
3. Run python run.py
4. Inspect results/report.md
5. Review docs/CLAIM_MAP.md
