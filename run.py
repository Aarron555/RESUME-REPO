from __future__ import annotations

import argparse
import subprocess

from results.report_generator import generate_report
from src.analysis.cross_model_stats import compute_cross_model_statistics
from src.evaluator import load_experiment_config, run_experiment


def main() -> None:
    parser = argparse.ArgumentParser(description="Run HCM Evaluation Council benchmark")
    parser.add_argument("--config", default="config/experiment.yaml")
    parser.add_argument("--dashboard", action="store_true")
    args = parser.parse_args()

    config = load_experiment_config(args.config)
    results_payload = run_experiment(config)
    stats_payload = compute_cross_model_statistics(results_payload["records"], seed=int(config["seed"]))
    report = generate_report(results_payload, stats_payload)

    print(report)
    print("\nImprovement summary:")
    print(stats_payload["pairwise"])

    if args.dashboard:
        subprocess.run(["streamlit", "run", "src/dashboard/app.py"], check=False)


if __name__ == "__main__":
    main()
