# Evaluation Method

AXE-LAB evaluates prompt-system behavior through a deterministic experiment matrix. The method is intentionally conservative: it compares outputs under controlled local conditions and reports only what the generated evidence supports.

## Prompt systems compared

- `casual`: minimal instruction style
- `structured`: clearer structure, output requirements, and task constraints
- `hcm`: recursive / council-style prompting with explicit role, review, and constraint emphasis

## Task categories

The current benchmark includes:

- summarization
- reasoning
- code transformation
- constrained JSON output
- adversarial instruction conflict

These are small controlled tasks, not a broad production benchmark.

## Deterministic model stand-ins

The model layer uses deterministic stand-ins for GPT, Claude, and local models. Each stand-in has a reliability setting and deterministic seeded behavior. This allows the harness to be run repeatedly without paid API keys or nondeterministic API responses.

This means the project measures the evaluation pipeline and prompt-strategy simulation, not live commercial model performance.

## Validation layer

Each task includes a validation type:

- math validation
- code-output validation
- JSON schema validation
- semantic keyword / exact-match validation

The retry loop runs until the validator passes or the configured max attempt count is reached.

## Rubric scoring

Final outputs are scored with rubric dimensions such as:

- instruction adherence
- evidence grounding
- completeness
- hallucination resistance
- usefulness
- clarity
- risk detection
- false-positive control
- revision efficiency
- executive usability

The rubric produces a `rubric_mean` used for cross-condition comparison.

## Failure taxonomy

The failure taxonomy tags common failure modes such as:

- format failure
- instruction miss
- hallucination proxy trigger
- adversarial breakdown
- structural violation

## Claim standard

A prompt system is only marked as helpful for a task when its score beats both comparison baselines for that task. This prevents overclaiming and keeps conclusions narrow.

## Why this matters

The project demonstrates a practical AI operations habit: treat LLM outputs as measurable system behavior, not magic. It shows how to create a repeatable evaluation loop, define success criteria, capture failures, and report conclusions with controlled language.
