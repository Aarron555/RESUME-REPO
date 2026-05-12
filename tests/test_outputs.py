from src.analysis.cross_model_stats import compute_cross_model_statistics
from src.evaluator import load_experiment_config, run_experiment
from src.metrics import RUBRIC_KEYS


def test_hcm_matrix_and_blind_integrity():
    cfg = load_experiment_config()
    payload = run_experiment(cfg)
    expected = len(cfg["models"]) * len(cfg["systems"]) * len(cfg["tasks"]) * int(cfg["runs_per_task"])
    assert payload["metadata"]["total_records"] == expected
    assert payload["metadata"]["blind_evaluation"] is True


def test_rubric_present_and_complete():
    cfg = load_experiment_config()
    payload = run_experiment(cfg)
    for rec in payload["records"]:
        for key in RUBRIC_KEYS + ["rubric_mean"]:
            assert key in rec["rubric"]


def test_improvement_calculation_and_reproducible():
    cfg = load_experiment_config()
    one = compute_cross_model_statistics(run_experiment(cfg)["records"], seed=int(cfg["seed"]))
    two = compute_cross_model_statistics(run_experiment(cfg)["records"], seed=int(cfg["seed"]))
    assert one == two
    assert "hcm_vs_casual_improvement_pct" in one["pairwise"]
