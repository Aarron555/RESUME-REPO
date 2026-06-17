from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from aeropod_x4.geometry.openscad_exporter import export_best_to_openscad
from aeropod_x4.geometry.parameters import DesignParameters, MissionProfile
from aeropod_x4.optimization.generator import generate_variants
from aeropod_x4.optimization.ranker import rank_designs
from aeropod_x4.optimization.scorer import score_design
from aeropod_x4.reports.html_generator import write_top4_html
from aeropod_x4.reports.report_writer import write_reports


def load_mission(path: str | None) -> MissionProfile:
    if not path:
        return MissionProfile()
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return MissionProfile(**data)


def default_ranges() -> dict[str, tuple[float, float]]:
    return {
        "pod_length_mm": (80, 140),
        "pod_width_mm": (35, 70),
        "pod_height_mm": (25, 55),
        "tail_length_mm": (20, 65),
        "arm_length_mm": (55, 95),
        "arm_chord_mm": (10, 22),
        "arm_thickness_mm": (2.5, 7.0),
        "wall_thickness_mm": (1.2, 2.8),
        "motor_pad_diameter_mm": (12, 22),
        "battery_bay_length_mm": (45, 85),
        "battery_bay_width_mm": (20, 40),
        "battery_bay_height_mm": (15, 30),
    }


def _compact_table(designs: list[dict]) -> str:
    headers = ("rank", "id", "score", "mass_g", "drag_n", "power_w")
    rows = []
    for idx, d in enumerate(designs, start=1):
        rows.append((idx, d["design_id"], f"{d['score']:.2f}", f"{d['mass_kg'] * 1000:.1f}", f"{d['drag_force_n']:.3f}", f"{d['power_required_w']:.3f}"))
    col_w = [max(len(str(x[i])) for x in ([headers] + rows)) for i in range(len(headers))]
    fmt = " | ".join(f"{{:{w}}}" for w in col_w)
    sep = "-+-".join("-" * w for w in col_w)
    body = [fmt.format(*headers), sep] + [fmt.format(*r) for r in rows]
    return "\n".join(body)


def run(count: int = 500, mission_path: str | None = None, output_dir: str = "outputs") -> None:
    mission = load_mission(mission_path)
    variants = generate_variants(default_ranges(), count=count)

    scored = []
    for i, design in enumerate(variants, start=1):
        metrics = score_design(design, mission)
        scored.append({"design_id": i, **asdict(design), **metrics})

    constrained = [d for d in scored if d["mass_kg"] < mission.target_mass_kg]
    if not constrained:
        raise RuntimeError("No designs satisfy hard mass constraint.")

    top10 = rank_designs(constrained, top_n=10)
    top4 = rank_designs(constrained, top_n=4)

    write_reports(constrained, top10, output_dir=output_dir)

    for idx, design in enumerate(top4, start=1):
        best_params = DesignParameters(
            pod_length_mm=design["pod_length_mm"],
            pod_width_mm=design["pod_width_mm"],
            pod_height_mm=design["pod_height_mm"],
            tail_length_mm=design["tail_length_mm"],
            arm_length_mm=design["arm_length_mm"],
            arm_chord_mm=design["arm_chord_mm"],
            arm_thickness_mm=design["arm_thickness_mm"],
            wall_thickness_mm=design["wall_thickness_mm"],
            motor_pad_diameter_mm=design["motor_pad_diameter_mm"],
            battery_bay_length_mm=design["battery_bay_length_mm"],
            battery_bay_width_mm=design["battery_bay_width_mm"],
            battery_bay_height_mm=design["battery_bay_height_mm"],
        )
        export_best_to_openscad(best_params, f"{output_dir}/top_{idx}_design.scad")

    write_top4_html(top4, f"{output_dir}/top4_viewer.html")
    print(_compact_table(top10))


if __name__ == "__main__":
    run(count=500, mission_path="aeropod_x4/examples/mission_drone_5inch.json", output_dir="outputs_500")
