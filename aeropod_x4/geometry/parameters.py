from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict


@dataclass(frozen=True)
class DesignParameters:
    """Parametric body description for an X4 drone body."""

    pod_length_mm: float
    pod_width_mm: float
    pod_height_mm: float
    tail_length_mm: float
    arm_length_mm: float
    arm_chord_mm: float
    arm_thickness_mm: float
    wall_thickness_mm: float
    motor_pad_diameter_mm: float
    battery_bay_length_mm: float
    battery_bay_width_mm: float
    battery_bay_height_mm: float


@dataclass(frozen=True)
class MissionProfile:
    """Mission-level objectives and environmental constants."""

    name: str = "default_5inch"
    motor_to_motor_diagonal_mm: float = 225.0
    cruise_speed_mps: float = 15.0
    air_density_kg_m3: float = 1.225
    dynamic_viscosity_pa_s: float = 1.81e-5
    target_mass_kg: float = 0.300
    material: str = "PETG"
    manufacturing_method: str = "FDM"
    score_weights: Dict[str, float] = field(
        default_factory=lambda: {
            "drag": 0.22,
            "mass": 0.18,
            "durability": 0.16,
            "printability": 0.14,
            "repairability": 0.10,
            "prop_blockage": 0.08,
            "power": 0.08,
            "frontal_area": 0.04,
        }
    )
