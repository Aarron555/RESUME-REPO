# AXE-LAB v4 (PERS)

Ground-truth validated, cost-aware, iteration-simulating LLM evaluation framework.

## Measures

- True task success (validator pass/fail)
- Retry-loop behavior (attempts to success)
- Economic cost (token-to-$ model)
- Failure persistence
- Cross-model efficiency

## Run

```bash
python run.py
```

Optional dashboard:

```bash
python run.py --dashboard
```

## Tests

```bash
python -m pytest -q
```
