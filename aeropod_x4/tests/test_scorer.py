from aeropod_x4.geometry.parameters import DesignParameters, MissionProfile
from aeropod_x4.optimization.scorer import score_design


def _sample_design() -> DesignParameters:
    return DesignParameters(
        pod_length_mm=110,
        pod_width_mm=52,
        pod_height_mm=35,
        tail_length_mm=40,
        arm_length_mm=75,
        arm_chord_mm=16,
        arm_thickness_mm=4,
        wall_thickness_mm=1.8,
        motor_pad_diameter_mm=16,
        battery_bay_length_mm=65,
        battery_bay_width_mm=30,
        battery_bay_height_mm=20,
    )


def test_score_in_range() -> None:
    result = score_design(_sample_design(), MissionProfile())
    assert 0 <= result["score"] <= 100


def test_metric_signs() -> None:
    result = score_design(_sample_design(), MissionProfile())
    assert result["drag_force_n"] > 0
    assert result["mass_kg"] > 0
    assert result["reynolds_number"] > 0
