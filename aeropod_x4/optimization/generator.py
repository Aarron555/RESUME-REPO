from __future__ import annotations

import random
from typing import Dict, List, Tuple

from aeropod_x4.geometry.parameters import DesignParameters

RangeMap = Dict[str, Tuple[float, float]]


def generate_variants(parameter_ranges: RangeMap, count: int, seed: int = 42) -> List[DesignParameters]:
    """Generate random design variants from inclusive continuous ranges."""
    if count < 1:
        raise ValueError("count must be >= 1")

    rng = random.Random(seed)
    variants: List[DesignParameters] = []

    required = {
        "pod_length_mm",
        "pod_width_mm",
        "pod_height_mm",
        "tail_length_mm",
        "arm_length_mm",
        "arm_chord_mm",
        "arm_thickness_mm",
        "wall_thickness_mm",
        "motor_pad_diameter_mm",
        "battery_bay_length_mm",
        "battery_bay_width_mm",
        "battery_bay_height_mm",
    }
    missing = required - parameter_ranges.keys()
    if missing:
        raise ValueError(f"Missing parameter ranges: {sorted(missing)}")

    for _ in range(count):
        values = {k: rng.uniform(v[0], v[1]) for k, v in parameter_ranges.items()}
        variants.append(DesignParameters(**values))

    return variants
