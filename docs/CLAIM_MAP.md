# Claim Map

This file maps resume-safe claims to evidence inside AXE-LAB. It helps reviewers understand what the repo proves and what it does not prove.

## Resume-safe claims

### Built a deterministic LLM evaluation harness

Evidence:

- `run.py` provides the CLI entrypoint.
- `src/evaluator.py` runs the experiment matrix.
- `config/experiment.yaml` defines models, prompt systems, tasks, run counts, retry limits, temperature, and seed.

Safe wording:

> Built a deterministic LLM evaluation harness for comparing prompt strategies across controlled task categories.

### Designed prompt-system evaluation workflows

Evidence:

- `src/prompts.py` builds prompts for casual, structured, and HCM systems.
- `src/evaluator.py` expands the experiment across models, systems, tasks, and repeated runs.

Safe wording:

> Designed prompt-system evaluation workflows comparing casual, structured, and recursive prompting patterns.

### Implemented output validation and retry behavior

Evidence:

- `src/core/iteration_runner.py` executes the retry loop.
- `src/evaluation/validators/` contains validators for task-specific output checks.

Safe wording:

> Implemented retry-loop behavior and task-specific validators for structured AI output evaluation.

### Created rubric-based AI output scoring

Evidence:

- `src/metrics.py` defines rubric keys and scoring logic.
- Generated artifacts include rubric means and condition comparisons.

Safe wording:

> Created rubric-based scoring for instruction adherence, completeness, risk handling, and usability.

### Generated evidence-backed reports

Evidence:

- `results/report_generator.py` creates a Markdown report.
- `results/report.md` shows generated condition means and task comparisons.

Safe wording:

> Generated human-readable reports that summarize task-level evidence and avoid unsupported universal claims.

### Built cost-aware evaluation logic

Evidence:

- `src/analysis/cost_model.py` converts token counts into configurable simulated cost estimates.
- `config/pricing.yaml` stores pricing values.

Safe wording:

> Built configurable cost-modeling logic to estimate experiment cost across simulated model runs.

### Added tests for reproducibility and output structure

Evidence:

- `tests/test_outputs.py` checks record counts, blind-evaluation metadata, rubric completeness, and reproducibility.

Safe wording:

> Added automated tests covering benchmark matrix completeness, blind-evaluation metadata, rubric output shape, and deterministic reproducibility.

## Claims that should not be made yet

Do not claim:

- Live production benchmarking of GPT, Claude, or local models.
- Universal superiority of HCM prompting.
- Enterprise-grade AI evaluation platform.
- Production deployment readiness.

## Strong public project description

> AXE-LAB is a deterministic local evaluation harness that compares prompt strategies across controlled task types using validators, rubric scoring, retry loops, failure tagging, cost modeling, and generated reports.
