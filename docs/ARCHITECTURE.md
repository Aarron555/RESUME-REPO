# Architecture

AXE-LAB is organized as a local-first evaluation pipeline. The goal is not to call live commercial models by default; the goal is to provide a reproducible harness that can be reviewed, tested, and extended.

## Pipeline overview

1. `run.py` loads the experiment configuration.
2. `src.evaluator.load_experiment_config` parses `config/experiment.yaml`.
3. `src.evaluator.run_experiment` expands the matrix across models, prompt systems, tasks, and runs.
4. `src.prompts.build_prompt` creates the prompt for each system/task pair.
5. `src.core.multi_model_runner.get_model_client` returns a deterministic model stand-in.
6. `src.core.iteration_runner.run_iteration_loop` executes attempts and retries until validation passes or the attempt limit is reached.
7. `src.evaluation.validators` validates task outputs.
8. `src.metrics.score_rubric_blind` scores final outputs using a rubric.
9. `src.evaluation.failure_taxonomy.classify_failure_types` tags failure modes.
10. `src.analysis.cross_model_stats.compute_cross_model_statistics` summarizes condition and task-level performance.
11. `results.report_generator.generate_report` writes `results/report.md`.
12. `src.dashboard.app` can load generated artifacts for visual inspection.

## Core modules

### `src/core/`

Contains model execution abstractions and retry-loop logic. The current model clients are deterministic stand-ins, which keeps the repo runnable without paid API keys and makes test results stable.

### `src/evaluation/`

Contains validators for math, code, JSON format, and semantic expectations, plus failure taxonomy helpers.

### `src/analysis/`

Contains cost modeling and summary statistics. `cross_model_stats.py` is the active analysis path for the current data schema.

### `src/metrics.py`

Defines the rubric keys, blind scoring logic, and HCM council summary.

### `results/`

Contains generated reports and the report generation helper.

## Data artifacts

Generated artifacts are written to:

- `benchmarks/results.json`
- `benchmarks/statistical_summary.json`
- `results/report.md`
- `experiments/experiment_<timestamp>.json`

## Extension points

The cleanest extension point is the `ModelClient` interface in `src/core/multi_model_runner.py`. Real model adapters can be added later while preserving the same evaluator pipeline.

Potential future adapters:

- OpenAI API adapter
- Anthropic API adapter
- Local model adapter
- Cached response replay adapter

## Design principle

Every result should be reproducible, inspectable, and carefully scoped. The repo intentionally avoids universal claims about HCM or recursive prompting unless the measured task-level evidence supports them.
