from __future__ import annotations

from typing import Dict

from aeropod_x4.geometry.parameters import DesignParameters, MissionProfile
from aeropod_x4.physics.aero import drag_force, power_required, reynolds_number
from aeropod_x4.physics.estimates import (
    estimate_durability,
    estimate_frontal_area,
    estimate_mass,
    estimate_printability,
    estimate_prop_blockage,
    mm_to_m,
)


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, value))


def score_design(params: DesignParameters, mission: MissionProfile) -> Dict[str, float]:
    frontal_area = estimate_frontal_area(params)
    cd = 0.68
    drag_n = drag_force(mission.air_density_kg_m3, mission.cruise_speed_mps, cd, frontal_area)
    reynolds = reynolds_number(
        mission.air_density_kg_m3,
        mission.cruise_speed_mps,
        mm_to_m(params.pod_length_mm),
        mission.dynamic_viscosity_pa_s,
    )
    power_w = power_required(drag_n, mission.cruise_speed_mps)
    mass_kg = estimate_mass(params)
    blockage = estimate_prop_blockage(params, mission.motor_to_motor_diagonal_mm)
    durability = estimate_durability(params)
    printability = estimate_printability(params)

    repairability = _clamp01(1.0 - (params.pod_height_mm - 30.0) / 50.0) * 0.6 + _clamp01(params.wall_thickness_mm / 2.4) * 0.4

    drag_score = _clamp01(1.0 - drag_n / 3.0)
    mass_score = _clamp01(1.0 - mass_kg / mission.target_mass_kg)
    blockage_score = _clamp01(1.0 - blockage / 0.4)
    power_score = _clamp01(1.0 - power_w / 45.0)
    area_score = _clamp01(1.0 - frontal_area / 0.03)

    weights = mission.score_weights
    weighted_total = (
        weights["drag"] * drag_score
        + weights["mass"] * mass_score
        + weights["durability"] * durability
        + weights["printability"] * printability
        + weights["repairability"] * repairability
        + weights["prop_blockage"] * blockage_score
        + weights["power"] * power_score
        + weights["frontal_area"] * area_score
    )

    total_score = round(100.0 * _clamp01(weighted_total), 2)

    return {
        "score": total_score,
        "drag_force_n": drag_n,
        "reynolds_number": reynolds,
        "power_required_w": power_w,
        "frontal_area_m2": frontal_area,
        "prop_blockage": blockage,
        "mass_kg": mass_kg,
        "durability": durability,
        "printability": printability,
        "repairability": repairability,
    }
