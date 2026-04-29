"""Statistical analysis layer for AXE-LAB experiments."""

from __future__ import annotations

import math
import random
from collections import defaultdict
from typing import Any, Dict, List, Tuple


def _mean(values: List[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def _variance(values: List[float]) -> float:
    if len(values) < 2:
        return 0.0
    m = _mean(values)
    return sum((v - m) ** 2 for v in values) / (len(values) - 1)


def _ci95(values: List[float]) -> Tuple[float, float]:
    if not values:
        return (0.0, 0.0)
    m = _mean(values)
    if len(values) == 1:
        return (m, m)
    std = math.sqrt(_variance(values))
    margin = 1.96 * (std / math.sqrt(len(values)))
    return (m - margin, m + margin)


def _cohens_d(a: List[float], b: List[float]) -> float:
    if not a or not b:
        return 0.0
    va = _variance(a)
    vb = _variance(b)
    pooled = ((len(a) - 1) * va + (len(b) - 1) * vb) / max(1, (len(a) + len(b) - 2))
    if pooled == 0:
        return 0.0
    return (_mean(a) - _mean(b)) / math.sqrt(pooled)


def _permutation_p_value(a: List[float], b: List[float], n_perm: int = 5000, seed: int = 1337) -> float:
    if not a or not b:
        return 1.0
    observed = abs(_mean(a) - _mean(b))
    merged = a + b
    count = 0
    rng = random.Random(seed)
    for _ in range(n_perm):
        rng.shuffle(merged)
        pa = merged[: len(a)]
        pb = merged[len(a) :]
        if abs(_mean(pa) - _mean(pb)) >= observed:
            count += 1
    return (count + 1) / (n_perm + 1)


def analyze(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    grouped = defaultdict(lambda: defaultdict(list))
    by_task = defaultdict(lambda: defaultdict(list))

    for row in records:
        system = row["system"]
        task = row["task_id"]
        overall = row["metrics"]["overall"]
        grouped[system]["overall"].append(overall)
        by_task[task][system].append(overall)

    summary = {}
    for system, payload in grouped.items():
        values = payload["overall"]
        ci_low, ci_high = _ci95(values)
        summary[system] = {
            "mean": round(_mean(values), 4),
            "variance": round(_variance(values), 4),
            "ci95": [round(ci_low, 4), round(ci_high, 4)],
            "n": len(values),
        }

    task_breakdown = {}
    for task_id, system_values in by_task.items():
        task_breakdown[task_id] = {}
        for system, values in system_values.items():
            task_breakdown[task_id][system] = {
                "mean": round(_mean(values), 4),
                "variance": round(_variance(values), 4),
                "ci95": [round(x, 4) for x in _ci95(values)],
                "n": len(values),
            }

    axiom_values = grouped["axiom"]["overall"]
    baseline_values = grouped["baseline"]["overall"]
    structured_values = grouped["structured"]["overall"]

    pairwise = {
        "axiom_vs_baseline": {
            "p_value": round(_permutation_p_value(axiom_values, baseline_values), 6),
            "cohens_d": round(_cohens_d(axiom_values, baseline_values), 4),
            "mean_delta": round(_mean(axiom_values) - _mean(baseline_values), 4),
        },
        "axiom_vs_structured": {
            "p_value": round(_permutation_p_value(axiom_values, structured_values), 6),
            "cohens_d": round(_cohens_d(axiom_values, structured_values), 4),
            "mean_delta": round(_mean(axiom_values) - _mean(structured_values), 4),
        },
    }

    return {
        "summary_by_system": summary,
        "summary_by_task": task_breakdown,
        "pairwise_tests": pairwise,
    }
