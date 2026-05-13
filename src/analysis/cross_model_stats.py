from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List

from src.metrics import summarize_hcm_council

STAT_PATH = Path("benchmarks/statistical_summary.json")


def _mean(v: List[float]) -> float:
    return sum(v) / len(v) if v else 0.0


def compute_cross_model_statistics(records: List[Dict[str, Any]], seed: int = 42) -> Dict[str, Any]:
    by_triplet = defaultdict(list)
    for r in records:
        by_triplet[(r["model_name"], r["system_type"], r["task_type"])].append(r["rubric"]["rubric_mean"])

    summary = defaultdict(lambda: defaultdict(dict))
    for (m, s, t), vals in by_triplet.items():
        summary[m][s][t] = {"mean_rubric": round(_mean(vals), 4), "n": len(vals)}

    council = summarize_hcm_council(records)

    payload = {
        "model_system_task_summary": summary,
        "hcm_council": council,
        "pairwise": {
            "hcm_vs_casual_improvement_pct": round(((council["condition_means"]["hcm"] - council["condition_means"]["casual"]) / council["condition_means"]["casual"] * 100), 2),
            "hcm_vs_structured_improvement_pct": round(((council["condition_means"]["hcm"] - council["condition_means"]["structured"]) / council["condition_means"]["structured"] * 100), 2),
        },
    }

    STAT_PATH.parent.mkdir(parents=True, exist_ok=True)
    STAT_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload
