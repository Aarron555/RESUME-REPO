# aeropod-x4-optimizer

Python MVP for parametric quadcopter body optimization focused on aerodynamic efficiency, durability, and manufacturability.

## Run (500 variants + hard mass constraint + top-4 3D HTML)

```bash
PYTHONPATH=. python -m aeropod_x4.main
```

This generates in `outputs_500/`:
- `report.json`
- `designs.csv`
- `top_1_design.scad` ... `top_4_design.scad`
- `top4_viewer.html` (browser-ready detailed 3D CAD simulation viewer)

## Edit mission inputs

Update `examples/mission_drone_5inch.json` and pass the path into `run(mission_path=...)`.

## Score meaning

Final score is 0–100 weighted by mission priorities:
- **Drag / Power / Frontal area**: aerodynamic efficiency.
- **Mass**: lighter is better against `target_mass_kg`.
- **Prop blockage**: lower rotor disk blockage is better.
- **Durability**: thicker, less slender structure tends to score higher.
- **Printability**: FDM-friendly wall/height/arm proportions.
- **Repairability**: access-friendly and practical wall thickness.

## Hard constraints

A strict filter is applied: **mass_kg < target_mass_kg** (default target: `0.30 kg`).
Only constrained-feasible designs are ranked.

## Validation path

1. **Smoke test**: confirm report/CSV/SCAD/HTML outputs are generated.
2. **Flight telemetry**: compare predicted drag/power to real current draw and cruise behavior.
3. **CFD screening**: run top 10 in coarse CFD and recalibrate scoring constants.
4. **Next step**: integrate OpenFOAM or SU2 batch validation loop for high-fidelity aero ranking.

## Notes

- SI units are used in physics calculations.
- Input geometry dimensions are in mm and converted to meters where needed.
- OpenSCAD output is intentionally simplified but parametric and STL-exportable.


## HTML CAD simulation

Open `outputs_500/top4_viewer.html` in a browser to inspect designs with:
- orbit/pan/zoom camera controls
- wireframe toggle
- exploded-view toggle
- measurement envelope overlay
- ranked design selector and metric panel
