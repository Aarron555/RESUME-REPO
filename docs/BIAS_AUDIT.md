# Bias Audit

AXE-LAB is designed to be bias-resistant, not bias-free. This file documents where bias can enter the evaluation and how the project controls or mitigates it.

## Bias-control goal

The goal is to avoid overclaiming. AXE-LAB should support narrow, evidence-backed conclusions about controlled prompt-system comparisons, not universal claims about model quality or prompt superiority.

## Current bias controls

- Deterministic runs use a fixed seed for reproducibility.
- The same task catalog is used across prompt systems.
- The same validation rules are applied to each output.
- Rubric dimensions are defined in code instead of evaluated casually.
- Failure modes are tagged explicitly.
- Reports state when HCM does not beat both baselines.
- Documentation clearly states that current model clients are deterministic stand-ins.
- Limitations are public and linked from the README.

## Known bias sources

### 1. Simulated model outputs

The current GPT, Claude, and local clients are deterministic stand-ins. This keeps the project runnable, but it means results reflect simulator design choices rather than live commercial model behavior.

Mitigation:

- State this clearly in README and LIMITATIONS.
- Keep deterministic mode as the default test path.
- Add optional live API adapters later.

### 2. Human-designed rubric

The rubric reflects design choices about what counts as quality.

Mitigation:

- Keep rubric keys visible in `src/metrics.py`.
- Add task-success metrics alongside rubric scores.
- Add reviewer annotations in a future version.

### 3. Prompt-system parity

A recursive or structured prompt may contain more explicit constraints than a casual baseline.

Mitigation:

- Use the same task input, expected output, validation rules, retry limits, and seed across systems.
- Document prompt construction in `src/prompts.py`.
- Add baseline parity checks in future tests.

### 4. Small task set

Five controlled task types are useful for proof-of-work, but not enough for broad scientific conclusions.

Mitigation:

- Treat current results as portfolio-level evidence.
- Expand fixtures gradually.
- Add larger randomized task sets later.

### 5. Portfolio presentation bias

Because this repository is also proof of work, it can be tempting to frame results too strongly.

Mitigation:

- Use `docs/CLAIM_MAP.md` for resume-safe wording.
- Use `docs/LIMITATIONS.md` to document boundaries.
- Keep generated conclusions narrow.

## Pass / fail standard for claims

A claim is acceptable only if it is supported by code, generated artifacts, tests, or documentation.

A claim should be rejected if it suggests:

- live commercial benchmark results that were not produced
- universal superiority of one prompt method
- production deployment readiness
- security or compliance certification

## Bias-resistant public wording

Safe wording:

> AXE-LAB is a deterministic LLM evaluation harness simulator that compares prompt strategies under controlled local conditions and documents limitations to avoid unsupported claims.

Avoid wording:

> AXE-LAB proves one prompt system is universally better than another.

## Next bias-reduction upgrades

- Add real API adapters behind environment variables.
- Add response caching.
- Add task fixture expansion.
- Add human-review annotations.
- Add baseline parity tests.
- Add multiple scoring modes.
- Add report confidence notes.
