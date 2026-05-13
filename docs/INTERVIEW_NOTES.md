# Interview Notes

Use this document to explain AXE-LAB clearly in interviews without overclaiming.

## Short explanation

AXE-LAB is a deterministic local evaluation harness I built to compare prompt strategies across controlled tasks. It validates model outputs, retries failures, scores final outputs with a rubric, tags failure modes, estimates simulated cost, and generates evidence-backed reports.

## Why I built it

I wanted a project that shows more than prompting. The goal was to demonstrate how I would operationalize AI quality: define success criteria, run controlled experiments, validate outputs, track failures, and report conclusions carefully.

## What makes it relevant to business workflows

The same evaluation pattern can apply to:

- lead qualification prompts
- CRM follow-up drafts
- AI customer support replies
- marketing content generators
- structured JSON workflow outputs
- internal knowledge-base responses
- compliance-sensitive AI workflows

## How the system works

1. A config file defines tasks, systems, models, runs, retry limits, temperature, and seed.
2. The runner expands that into an experiment matrix.
3. A prompt builder generates the correct prompt format.
4. A deterministic model stand-in produces output.
5. A validator checks whether the output meets requirements.
6. A retry loop gives the system another attempt if the output fails.
7. A rubric scores the output across quality dimensions.
8. A failure taxonomy tags problems.
9. A report generator writes a readable Markdown report.

## Why deterministic stand-ins were used

I used deterministic stand-ins so the project could run locally without paid API keys and produce stable results during testing. The design still supports future real API adapters through the model-client interface.

## Strong technical talking points

- The model layer is abstracted through `ModelClient`.
- The runner is config-driven.
- Validators are task-specific.
- Rubric scoring is separated from generation.
- Reports are generated from structured artifacts.
- Tests check reproducibility and pipeline integrity.
- The project explicitly documents limitations and safe claims.

## Honest limitation statement

This is not a live commercial model benchmark yet. It is a deterministic evaluation harness simulator that demonstrates the workflow architecture and evaluation logic. A production version would add real API adapters, caching, larger task sets, reviewer annotations, and stronger statistical design.

## Best resume wording

Built AXE-LAB, a deterministic LLM evaluation harness comparing prompt strategies across controlled task types using validators, retry loops, rubric scoring, failure tagging, cost modeling, tests, and generated reports.

## Strong answer to: “What would you improve next?”

I would add optional real API adapters behind environment variables, implement response caching, expand the task fixture catalog, add dashboard filters, and allow human reviewers to annotate outputs. I would keep deterministic mode as the default CI path so tests remain stable.

## Strong answer to: “How is this useful for a company?”

A company could use this pattern to evaluate whether AI-generated workflow outputs are reliable enough to use. For example, it could evaluate CRM follow-up drafts, support responses, structured JSON outputs, internal knowledge-base answers, or marketing copy before those workflows are handed off to staff or customers.