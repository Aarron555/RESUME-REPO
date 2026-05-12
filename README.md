# AXE-LAB v4 — HCM Evaluation Council Mode

This repo benchmarks **casual vs structured vs HCM recursive prompts** across multiple models and tasks.

It performs:
- blind output scoring
- rubric-based quality scoring
- failure taxonomy tagging
- task-level HCM improvement percentage calculation
- evidence-backed final conclusions (no universal claims)

## Run

```bash
python run.py
```

## Test

```bash
python -m pytest -q
```
