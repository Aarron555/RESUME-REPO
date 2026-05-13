# AXE-LAB Case Study

## One-sentence summary

AXE-LAB is a deterministic local evaluation harness that compares prompt strategies across controlled task types, scores outputs with a rubric, tags failure modes, estimates simulated cost, and generates evidence-backed reports.

## Problem

LLM workflows are often judged by intuition instead of repeatable evaluation. Teams may assume a prompt style is better without measuring whether it actually improves output quality, reliability, format compliance, or risk handling.

AXE-LAB addresses that problem by turning prompt comparison into a repeatable local experiment.

## Target user

AXE-LAB is useful for:

- AI workflow specialists testing prompt patterns.
- AI operations teams checking output reliability.
- Product operators comparing automation quality.
- LLM evaluators reviewing task-specific behavior.
- Automation builders validating whether a prompt workflow is reliable enough to hand off.

## Build goal

The goal was to create a professional, reproducible proof-of-work project that demonstrates:

- structured AI workflow design
- prompt strategy comparison
- validation and retry loops
- rubric-based output scoring
- failure analysis
- generated reporting
- careful claim control

## System design

The project runs an experiment matrix across:

- model categories: GPT, Claude, local
- prompt systems: casual, structured, HCM recursive
- task categories: summarization, reasoning, code transformation, constrained output, adversarial instruction conflict

Each run produces a final output, validation result, attempt log, simulated token cost, rubric score, and failure tags.

## Why deterministic stand-ins

The current model layer uses deterministic stand-ins rather than live APIs. That decision makes the project:

- runnable without paid API keys
- stable for local testing
- reproducible for reviewers
- safe for CI environments
- easy to extend later with real adapters

This is a deliberate engineering tradeoff. The project demonstrates the evaluation harness and workflow architecture, not live commercial model performance.

## Evaluation flow

1. Load experiment configuration.
2. Build prompt for each task and prompt system.
3. Generate deterministic model output.
4. Validate output against task-specific expectations.
5. Retry if validation fails.
6. Score final output using a rubric.
7. Tag failure modes.
8. Compute cross-model and cross-system summaries.
9. Generate a Markdown report.
10. Optionally inspect results in the dashboard scaffold.

## Key implementation areas

- `run.py` — CLI entrypoint
- `src/evaluator.py` — experiment orchestration
- `src/core/` — model stand-ins and retry loop
- `src/evaluation/validators/` — task-specific validation
- `src/metrics.py` — rubric scoring and HCM summary
- `src/analysis/` — cost and statistics helpers
- `results/report_generator.py` — report generation
- `tests/` — reproducibility and pipeline checks

## What the project proves

AXE-LAB proves that I can design and implement a structured AI evaluation workflow with clear inputs, outputs, validation rules, scoring logic, documentation, and tests.

It also demonstrates the discipline to avoid exaggerated AI claims. The generated conclusion is intentionally narrow: HCM only counts as helpful where task-level scores beat both baselines.

## What the project does not prove

AXE-LAB does not prove that one prompt strategy universally outperforms all others. It also does not claim live model performance across commercial LLM providers. Those would require real API adapters, larger task sets, and a more rigorous statistical design.

## Business relevance

A company could adapt this pattern to evaluate:

- AI customer support responses
- CRM follow-up drafts
- marketing automation copy
- internal knowledge-base answers
- structured JSON outputs
- lead qualification workflows
- policy-compliance responses
- workflow handoff quality

## Resume-safe project bullet

Built AXE-LAB, a deterministic LLM evaluation harness comparing prompt strategies across controlled task types using validators, retry loops, rubric scoring, failure tagging, cost modeling, tests, and generated reports.

## Next upgrade

The strongest next technical upgrade is adding optional real API adapters behind environment variables while keeping deterministic mode as the default test path.