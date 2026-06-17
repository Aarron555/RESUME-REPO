from __future__ import annotations

import math

from aeropod_x4.geometry.parameters import DesignParameters

PETG_DENSITY_KG_M3 = 1270.0


def mm_to_m(value_mm: float) -> float:
    return value_mm / 1000.0


def estimate_frontal_area(params: DesignParameters) -> float:
    """Approximate frontal area in m^2 using an ellipse + arm contribution."""
    pod_w = mm_to_m(params.pod_width_mm)
    pod_h = mm_to_m(params.pod_height_mm)
    pod_area = math.pi * (pod_w * 0.5) * (pod_h * 0.5)

    arm_area = 4.0 * mm_to_m(params.arm_chord_mm) * mm_to_m(params.arm_thickness_mm) * 0.55
    return pod_area + arm_area


def estimate_prop_blockage(params: DesignParameters, motor_to_motor_diagonal_mm: float) -> float:
    """Fraction [0,1] of rotor disk area blocked by central body + arm roots."""
    rotor_diameter_m = 0.127  # 5-inch nominal prop
    single_rotor_area = math.pi * (rotor_diameter_m * 0.5) ** 2
    total_rotor_area = 4.0 * single_rotor_area

    body_shadow = estimate_frontal_area(params)
    spacing_factor = min(1.0, max(0.5, motor_to_motor_diagonal_mm / 225.0))
    blocked = (body_shadow * 0.35 / spacing_factor) / total_rotor_area
    return max(0.0, min(0.6, blocked))


def estimate_mass(params: DesignParameters, material_density_kg_m3: float = PETG_DENSITY_KG_M3) -> float:
    """Approximate shell/body mass in kg."""
    t = mm_to_m(params.wall_thickness_mm)

    pod_surface = 2.0 * (
        mm_to_m(params.pod_length_mm) * mm_to_m(params.pod_width_mm)
        + mm_to_m(params.pod_length_mm) * mm_to_m(params.pod_height_mm)
        + mm_to_m(params.pod_width_mm) * mm_to_m(params.pod_height_mm)
    )
    pod_shell_volume = pod_surface * t * 0.82

    arm_volume = 4.0 * mm_to_m(params.arm_length_mm) * mm_to_m(params.arm_chord_mm) * mm_to_m(params.arm_thickness_mm)

    tail_volume = 0.5 * mm_to_m(params.tail_length_mm) * mm_to_m(params.pod_width_mm) * mm_to_m(params.pod_height_mm) * 0.25

    motor_pad_volume = 4.0 * math.pi * (mm_to_m(params.motor_pad_diameter_mm) * 0.5) ** 2 * t

    gross_volume = pod_shell_volume + arm_volume + tail_volume + motor_pad_volume

    battery_bay_void = (
        mm_to_m(params.battery_bay_length_mm)
        * mm_to_m(params.battery_bay_width_mm)
        * mm_to_m(params.battery_bay_height_mm)
    ) * 0.55

    effective_volume = max(0.0, gross_volume - battery_bay_void)
    return effective_volume * material_density_kg_m3


def estimate_durability(params: DesignParameters) -> float:
    """Heuristic durability score in [0,1]."""
    t = params.wall_thickness_mm
    arm_t = params.arm_thickness_mm
    ratio = params.arm_chord_mm / max(params.arm_thickness_mm, 1e-6)

    thickness_score = min(1.0, max(0.0, (t - 1.1) / 1.6))
    arm_score = min(1.0, max(0.0, (arm_t - 3.0) / 4.0))
    slender_penalty = min(1.0, max(0.0, (ratio - 3.0) / 5.0))

    return max(0.0, min(1.0, 0.45 * thickness_score + 0.45 * arm_score + 0.10 * (1 - slender_penalty)))


def estimate_printability(params: DesignParameters) -> float:
    """Heuristic printability score in [0,1]."""
    t = params.wall_thickness_mm
    pod_h = params.pod_height_mm
    arm_t = params.arm_thickness_mm

    wall_score = max(0.0, min(1.0, 1.0 - abs(t - 1.8) / 1.4))
    height_score = max(0.0, min(1.0, 1.0 - max(0.0, pod_h - 55.0) / 35.0))
    arm_score = max(0.0, min(1.0, (arm_t - 2.2) / 2.8))

    return max(0.0, min(1.0, 0.4 * wall_score + 0.35 * height_score + 0.25 * arm_score))
