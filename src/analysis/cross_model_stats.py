"""Cross-model statistical analysis for AXE-LAB v4 primary metrics."""

from __future__ import annotations

import json
import math
import random
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List

from src.metrics import compute_primary_metrics

STAT_PATH = Path("benchmarks/statistical_summary.json")


def _mean(values: List[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def _variance(values: List[float]) -> float:
    if len(values) < 2:
        return 0.0
    m = _mean(values)
    return sum((v - m) ** 2 for v in values) / (len(values) - 1)


def _ci95(values: List[float]) -> List[float]:
    if not values:
        return [0.0, 0.0]
    m = _mean(values)
    if len(values) == 1:
        return [m, m]
    margin = 1.96 * math.sqrt(_variance(values) / len(values))
    return [m - margin, m + margin]


def _cohens_d(a: List[float], b: List[float]) -> float:
    if not a or not b:
        return 0.0
    va, vb = _variance(a), _variance(b)
    pooled = ((len(a) - 1) * va + (len(b) - 1) * vb) / max(1, len(a) + len(b) - 2)
    if pooled == 0:
        return 0.0
    return (_mean(a) - _mean(b)) / math.sqrt(pooled)


def _bootstrap_p_value(a: List[float], b: List[float], seed: int = 42, iterations: int = 3000) -> float:
    rng = random.Random(seed)
    observed = abs(_mean(a) - _mean(b))
    merged = a + b
    if not merged or not a or not b:
        return 1.0
    count = 0
    for _ in range(iterations):
        sa = [rng.choice(merged) for _ in range(len(a))]
        sb = [rng.choice(merged) for _ in range(len(b))]
        if abs(_mean(sa) - _mean(sb)) >= observed:
            count += 1
    return (count + 1) / (iterations + 1)


def compute_cross_model_statistics(records: List[Dict[str, Any]], seed: int = 42) -> Dict[str, Any]:
    primary = compute_primary_metrics(records)

    per_triplet_success = defaultdict(list)
    per_model_system_success = defaultdict(list)
    per_model_system_cost = defaultdict(list)

    for row in records:
        model, system, task = row["model_name"], row["system_type"], row["task_type"]
        success_value = 1.0 if row["success"] else 0.0
        per_triplet_success[(model, system, task)].append(success_value)
        per_model_system_success[(model, system)].append(success_value)
        per_model_system_cost[(model, system)].append(row["total_cost"])

    matrix: Dict[str, Dict[str, Dict[str, Any]]] = defaultdict(lambda: defaultdict(dict))
    for (model, system, task), vals in per_triplet_success.items():
        cost_vals = per_model_system_cost[(model, system)]
        matrix[model][system][task] = {
            "success_mean": round(_mean(vals), 4),
            "variance": round(_variance(vals), 4),
            "ci95": [round(x, 4) for x in _ci95(vals)],
            "avg_cost": round(_mean(cost_vals), 8),
            "n": len(vals),
        }

    pairwise = {}
    models = sorted({r["model_name"] for r in records})
    for model in models:
        ax_s = per_model_system_success[(model, "axiom")]
        ba_s = per_model_system_success[(model, "baseline")]
        st_s = per_model_system_success[(model, "structured")]

        ax_cost = _mean(per_model_system_cost[(model, "axiom")])
        ba_cost = _mean(per_model_system_cost[(model, "baseline")])
        st_cost = _mean(per_model_system_cost[(model, "structured")])

        pairwise[model] = {
            "axiom_vs_baseline": {
                "success_delta": round(_mean(ax_s) - _mean(ba_s), 4),
                "cost_delta": round(ba_cost - ax_cost, 8),
                "p_value": round(_bootstrap_p_value(ax_s, ba_s, seed=seed), 6),
                "cohens_d": round(_cohens_d(ax_s, ba_s), 4),
            },
            "axiom_vs_structured": {
                "success_delta": round(_mean(ax_s) - _mean(st_s), 4),
                "cost_delta": round(st_cost - ax_cost, 8),
                "p_value": round(_bootstrap_p_value(ax_s, st_s, seed=seed), 6),
                "cohens_d": round(_cohens_d(ax_s, st_s), 4),
            },
        }

    summary = {
        "primary_metrics": primary,
        "model_system_task_summary": matrix,
        "pairwise_by_model": pairwise,
    }

    STAT_PATH.parent.mkdir(parents=True, exist_ok=True)
    STAT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary
