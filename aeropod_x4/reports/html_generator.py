from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def write_top4_html(top_four: list[dict[str, Any]], output_path: str) -> Path:
    """Create a browser-runnable, detailed 3D CAD-style viewer for top designs."""
    payload = json.dumps(top_four)
    html = f"""<!doctype html>
<html lang='en'>
<head>
  <meta charset='utf-8' />
  <meta name='viewport' content='width=device-width, initial-scale=1' />
  <title>Aeropod X4 Native CAD Viewer</title>
  <style>
    :root {{ --bg: #0b1220; --panel: #111827; --line: #334155; --txt: #dbeafe; --muted: #94a3b8; --accent: #60a5fa; }}
    body {{ margin: 0; background: var(--bg); color: var(--txt); font-family: Inter, Segoe UI, Arial, sans-serif; }}
    .layout {{ display: grid; grid-template-columns: 320px 1fr; height: 100vh; }}
    .sidebar {{ border-right: 1px solid var(--line); background: #0f172a; padding: 14px; overflow: auto; }}
    .main {{ position: relative; }}
    .toolbar {{ display: flex; gap: 8px; margin-bottom: 12px; flex-wrap: wrap; }}
    button, select, input {{ background: #111827; color: var(--txt); border: 1px solid var(--line); border-radius: 8px; padding: 7px 10px; }}
    button:hover {{ border-color: var(--accent); cursor: pointer; }}
    .meta {{ border: 1px solid var(--line); border-radius: 10px; background: var(--panel); padding: 10px; margin-bottom: 8px; font-size: 12px; }}
    .stat {{ display: grid; grid-template-columns: 1fr auto; color: var(--muted); gap: 8px; }}
    #renderZone {{ position: absolute; inset: 0; }}
    .hint {{ position: absolute; right: 12px; bottom: 12px; font-size: 12px; color: #cbd5e1; background: rgba(17,24,39,.8); border: 1px solid var(--line); border-radius: 8px; padding: 8px; }}
  </style>
</head>
<body>
<div class='layout'>
  <aside class='sidebar'>
    <h2 style='margin:0 0 8px 0'>Aeropod X4 CAD Viewer</h2>
    <p style='margin:0 0 12px 0;color:var(--muted);font-size:13px'>Native browser 3D inspection of top designs.</p>

    <div class='toolbar'>
      <select id='designSelect'></select>
      <button id='fitBtn'>Fit View</button>
      <button id='wireBtn'>Wireframe</button>
      <button id='measureBtn'>Measure</button>
      <button id='explodeBtn'>Explode</button>
    </div>

    <div class='meta'>
      <div class='stat'><span>Score</span><strong id='score'></strong></div>
      <div class='stat'><span>Mass</span><strong id='mass'></strong></div>
      <div class='stat'><span>Drag</span><strong id='drag'></strong></div>
      <div class='stat'><span>Power</span><strong id='power'></strong></div>
      <div class='stat'><span>Reynolds</span><strong id='reynolds'></strong></div>
      <div class='stat'><span>Blockage</span><strong id='blockage'></strong></div>
    </div>

    <div class='meta'>
      <div class='stat'><span>Pod L × W × H</span><strong id='podDims'></strong></div>
      <div class='stat'><span>Tail Length</span><strong id='tailLen'></strong></div>
      <div class='stat'><span>Arm L / Chord / Thick</span><strong id='armDims'></strong></div>
      <div class='stat'><span>Motor Pad Ø</span><strong id='motorPad'></strong></div>
      <div class='stat'><span>Battery Bay</span><strong id='bayDims'></strong></div>
    </div>
  </aside>

  <main class='main'>
    <canvas id='renderZone'></canvas>
    <div class='hint'>Drag=orbit • Right-drag=pan • Wheel=zoom</div>
  </main>
</div>

<script type='module'>
import * as THREE from 'https://unpkg.com/three@0.164.1/build/three.module.js';
import {{ OrbitControls }} from 'https://unpkg.com/three@0.164.1/examples/jsm/controls/OrbitControls.js';

const designs = {payload};
const canvas = document.getElementById('renderZone');
const renderer = new THREE.WebGLRenderer({{ canvas, antialias: true }});
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.outputColorSpace = THREE.SRGBColorSpace;

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0b1220);

const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 10000);
camera.position.set(260, 190, 260);

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.06;

scene.add(new THREE.HemisphereLight(0xffffff, 0x101820, 1.0));
const key = new THREE.DirectionalLight(0xffffff, 1.1); key.position.set(280, 300, 130); scene.add(key);
const rim = new THREE.DirectionalLight(0x9dc1ff, 0.55); rim.position.set(-180, 130, -240); scene.add(rim);

const grid = new THREE.GridHelper(900, 45, 0x334155, 0x1e293b);
scene.add(grid);

let currentGroup = null;
let wireMode = false;
let measureMode = false;
let explodeMode = false;
let measureHelpers = [];

function roundedPod(d, material) {{
  const mesh = new THREE.Mesh(new THREE.SphereGeometry(1, 64, 32), material);
  mesh.scale.set(d.pod_length_mm / d.pod_width_mm, 1, d.pod_height_mm / d.pod_width_mm);
  return mesh;
}}

function taperedTail(d, material) {{
  const g = new THREE.Group();
  const cone = new THREE.Mesh(new THREE.ConeGeometry(d.pod_width_mm*0.18, d.tail_length_mm, 50), material);
  cone.rotation.z = -Math.PI / 2;
  cone.position.x = d.pod_length_mm * 0.66;
  g.add(cone);
  return g;
}}

function armAssembly(d, material, padMat) {{
  const g = new THREE.Group();
  for (let i=0; i<4; i++) {{
    const a = i * Math.PI / 2 + Math.PI / 4;
    const arm = new THREE.Mesh(new THREE.BoxGeometry(d.arm_length_mm, d.arm_thickness_mm, d.arm_chord_mm), material);
    arm.position.set(Math.cos(a)*(d.arm_length_mm*0.57), 0, Math.sin(a)*(d.arm_length_mm*0.57));
    arm.rotation.y = -a;
    arm.userData.partType = 'arm';
    g.add(arm);

    const pod = new THREE.Mesh(new THREE.CylinderGeometry(d.motor_pad_diameter_mm*0.5, d.motor_pad_diameter_mm*0.5, 3.2, 32), padMat);
    pod.rotation.x = Math.PI/2;
    pod.position.set(Math.cos(a)*(d.arm_length_mm*1.08), 0, Math.sin(a)*(d.arm_length_mm*1.08));
    pod.userData.partType = 'motor_pad';
    g.add(pod);
  }}
  return g;
}}

function batteryBay(d, mat) {{
  const bay = new THREE.Mesh(new THREE.BoxGeometry(d.battery_bay_length_mm, d.battery_bay_height_mm, d.battery_bay_width_mm), mat);
  bay.position.y = -d.pod_height_mm * 0.12;
  bay.userData.partType = 'battery_bay';
  return bay;
}}

function buildDrone(d) {{
  const bodyMat = new THREE.MeshStandardMaterial({{ color: 0x60a5fa, metalness: 0.08, roughness: 0.42 }});
  const padMat = new THREE.MeshStandardMaterial({{ color: 0x1e293b, roughness: 0.62 }});
  const bayMat = new THREE.MeshStandardMaterial({{ color: 0x111827, transparent: true, opacity: 0.8 }});

  const g = new THREE.Group();
  g.add(roundedPod(d, bodyMat));
  g.add(taperedTail(d, bodyMat));
  g.add(armAssembly(d, bodyMat, padMat));
  g.add(batteryBay(d, bayMat));
  return g;
}}

function clearMeasure() {{
  measureHelpers.forEach(h => scene.remove(h));
  measureHelpers = [];
}}

function addMeasureBox(group) {{
  clearMeasure();
  const box = new THREE.Box3().setFromObject(group);
  const size = new THREE.Vector3(); box.getSize(size);
  const helper = new THREE.Box3Helper(box, 0xf59e0b);
  scene.add(helper); measureHelpers.push(helper);

  const geo = new THREE.BufferGeometry().setFromPoints([
    new THREE.Vector3(box.min.x, box.max.y + 8, box.min.z),
    new THREE.Vector3(box.max.x, box.max.y + 8, box.min.z),
  ]);
  const line = new THREE.Line(geo, new THREE.LineBasicMaterial({{ color: 0xf59e0b }}));
  scene.add(line); measureHelpers.push(line);
  console.log('Envelope (mm):', size.x.toFixed(1), size.y.toFixed(1), size.z.toFixed(1));
}}

function applyWireframe(group, value) {{
  group.traverse(obj => {{
    if (obj.isMesh && obj.material) obj.material.wireframe = value;
  }});
}}

function applyExplode(group, on) {{
  group.traverse(obj => {{
    if (!obj.isMesh) return;
    const p = obj.userData.partType;
    if (p === 'arm' || p === 'motor_pad') {{
      const dir = obj.position.clone().normalize();
      const mag = on ? 14 : 0;
      obj.position.addScaledVector(dir, mag);
    }}
    if (p === 'battery_bay') obj.position.y = on ? obj.position.y - 12 : obj.position.y + 12;
  }});
}}

function fitToObject(obj) {{
  const box = new THREE.Box3().setFromObject(obj);
  const size = box.getSize(new THREE.Vector3());
  const center = box.getCenter(new THREE.Vector3());
  const maxDim = Math.max(size.x, size.y, size.z);
  const dist = maxDim / (2 * Math.tan((camera.fov * Math.PI / 180) / 2)) * 1.8;
  camera.position.set(center.x + dist, center.y + dist * 0.7, center.z + dist);
  camera.near = Math.max(0.1, dist / 100);
  camera.far = dist * 20;
  camera.updateProjectionMatrix();
  controls.target.copy(center);
  controls.update();
}}

function setMeta(d) {{
  const set = (id, v) => document.getElementById(id).textContent = v;
  set('score', d.score.toFixed(2));
  set('mass', `${{(d.mass_kg*1000).toFixed(1)}} g`);
  set('drag', `${{d.drag_force_n.toFixed(3)}} N`);
  set('power', `${{d.power_required_w.toFixed(3)}} W`);
  set('reynolds', d.reynolds_number.toFixed(0));
  set('blockage', `${{(d.prop_blockage*100).toFixed(2)}} %`);
  set('podDims', `${{d.pod_length_mm.toFixed(1)}} × ${{d.pod_width_mm.toFixed(1)}} × ${{d.pod_height_mm.toFixed(1)}} mm`);
  set('tailLen', `${{d.tail_length_mm.toFixed(1)}} mm`);
  set('armDims', `${{d.arm_length_mm.toFixed(1)}} / ${{d.arm_chord_mm.toFixed(1)}} / ${{d.arm_thickness_mm.toFixed(1)}} mm`);
  set('motorPad', `${{d.motor_pad_diameter_mm.toFixed(1)}} mm`);
  set('bayDims', `${{d.battery_bay_length_mm.toFixed(1)}} × ${{d.battery_bay_width_mm.toFixed(1)}} × ${{d.battery_bay_height_mm.toFixed(1)}} mm`);
}}

function loadDesign(index) {{
  if (currentGroup) scene.remove(currentGroup);
  currentGroup = buildDrone(designs[index]);
  scene.add(currentGroup);
  applyWireframe(currentGroup, wireMode);
  if (explodeMode) applyExplode(currentGroup, true);
  if (measureMode) addMeasureBox(currentGroup); else clearMeasure();
  fitToObject(currentGroup);
  setMeta(designs[index]);
}}

const select = document.getElementById('designSelect');
designs.forEach((d, i) => {{
  const o = document.createElement('option');
  o.value = String(i);
  o.textContent = `Rank ${{i+1}} · Score ${{d.score.toFixed(2)}}`;
  select.appendChild(o);
}});
select.addEventListener('change', () => loadDesign(Number(select.value)));

document.getElementById('fitBtn').addEventListener('click', () => currentGroup && fitToObject(currentGroup));
document.getElementById('wireBtn').addEventListener('click', () => {{
  wireMode = !wireMode; if (currentGroup) applyWireframe(currentGroup, wireMode);
}});
document.getElementById('measureBtn').addEventListener('click', () => {{
  measureMode = !measureMode; if (!currentGroup) return;
  if (measureMode) addMeasureBox(currentGroup); else clearMeasure();
}});
document.getElementById('explodeBtn').addEventListener('click', () => {{
  explodeMode = !explodeMode; if (currentGroup) loadDesign(Number(select.value));
}});

function resize() {{
  const w = canvas.clientWidth || window.innerWidth;
  const h = canvas.clientHeight || window.innerHeight;
  renderer.setSize(w, h, false);
  camera.aspect = w / h;
  camera.updateProjectionMatrix();
}}
window.addEventListener('resize', resize);
resize();
loadDesign(0);

function animate() {{
  requestAnimationFrame(animate);
  controls.update();
  renderer.render(scene, camera);
}}
animate();
</script>
</body>
</html>"""

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    return out
