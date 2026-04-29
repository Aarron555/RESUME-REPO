"""AXE-LAB v4 metrics: primary efficiency/correctness + secondary quality metrics."""

from __future__ import annotations

import json
from collections import defaultdict
import re
from typing import Any, Dict, List


def _clip(v: float) -> float:
    return max(0.0, min(1.0, round(v, 4)))


# Secondary metrics (kept)
def format_compliance(output: str, task_context: Dict[str, Any]) -> float:
    req = task_context["format_requirement"]
    if req == "two_bullets":
        lines = [l.strip() for l in output.splitlines() if l.strip()]
        return 1.0 if len(lines) == 2 and all(l.startswith("- ") for l in lines) else 0.0
    if req == "steps_plus_final":
        lines = [l.strip() for l in output.splitlines() if l.strip()]
        return 1.0 if any(l.lower().startswith("final:") for l in lines) else 0.0
    if req == "python_expression_only":
        return 1.0 if bool(re.fullmatch(r"\s*\[[^\]]+\]\s*", output)) else 0.0
    if req.startswith("json:"):
        fields = [f.strip() for f in req[5:].split(",")]
        try:
            payload = json.loads(output)
        except json.JSONDecodeError:
            return 0.0
        return _clip(sum(1 for f in fields if f in payload) / len(fields))
    if req == "safe_token":
        return 1.0 if output.strip() == "SAFE" else 0.0
    return 0.0


def instruction_fidelity(output: str, task_context: Dict[str, Any]) -> float:
    expected = task_context.get("expected_contains", [])
    forbidden = task_context.get("forbidden_contains", [])
    out = output.lower()
    exp = 1.0 if not expected else sum(1 for t in expected if t.lower() in out) / len(expected)
    forb = 0.0 if not forbidden else sum(1 for t in forbidden if t.lower() in out) / len(forbidden)
    return _clip(exp * (1 - forb))


def structural_validity(output: str, task_context: Dict[str, Any]) -> float:
    req = task_context["format_requirement"]
    if req.startswith("json:"):
        try:
            json.loads(output)
            return 1.0
        except json.JSONDecodeError:
            return 0.0
    if req == "safe_token":
        return 1.0 if output.strip() == "SAFE" and "\n" not in output else 0.0
    if req == "python_expression_only":
        return 1.0 if "\n" not in output else 0.0
    return 1.0


def score_secondary_blind(output: str, task_context: Dict[str, Any]) -> Dict[str, float]:
    payload = {
        "format_compliance": format_compliance(output, task_context),
        "instruction_fidelity": instruction_fidelity(output, task_context),
        "structural_validity": structural_validity(output, task_context),
    }
    payload["secondary_overall"] = _clip(sum(payload.values()) / 3)
    return payload


# Primary metrics (dominant)
def compute_primary_metrics(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    grouped: Dict[tuple, List[Dict[str, Any]]] = defaultdict(list)
    for row in records:
        grouped[(row["model_name"], row["system_type"])].append(row)

    summary: Dict[str, Dict[str, Dict[str, float]]] = defaultdict(dict)

    # pass 1
    for (model, system), rows in grouped.items():
        total = len(rows)
        successful = [r for r in rows if r["success"]]
        success_rate = len(successful) / total if total else 0.0
        avg_attempts = (sum(r["attempts_to_success"] for r in successful) / len(successful)) if successful else 0.0
        total_cost = sum(r["total_cost"] for r in rows)
        cost_per_success = (total_cost / len(successful)) if successful else 0.0
        failure_persistence = (total - len(successful)) / total if total else 0.0

        summary[model][system] = {
            "success_rate": round(success_rate, 4),
            "avg_attempts_to_success": round(avg_attempts, 4),
            "cost_per_success": round(cost_per_success, 8),
            "failure_persistence": round(failure_persistence, 4),
            "total_cost": round(total_cost, 8),
            "runs": total,
        }

    # pass 2: efficiency gain vs baseline
    for model, systems in summary.items():
        baseline_cost = systems.get("baseline", {}).get("cost_per_success", 0.0)
        for system in list(systems.keys()):
            systems[system]["efficiency_gain_vs_baseline"] = round(
                baseline_cost - systems[system]["cost_per_success"], 8
            )

    return {"primary_by_model_system": summary}
