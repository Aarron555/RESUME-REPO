"""Token-to-cost conversion and aggregation."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List


def load_pricing(path: str = "config/pricing.yaml") -> Dict[str, Dict[str, float]]:
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    pricing: Dict[str, Dict[str, float]] = {}
    current = None
    for line in lines:
        if not line.strip() or line.strip().startswith("#"):
            continue
        if line.startswith("  "):
            key, value = line.strip().split(":", 1)
            pricing[current][key.strip()] = float(value.strip())
        else:
            key = line.replace(":", "").strip()
            pricing[key] = {}
            current = key
    return pricing


def compute_call_cost(input_tokens: int, output_tokens: int, model_name: str, pricing: Dict[str, Dict[str, float]]) -> float:
    rates = pricing[model_name]
    return round((input_tokens * rates["input"]) + (output_tokens * rates["output"]), 8)


def aggregate_costs(records: List[Dict[str, Any]]) -> Dict[str, float]:
    total_cost = sum(r["total_cost"] for r in records)
    total_runs = len(records)
    successes = [r for r in records if r["success"]]
    failures = [r for r in records if not r["success"]]

    return {
        "total_cost": round(total_cost, 8),
        "avg_cost_per_run": round(total_cost / total_runs, 8) if total_runs else 0.0,
        "cost_per_success": round(total_cost / len(successes), 8) if successes else 0.0,
        "cost_per_failure": round(sum(r["total_cost"] for r in failures) / len(failures), 8) if failures else 0.0,
    }
