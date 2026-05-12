from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

REPORT_PATH = Path("results/report.md")


def generate_report(results_payload: Dict[str, Any], stats_payload: Dict[str, Any]) -> str:
    council = stats_payload["hcm_council"]
    table = council["task_comparison"]

    lines: List[str] = [
        "# HCM Evaluation Council Report",
        "",
        "## Condition Means (Rubric)",
        f"- Casual: {council['condition_means']['casual']}",
        f"- Structured: {council['condition_means']['structured']}",
        f"- HCM: {council['condition_means']['hcm']}",
        "",
        "## Task-by-Task Evidence",
        "| Task | Casual | Structured | HCM | HCM vs Casual % | HCM vs Structured % | HCM Helped | Narrow Valid Condition |",
        "|---|---:|---:|---:|---:|---:|---|---|",
    ]
    for task, row in table.items():
        lines.append(
            f"| {task} | {row['casual']:.4f} | {row['structured']:.4f} | {row['hcm']:.4f} | {row['improvement_vs_casual_pct']:.2f}% | {row['improvement_vs_structured_pct']:.2f}% | {row['hcm_helped']} | {row['narrow_valid_condition']} |"
        )

    lines.extend(
        [
            "",
            "## Failures by Category",
            "- format_failure",
            "- instruction_miss",
            "- hallucination_proxy_trigger",
            "- adversarial_breakdown",
            "- structural_violation",
            "",
            "## Final Evidence-backed Conclusion",
            council["final_conclusion"],
        ]
    )

    report = "\n".join(lines)
    REPORT_PATH.write_text(report, encoding="utf-8")
    return report
