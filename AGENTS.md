# SENTINEL-1 Engineering Protocol

This repository uses SENTINEL-1 as its AI-coding standard. Apply it to code, tests, automation, validators, scripts, workflow engines, CI, and any logic that handles user input or generated output.

## Core standard

- Treat all external inputs as untrusted.
- Prefer secure, boring, standard-library or well-vetted methods.
- Do not add placeholder logic such as `TODO: implement` in production paths.
- Do not hide complexity with vague comments; implement the full behavior or document the limit clearly.
- Keep claims and docs aligned with what the code actually does.

## Required workflow for code changes

1. Deconstruct the requirement into the smallest components.
2. Threat-model the change: injection, unsafe execution, data leakage, broken assumptions, race conditions, dependency risk, and failure modes.
3. Implement the complete change with readable code and clear error handling.
4. Add or update tests for at least one happy path and two failure modes where practical.
5. Run the relevant test suite and document anything that could not be verified.

## Repo-specific emphasis

AXE-LAB is a deterministic evaluation harness simulator. Do not imply live commercial model benchmarking unless real API adapters and corresponding tests are added.

High-risk files require extra care:

- `src/evaluation/validators/`
- `src/core/iteration_runner.py`
- `src/core/multi_model_runner.py`
- `src/evaluator.py`
- `run.py`
- `.github/workflows/`

## Output expectations

Every substantial change should include:

- clear implementation
- dependency notes if dependencies change
- tests or a reason tests are not applicable
- security assumptions
- limitation notes when relevant
