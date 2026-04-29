"""AXE-LAB v4 report generation with primary efficiency metrics."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

REPORT_PATH = Path("results/report.md")


def _aggregate_system_primary(primary_by_model: Dict[str, Dict[str, Dict[str, float]]]) -> Dict[str, Dict[str, float]]:
    systems = {"baseline": [], "structured": [], "axiom": []}
    for model, system_map in primary_by_model.items():
        for system, metrics in system_map.items():
            systems[system].append(metrics)

    agg = {}
    for system, rows in systems.items():
        if not rows:
            agg[system] = {"success_rate": 0.0, "cost_per_success": 0.0, "avg_attempts_to_success": 0.0}
            continue
        agg[system] = {
            "success_rate": sum(r["success_rate"] for r in rows) / len(rows),
            "cost_per_success": sum(r["cost_per_success"] for r in rows) / len(rows),
            "avg_attempts_to_success": sum(r["avg_attempts_to_success"] for r in rows) / len(rows),
        }
    return agg


def _axiom_status(stats_payload: Dict[str, Any]) -> str:
    pairwise = stats_payload["pairwise_by_model"]
    pass_count = 0
    partial_count = 0

    for model, pair in pairwise.items():
        ab = pair["axiom_vs_baseline"]
        ast = pair["axiom_vs_structured"]
        pass_model = (
            ab["success_delta"] > 0
            and ab["cost_delta"] > 0
            and ab["p_value"] <= 0.05
            and ast["success_delta"] >= 0
            and ast["cost_delta"] >= 0
        )
        partial_model = (
            (ab["success_delta"] > 0 or ab["cost_delta"] > 0)
            or (ast["success_delta"] > 0 or ast["cost_delta"] > 0)
        )
        if pass_model:
            pass_count += 1
        elif partial_model:
            partial_count += 1

    if pass_count == len(pairwise):
        return "PASS"
    if pass_count + partial_count > 0:
        return "PARTIAL"
    return "FAIL"


def generate_report(results_payload: Dict[str, Any], stats_payload: Dict[str, Any]) -> str:
    primary = stats_payload["primary_metrics"]["primary_by_model_system"]
    aggregated = _aggregate_system_primary(primary)
    ranking = sorted(
        aggregated.items(),
        key=lambda x: (-x[1]["success_rate"], x[1]["cost_per_success"], x[1]["avg_attempts_to_success"]),
    )

    lines: List[str] = [
        "# AXE-LAB v4 Benchmark Report",
        "",
        "## Efficiency Ranking (Primary Metrics)",
        "| Rank | System | Success Rate | Cost/Success | Avg Attempts |",
        "|---:|---|---:|---:|---:|",
    ]
    for idx, (system, m) in enumerate(ranking, start=1):
        lines.append(
            f"| {idx} | {system} | {m['success_rate']:.4f} | ${m['cost_per_success']:.8f} | {m['avg_attempts_to_success']:.4f} |"
        )

    lines.extend([
        "",
        "## Cost Comparison by Model × System",
        "| Model | System | Success Rate | Failure Persistence | Cost/Success | Efficiency Gain vs Baseline |",
        "|---|---|---:|---:|---:|---:|",
    ])

    for model, system_map in primary.items():
        for system in ["baseline", "structured", "axiom"]:
            m = system_map[system]
            lines.append(
                f"| {model} | {system} | {m['success_rate']:.4f} | {m['failure_persistence']:.4f} | ${m['cost_per_success']:.8f} | {m['efficiency_gain_vs_baseline']:.8f} |"
            )

    lines.extend(["", "## Retry Reduction Comparison", "| Model | Baseline Attempts | Structured Attempts | AXIOM Attempts |", "|---|---:|---:|---:|"])
    for model, system_map in primary.items():
        lines.append(
            f"| {model} | {system_map['baseline']['avg_attempts_to_success']:.4f} | {system_map['structured']['avg_attempts_to_success']:.4f} | {system_map['axiom']['avg_attempts_to_success']:.4f} |"
        )

    lines.append("\n## Statistical Conclusions")
    for model, pair in stats_payload["pairwise_by_model"].items():
        lines.append(
            f"- {model}: AXIOM vs BASELINE (Δsuccess={pair['axiom_vs_baseline']['success_delta']}, Δcost={pair['axiom_vs_baseline']['cost_delta']}, p={pair['axiom_vs_baseline']['p_value']}, d={pair['axiom_vs_baseline']['cohens_d']}); "
            f"AXIOM vs STRUCTURED (Δsuccess={pair['axiom_vs_structured']['success_delta']}, Δcost={pair['axiom_vs_structured']['cost_delta']}, p={pair['axiom_vs_structured']['p_value']}, d={pair['axiom_vs_structured']['cohens_d']})"
        )

    axiom_status = _axiom_status(stats_payload)
    lines.extend(["", f"## AXIOM_STATUS: **{axiom_status}**", ""])

    report = "\n".join(lines)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(report, encoding="utf-8")
    return report
