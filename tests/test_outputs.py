import math

from src.analysis.cost_model import aggregate_costs, compute_call_cost, load_pricing
from src.analysis.cross_model_stats import compute_cross_model_statistics
from src.core.iteration_runner import run_iteration_loop
from src.evaluation.validators import get_validator
from src.evaluator import load_experiment_config, run_experiment
from src.metrics import compute_primary_metrics


class _AlwaysFailClient:
    def generate(self, prompt: str, config: dict) -> str:
        return "BAD_OUTPUT"


class _AlwaysPassClient:
    def generate(self, prompt: str, config: dict) -> str:
        return "SAFE"


def test_validators_correctness():
    assert get_validator("math").validate("Final: 31", {"value": 31})
    assert get_validator("format").validate('{"answer":"yes","confidence":0.9}', {"schema": {"answer": "str", "confidence": "float"}})
    assert get_validator("semantic").validate("SAFE", {"exact_match": "SAFE"})
    assert get_validator("code").validate("[n*n for n in nums]", {"tests": [{"env": {"nums": [1, 2, 3]}, "expected": [1, 4, 9]}]})


def test_iteration_loop_terminates_at_max_attempts():
    result = run_iteration_loop(
        model_client=_AlwaysFailClient(),
        prompt="TASK",
        validator=get_validator("semantic"),
        expected={"exact_match": "SAFE"},
        generation_config={"seed": 42, "temperature": 0.0},
        max_attempts=3,
    )
    assert result["success"] is False
    assert len(result["attempt_logs"]) == 3


def test_cost_calculation_valid():
    pricing = load_pricing()
    c = compute_call_cost(100, 50, "gpt", pricing)
    assert c > 0

    agg = aggregate_costs([
        {"success": True, "total_cost": 0.01},
        {"success": False, "total_cost": 0.02},
    ])
    assert agg["total_cost"] == 0.03
    assert agg["cost_per_success"] > 0


def test_primary_metrics_bounds_and_cost_positive():
    cfg = load_experiment_config()
    payload = run_experiment(cfg)
    primary = compute_primary_metrics(payload["records"])["primary_by_model_system"]

    for model, systems in primary.items():
        for system, metrics in systems.items():
            assert 0 <= metrics["success_rate"] <= 1
            if metrics["success_rate"] > 0:
                assert metrics["cost_per_success"] > 0


def test_reproducibility_and_stats_functional():
    cfg = load_experiment_config()
    one = run_experiment(cfg)
    two = run_experiment(cfg)
    three = run_experiment(cfg)

    s1 = compute_cross_model_statistics(one["records"], seed=int(cfg["seed"]))
    s2 = compute_cross_model_statistics(two["records"], seed=int(cfg["seed"]))
    s3 = compute_cross_model_statistics(three["records"], seed=int(cfg["seed"]))

    assert s1 == s2 == s3
    for model, pair in s1["pairwise_by_model"].items():
        assert 0 <= pair["axiom_vs_baseline"]["p_value"] <= 1
        assert not math.isnan(pair["axiom_vs_baseline"]["cohens_d"])
