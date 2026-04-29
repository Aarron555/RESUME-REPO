from __future__ import annotations

import argparse
import subprocess
from collections import defaultdict

from results.report_generator import generate_report
from src.analysis.cross_model_stats import compute_cross_model_statistics
from src.evaluator import load_experiment_config, run_experiment
from src.reporting.live_explainer import render_live_readout_v4


def main() -> None:
    parser = argparse.ArgumentParser(description="Run AXE-LAB v4 efficiency + correctness benchmark")
    parser.add_argument("--config", default="config/experiment.yaml")
    parser.add_argument("--dashboard", action="store_true")
    args = parser.parse_args()

    config = load_experiment_config(args.config)
    results_payload = run_experiment(config)
    stats_payload = compute_cross_model_statistics(results_payload["records"], seed=int(config["seed"]))
    report = generate_report(results_payload, stats_payload)

    primary = stats_payload["primary_metrics"]["primary_by_model_system"]
    grouped = defaultdict(list)
    for rec in results_payload["records"]:
        grouped[(rec["model_name"], rec["system_type"], rec["task_type"])].append(rec)

    print(report)
    print("\n==============================")
    print("AXE-LAB LIVE INTERPRETABILITY")
    print("==============================")

    for (model, system, task), rows in sorted(grouped.items()):
        successes = sum(1 for r in rows if r["success"])
        total = len(rows)
        success_rate = successes / total if total else 0.0
        avg_attempts = (sum(r["attempts_to_success"] for r in rows if r["success"]) / successes) if successes else 0.0
        cost_per_success = primary[model][system]["cost_per_success"]
        failure_rate = 1 - success_rate
        failure_union = sorted({tag for r in rows for tag in r.get("failure_tags", [])})

        print(
            render_live_readout_v4(
                model=model,
                system=system,
                task=task,
                success_rate=success_rate,
                avg_attempts=avg_attempts,
                cost_per_success=cost_per_success,
                failure_rate=failure_rate,
                failure_tags=failure_union,
            )
        )
        print()

    if args.dashboard:
        subprocess.run(["streamlit", "run", "src/dashboard/app.py"], check=False)


if __name__ == "__main__":
    main()
