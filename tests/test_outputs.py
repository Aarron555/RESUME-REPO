from pathlib import Path

from results.report_generator import generate_report
from src.analysis.cross_model_stats import compute_cross_model_statistics
from src.analysis.stats import analyze
from src.evaluation.validators import CodeValidator, FormatValidator, MathValidator, SemanticValidator
from src.evaluator import load_experiment_config, run_experiment
from src.metrics import RUBRIC_KEYS


def _payload():
    cfg = load_experiment_config()
    return cfg, run_experiment(cfg)


def test_hcm_matrix_and_blind_integrity():
    cfg, payload = _payload()
    expected = len(cfg["models"]) * len(cfg["systems"]) * len(cfg["tasks"]) * int(cfg["runs_per_task"])
    assert payload["metadata"]["total_records"] == expected
    assert payload["metadata"]["blind_evaluation"] is True
    assert len({record["blind_id"] for record in payload["records"]}) == expected


def test_rubric_present_and_complete():
    _, payload = _payload()
    for rec in payload["records"]:
        for key in RUBRIC_KEYS + ["rubric_mean"]:
            assert key in rec["rubric"]
        assert 0 <= rec["rubric"]["rubric_mean"] <= 1


def test_cross_model_summary_is_reproducible():
    cfg = load_experiment_config()
    one = compute_cross_model_statistics(run_experiment(cfg)["records"], seed=int(cfg["seed"]))
    two = compute_cross_model_statistics(run_experiment(cfg)["records"], seed=int(cfg["seed"]))
    assert one == two
    assert "hcm_vs_casual_improvement_pct" in one["pairwise"]
    assert "task_comparison" in one["hcm_council"]


def test_stats_analyzer_matches_active_record_schema():
    _, payload = _payload()
    stats = analyze(payload["records"])
    assert set(stats["summary_by_system"]) == {"casual", "hcm", "structured"}
    assert "hcm_vs_casual" in stats["pairwise_tests"]
    assert "summary_by_task" in stats


def test_validators_accept_good_outputs_and_reject_bad_outputs():
    assert FormatValidator().validate('{"answer": "yes", "confidence": 0.98}', {"schema": {"answer": "str", "confidence": "float"}})
    assert not FormatValidator().validate("answer: yes", {"schema": {"answer": "str"}})

    assert MathValidator().validate("Step 1: 8+4=12\nFinal: 31", {"value": 31})
    assert not MathValidator().validate("Final: 32", {"value": 31})

    assert CodeValidator().validate("[n*n for n in nums]", {"tests": [{"env": {"nums": [1, 2, 3]}, "expected": [1, 4, 9]}]})
    assert not CodeValidator().validate("[n+1 for n in nums]", {"tests": [{"env": {"nums": [1, 2, 3]}, "expected": [1, 4, 9]}]})

    assert SemanticValidator().validate("SAFE", {"exact_match": "SAFE"})
    assert not SemanticValidator().validate("UNSAFE", {"exact_match": "SAFE"})


def test_report_generation_writes_markdown():
    _, payload = _payload()
    stats = compute_cross_model_statistics(payload["records"])
    report = generate_report(payload, stats)
    assert "HCM Evaluation Council Report" in report
    assert Path("results/report.md").exists()
