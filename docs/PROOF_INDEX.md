# Proof Index

This document compresses the repo into a fast proof map. It helps a reviewer connect project files to job-relevant capabilities.

## Featured proof asset: AXE-LAB

### Problem

Prompt workflows can be inconsistent, hard to compare, and easy to overclaim.

### What was built

A deterministic local evaluation harness that compares prompt strategies across controlled task types, validates outputs, retries failures, scores results, tags failures, estimates simulated cost, and generates reports.

### Tools and structure

- Python
- pytest
- Streamlit scaffold
- JSON artifacts
- YAML configuration
- GitHub Actions
- CLI runner
- Markdown documentation

### Evidence links inside repo

- `run.py` — command-line entrypoint
- `src/evaluator.py` — experiment orchestration
- `src/core/iteration_runner.py` — retry-loop logic
- `src/core/multi_model_runner.py` — deterministic model client interface
- `src/evaluation/validators/` — output validation
- `src/metrics.py` — scoring rubric
- `src/analysis/` — statistics and cost logic
- `results/report_generator.py` — report generator
- `results/report.md` — generated report output
- `tests/test_outputs.py` — tests
- `.github/workflows/tests.yml` — CI workflow

### Hiring relevance

This proves ability in AI workflow design, LLM evaluation, prompt-system testing, output validation, failure analysis, documentation, and QA-minded implementation.

## Related experience proof to connect in resume

### Tetris Pro Movers

Relevant evidence area:

- marketing automation
- paid ad workflow support
- customer messaging
- quote and booking follow-up
- service-business operations
- CRM-style lead tracking

Best role connection:

- Marketing Automation Specialist
- CRM Automation Specialist
- Customer Success Operations Specialist
- SaaS Implementation Specialist

### Multi-model generator builds

Relevant evidence area:

- prompt architecture
- reusable AI generators
- model comparison
- output formatting rules
- QA checks

Best role connection:

- AI Workflow Specialist
- Prompt Engineering Assistant
- AI Operations Specialist
- AI QA Analyst

### Product and mini-game prototypes

Relevant evidence area:

- product prototyping
- testing loops
- UI logic
- deployment attempts
- iterative development

Best role connection:

- Product Operations Associate
- Junior Product Builder
- AI Systems Builder

## Reviewer checklist

A reviewer should be able to answer:

- What problem does the project solve?
- What was built?
- How can it be run?
- What is simulated versus real?
- What files prove the core claims?
- What job skills does it demonstrate?
- What claims are intentionally avoided?

## Current proof strength

Strong:

- documentation quality
- reproducible local execution path
- evaluation workflow design
- careful claim control
- tests and CI scaffold

Still improving:

- screenshots and visual walkthrough
- real API adapters
- larger fixture catalog
- reviewer annotation workflow
