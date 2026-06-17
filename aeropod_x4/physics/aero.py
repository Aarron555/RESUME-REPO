from __future__ import annotations


def drag_force(air_density: float, velocity: float, drag_coefficient: float, frontal_area_m2: float) -> float:
    """Compute drag force (N): Fd = 0.5 * rho * v^2 * Cd * A."""
    return 0.5 * air_density * velocity**2 * drag_coefficient * frontal_area_m2


def reynolds_number(air_density: float, velocity: float, characteristic_length_m: float, dynamic_viscosity: float) -> float:
    """Compute Reynolds number: Re = rho * v * L / mu."""
    return (air_density * velocity * characteristic_length_m) / dynamic_viscosity


def power_required(drag_newtons: float, velocity: float) -> float:
    """Estimate aerodynamic power needed at cruise (W): P = F * v."""
    return drag_newtons * velocity
