"""Statistics helpers aligned with AXE-LAB v4 records."""

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
    mean = _mean(values)
    return sum((value - mean) ** 2 for value in values) / (len(values) - 1)


def _ci95(values: List[float]) -> Tuple[float, float]:
    if not values:
        return (0.0, 0.0)
    mean = _mean(values)
    if len(values) == 1:
        return (mean, mean)
    margin = 1.96 * (math.sqrt(_variance(values)) / math.sqrt(len(values)))
    return (mean - margin, mean + margin)


def _cohens_d(left: List[float], right: List[float]) -> float:
    if not left or not right:
        return 0.0
    left_var = _variance(left)
    right_var = _variance(right)
    pooled = ((len(left) - 1) * left_var + (len(right) - 1) * right_var) / max(1, len(left) + len(right) - 2)
    if pooled == 0:
        return 0.0
    return (_mean(left) - _mean(right)) / math.sqrt(pooled)


def _permutation_p_value(left: List[float], right: List[float], seed: int = 1337, n_perm: int = 1000) -> float:
    if not left or not right:
        return 1.0
    observed = abs(_mean(left) - _mean(right))
    merged = list(left) + list(right)
    count = 0
    rng = random.Random(seed)
    for _ in range(n_perm):
        rng.shuffle(merged)
        sample_left = merged[: len(left)]
        sample_right = merged[len(left) :]
        if abs(_mean(sample_left) - _mean(sample_right)) >= observed:
            count += 1
    return (count + 1) / (n_perm + 1)


def _record_score(row: Dict[str, Any]) -> float:
    return float(row["rubric"]["rubric_mean"])


def _system(row: Dict[str, Any]) -> str:
    return str(row.get("system_type", row.get("system")))


def _task(row: Dict[str, Any]) -> str:
    return str(row.get("task_type", row.get("task_id")))


def _summary(values: List[float]) -> Dict[str, Any]:
    ci_low, ci_high = _ci95(values)
    return {
        "mean": round(_mean(values), 4),
        "variance": round(_variance(values), 4),
        "ci95": [round(ci_low, 4), round(ci_high, 4)],
        "n": len(values),
    }


def analyze(records: List[Dict[str, Any]], seed: int = 1337) -> Dict[str, Any]:
    grouped = defaultdict(list)
    by_task = defaultdict(lambda: defaultdict(list))

    for row in records:
        system = _system(row)
        task = _task(row)
        score = _record_score(row)
        grouped[system].append(score)
        by_task[task][system].append(score)

    summary_by_system = {key: _summary(value) for key, value in sorted(grouped.items())}
    summary_by_task = {
        task: {system: _summary(values) for system, values in sorted(system_map.items())}
        for task, system_map in sorted(by_task.items())
    }

    pairwise_tests = {}
    for left, right in [("hcm", "casual"), ("hcm", "structured"), ("structured", "casual")]:
        left_values = grouped.get(left, [])
        right_values = grouped.get(right, [])
        if left_values and right_values:
            pairwise_tests[f"{left}_vs_{right}"] = {
                "p_value": round(_permutation_p_value(left_values, right_values, seed=seed), 6),
                "cohens_d": round(_cohens_d(left_values, right_values), 4),
                "mean_delta": round(_mean(left_values) - _mean(right_values), 4),
            }

    return {
        "summary_by_system": summary_by_system,
        "summary_by_task": summary_by_task,
        "pairwise_tests": pairwise_tests,
    }
