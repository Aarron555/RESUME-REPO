from __future__ import annotations

from pathlib import Path

from aeropod_x4.geometry.parameters import DesignParameters


def export_best_to_openscad(params: DesignParameters, output_path: str) -> Path:
    """Export a simple parametric OpenSCAD model for the selected best design."""
    scad = f"""
$fn = 64;

pod_len = {params.pod_length_mm};
pod_w = {params.pod_width_mm};
pod_h = {params.pod_height_mm};
tail_len = {params.tail_length_mm};
arm_len = {params.arm_length_mm};
arm_chord = {params.arm_chord_mm};
arm_thick = {params.arm_thickness_mm};
motor_pad_d = {params.motor_pad_diameter_mm};

module rounded_pod() {{
    scale([pod_len/pod_w, 1, pod_h/pod_w]) sphere(d=pod_w);
}}

module tail() {{
    translate([pod_len*0.45,0,0])
    hull() {{
        scale([0.3,0.35,0.35]) sphere(d=pod_w);
        translate([tail_len,0,0]) scale([0.08,0.12,0.12]) sphere(d=pod_w);
    }}
}}

module arm() {{
    hull() {{
        translate([0, -arm_chord/2, -arm_thick/2]) cube([arm_len, arm_chord, arm_thick]);
        translate([arm_len*0.8, -arm_chord*0.35, -arm_thick*0.35]) cube([arm_len*0.2, arm_chord*0.7, arm_thick*0.7]);
    }}
}}

module motor_pad() {{
    cylinder(h=3, d=motor_pad_d, center=true);
}}

module battery_bay() {{
    translate([0,0,0]) cube([{params.battery_bay_length_mm},{params.battery_bay_width_mm},{params.battery_bay_height_mm}], center=true);
}}

module screw_bosses() {{
    for (x=[-10,10], y=[-10,10])
      translate([x,y,-pod_h*0.2]) cylinder(h=8,d=4,center=true);
}}

difference() {{
  union() {{
    rounded_pod();
    tail();

    for (a=[45,135,225,315]) {{
      rotate([0,0,a]) translate([pod_len*0.18,0,0]) arm();
      rotate([0,0,a]) translate([pod_len*0.18 + arm_len,0,0]) motor_pad();
    }}

    screw_bosses();
  }}

  battery_bay();
}}
""".strip()

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(scad + "\n", encoding="utf-8")
    return out
