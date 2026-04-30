import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js";
import { OrbitControls } from "https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/controls/OrbitControls.js";

const canvas = document.getElementById("scene");
const statusEl = document.getElementById("status");
const timeRange = document.getElementById("timeRange");
const timeLabel = document.getElementById("timeLabel");
const distanceLabel = document.getElementById("distanceLabel");
const resetViewBtn = document.getElementById("resetView");
const toggleOrbitsBtn = document.getElementById("toggleOrbits");
const toggleLabelsBtn = document.getElementById("toggleLabels");

const AU_TO_SCENE = 35;
const EARTH_RADIUS = 0.7;
const MOON_RADIUS = 0.19;
const MARS_RADIUS = 0.37;
const SUN_RADIUS = 2.2;
const DEG = Math.PI / 180;

const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const isLowPowerDevice = (navigator.hardwareConcurrency || 8) <= 4;
const STAR_COUNT = isLowPowerDevice ? 5500 : 12000;
const PLANET_SEGMENTS = isLowPowerDevice ? 32 : 48;

const state = {
  showOrbits: true,
  showLabels: true,
  catalog: null,
  baseDate: new Date("2025-01-01T00:00:00Z"),
  currentDate: new Date(),
  frameCount: 0,
};

const tmpV1 = new THREE.Vector3();
const tmpV2 = new THREE.Vector3();

const scene = new THREE.Scene();
scene.fog = new THREE.FogExp2(0x02040a, 0.0014);

const renderer = new THREE.WebGLRenderer({
  canvas,
  antialias: true,
  alpha: false,
  powerPreference: "high-performance",
});
renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.5));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.outputColorSpace = THREE.SRGBColorSpace;

const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.1, 3000);
camera.position.set(0, 42, 92);

const controls = new OrbitControls(camera, canvas);
controls.enableDamping = true;
controls.dampingFactor = 0.06;
controls.minDistance = 6;
controls.maxDistance = 1200;
controls.target.set(0, 0, 0);

scene.add(new THREE.AmbientLight(0xffffff, 0.2));
const sunLight = new THREE.PointLight(0xfff1bf, 240, 0, 1.7);
scene.add(sunLight);

const textureLoader = new THREE.TextureLoader();
textureLoader.setCrossOrigin("anonymous");

const bodies = {
  sun: createSun(),
  earth: createPlanet(EARTH_RADIUS),
  moon: createPlanet(MOON_RADIUS),
  mars: createPlanet(MARS_RADIUS),
};
bodies.sun.name = "sun";
bodies.earth.name = "earth";
bodies.moon.name = "moon";
bodies.mars.name = "mars";

const clouds = createClouds(EARTH_RADIUS * 1.01);
bodies.earth.add(clouds);

const earthAtmosphere = createAtmosphereShell(EARTH_RADIUS * 1.03);

const starField = createStarField(STAR_COUNT);
scene.add(starField);

const orbitalGroup = new THREE.Group();
scene.add(orbitalGroup);

const bodyGroup = new THREE.Group();
bodyGroup.add(bodies.sun, bodies.earth, bodies.moon, bodies.mars, earthAtmosphere);
scene.add(bodyGroup);

const orbitLines = [];
const labels = {
  sun: createLabel("sun"),
  earth: createLabel("earth"),
  moon: createLabel("moon"),
  mars: createLabel("mars"),
};

buildOrbit("earth", 1.0, 0x3b66ff);
buildOrbit("mars", 1.523679, 0xd07347);

const raycaster = new THREE.Raycaster();
const pointer = new THREE.Vector2();
const pickables = [bodies.sun, bodies.earth, bodies.moon, bodies.mars];
let hovered = null;
let running = true;

canvas.addEventListener("pointermove", onPointerMove, { passive: true });
canvas.addEventListener("click", onPointerClick);
document.addEventListener("visibilitychange", onVisibilityChange);

const ELEMENTS = {
  earth: {
    a: 1.00000011,
    e: 0.01671022,
    i: 0.00005,
    omega: -11.26064,
    Omega: -11.26064,
    L0: 100.46435,
    periodDays: 365.256,
  },
  mars: {
    a: 1.52366231,
    e: 0.09341233,
    i: 1.85061,
    omega: 286.537,
    Omega: 49.57854,
    L0: 355.45332,
    periodDays: 686.98,
  },
  moon: {
    a: 0.00257,
    e: 0.0549,
    i: 5.145,
    omega: 318.15,
    Omega: 125.08,
    L0: 115.3654,
    periodDays: 27.321661,
  },
};

const TEXTURE_URLS = {
  sun: "https://raw.githubusercontent.com/mrdoob/three.js/dev/examples/textures/planets/sun.jpg",
  earth: "https://raw.githubusercontent.com/mrdoob/three.js/dev/examples/textures/planets/earth_atmos_2048.jpg",
  earthNormal: "https://raw.githubusercontent.com/mrdoob/three.js/dev/examples/textures/planets/earth_normal_2048.jpg",
  moon: "https://raw.githubusercontent.com/mrdoob/three.js/dev/examples/textures/planets/moon_1024.jpg",
  mars: "https://raw.githubusercontent.com/mrdoob/three.js/dev/examples/textures/planets/mars_1k_color.jpg",
};

await init();
animate();

async function init() {
  try {
    const [catalogRes, ephemerisRes] = await Promise.allSettled([fetch("/api/catalog"), fetch("/api/ephemeris")]);

    if (catalogRes.status === "fulfilled") {
      state.catalog = await catalogRes.value.json();
    }
    if (ephemerisRes.status === "fulfilled") {
      updateEphemeris(await ephemerisRes.value.json());
    }

    await applyRealisticTextures();

    statusEl.textContent = state.catalog?.system_name || "ready";
  } catch (err) {
    console.error(err);
    statusEl.textContent = "offline demo";
  }

  updateFromRange(Number(timeRange.value));

  timeRange.addEventListener("input", () => updateFromRange(Number(timeRange.value)));

  resetViewBtn.addEventListener("click", () => {
    controls.target.set(0, 0, 0);
    camera.position.set(0, 42, 92);
    controls.update();
  });

  toggleOrbitsBtn.addEventListener("click", () => {
    state.showOrbits = !state.showOrbits;
    orbitLines.forEach((line) => (line.visible = state.showOrbits));
    toggleOrbitsBtn.textContent = state.showOrbits ? "Hide Orbits" : "Show Orbits";
  });

  toggleLabelsBtn.addEventListener("click", () => {
    state.showLabels = !state.showLabels;
    toggleLabelsBtn.textContent = state.showLabels ? "Hide Labels" : "Show Labels";
  });
}

function createSun() {
  const mesh = new THREE.Mesh(
    new THREE.SphereGeometry(SUN_RADIUS, PLANET_SEGMENTS, PLANET_SEGMENTS),
    new THREE.MeshBasicMaterial({ color: 0xffcc66 }),
  );
  const glow = new THREE.Mesh(
    new THREE.SphereGeometry(SUN_RADIUS * 1.18, 36, 36),
    new THREE.MeshBasicMaterial({ color: 0xffb54d, transparent: true, opacity: 0.18 }),
  );
  mesh.add(glow);
  return mesh;
}

function createPlanet(radius) {
  return new THREE.Mesh(
    new THREE.SphereGeometry(radius, PLANET_SEGMENTS, PLANET_SEGMENTS),
    new THREE.MeshStandardMaterial({ color: 0x8c8c8c, roughness: 0.95, metalness: 0.0 }),
  );
}

function createClouds(radius) {
  return new THREE.Mesh(
    new THREE.SphereGeometry(radius, PLANET_SEGMENTS, PLANET_SEGMENTS),
    new THREE.MeshStandardMaterial({
      color: 0xffffff,
      transparent: true,
      opacity: 0.12,
      roughness: 1,
      metalness: 0,
      depthWrite: false,
    }),
  );
}

function createAtmosphereShell(radius) {
  return new THREE.Mesh(
    new THREE.SphereGeometry(radius, PLANET_SEGMENTS, PLANET_SEGMENTS),
    new THREE.ShaderMaterial({
      transparent: true,
      depthWrite: false,
      blending: THREE.AdditiveBlending,
      side: THREE.BackSide,
      uniforms: {
        glowColor: { value: new THREE.Color(0x5ea8ff) },
        intensity: { value: 1.2 },
      },
      vertexShader: `varying vec3 vNormal; void main(){ vNormal = normalize(normalMatrix * normal); gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }`,
      fragmentShader: `varying vec3 vNormal; uniform vec3 glowColor; uniform float intensity; void main(){ float a = pow(0.65 - dot(vNormal, vec3(0.0,0.0,1.0)),2.2); gl_FragColor = vec4(glowColor * intensity, a * 0.42); }`,
    }),
  );
}

function createLabel(text) {
  const div = document.createElement("div");
  div.textContent = text;
  div.style.position = "absolute";
  div.style.transform = "translate(-50%, -50%)";
  div.style.padding = "4px 8px";
  div.style.borderRadius = "999px";
  div.style.background = "rgba(0,0,0,0.45)";
  div.style.border = "1px solid rgba(255,255,255,0.12)";
  div.style.color = "white";
  div.style.fontSize = "12px";
  div.style.pointerEvents = "none";
  document.body.appendChild(div);
  return div;
}

function createStarField(count) {
  const geom = new THREE.BufferGeometry();
  const positions = new Float32Array(count * 3);
  const colors = new Float32Array(count * 3);
  const scales = new Float32Array(count);

  for (let i = 0; i < count; i += 1) {
    const r = 1200 + Math.random() * 800;
    const theta = Math.random() * Math.PI * 2;
    const phi = Math.acos(2 * Math.random() - 1);

    positions[i * 3 + 0] = r * Math.sin(phi) * Math.cos(theta);
    positions[i * 3 + 1] = r * Math.cos(phi);
    positions[i * 3 + 2] = r * Math.sin(phi) * Math.sin(theta);

    const temp = Math.random();
    if (temp > 0.9) {
      colors[i * 3 + 0] = 0.70;
      colors[i * 3 + 1] = 0.79;
      colors[i * 3 + 2] = 1.0;
    } else if (temp < 0.08) {
      colors[i * 3 + 0] = 1.0;
      colors[i * 3 + 1] = 0.86;
      colors[i * 3 + 2] = 0.75;
    } else {
      const tint = 0.86 + Math.random() * 0.14;
      colors[i * 3 + 0] = tint;
      colors[i * 3 + 1] = tint;
      colors[i * 3 + 2] = tint;
    }
    scales[i] = Math.random();
  }

  geom.setAttribute("position", new THREE.BufferAttribute(positions, 3));
  geom.setAttribute("color", new THREE.BufferAttribute(colors, 3));
  geom.setAttribute("scale", new THREE.BufferAttribute(scales, 1));

  const mat = new THREE.PointsMaterial({
    size: isLowPowerDevice ? 1.1 : 1.45,
    sizeAttenuation: true,
    vertexColors: true,
    transparent: true,
    opacity: 0.95,
  });

  return new THREE.Points(geom, mat);
}

function buildOrbit(name, semiMajorAU, color) {
  const segments = isLowPowerDevice ? 180 : 300;
  const points = [];
  for (let i = 0; i <= segments; i += 1) {
    const t = (i / segments) * Math.PI * 2;
    points.push(new THREE.Vector3(Math.cos(t) * semiMajorAU * AU_TO_SCENE, 0, Math.sin(t) * semiMajorAU * AU_TO_SCENE));
  }
  const line = new THREE.Line(
    new THREE.BufferGeometry().setFromPoints(points),
    new THREE.LineBasicMaterial({ color, transparent: true, opacity: 0.34 }),
  );
  line.userData.body = name;
  orbitalGroup.add(line);
  orbitLines.push(line);
}

async function applyRealisticTextures() {
  const [sunMap, earthMap, earthNormal, moonMap, marsMap] = await Promise.all([
    loadTexture(TEXTURE_URLS.sun),
    loadTexture(TEXTURE_URLS.earth),
    loadTexture(TEXTURE_URLS.earthNormal),
    loadTexture(TEXTURE_URLS.moon),
    loadTexture(TEXTURE_URLS.mars),
  ]);

  if (sunMap) {
    bodies.sun.material.map = sunMap;
    bodies.sun.material.needsUpdate = true;
  }

  if (earthMap) {
    bodies.earth.material.map = earthMap;
    bodies.earth.material.color.setHex(0xffffff);
  } else {
    bodies.earth.material.map = makeFallbackEarthTexture();
  }

  if (earthNormal) {
    bodies.earth.material.normalMap = earthNormal;
    bodies.earth.material.normalScale = new THREE.Vector2(0.7, 0.7);
  }

  if (moonMap) {
    bodies.moon.material.map = moonMap;
    bodies.moon.material.color.setHex(0xffffff);
  } else {
    bodies.moon.material.color.setHex(0xb8b8b8);
  }

  if (marsMap) {
    bodies.mars.material.map = marsMap;
    bodies.mars.material.color.setHex(0xffffff);
  } else {
    bodies.mars.material.color.setHex(0xcf7a4d);
  }

  for (const body of [bodies.earth, bodies.moon, bodies.mars]) {
    if (body.material.map) {
      body.material.map.colorSpace = THREE.SRGBColorSpace;
      body.material.map.anisotropy = Math.min(4, renderer.capabilities.getMaxAnisotropy());
    }
    body.material.needsUpdate = true;
  }
}

function loadTexture(url) {
  return new Promise((resolve) => {
    textureLoader.load(url, (tex) => resolve(tex), undefined, () => resolve(null));
  });
}

function makeFallbackEarthTexture() {
  const c = document.createElement("canvas");
  c.width = 1024;
  c.height = 512;
  const ctx = c.getContext("2d");
  ctx.fillStyle = "#08173b";
  ctx.fillRect(0, 0, c.width, c.height);

  const grad = ctx.createLinearGradient(0, 0, c.width, c.height);
  grad.addColorStop(0, "#0b2c7a");
  grad.addColorStop(1, "#05143c");
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, c.width, c.height);

  const blobs = [
    [130, 170, 160, 110, "#5b8d3a"],
    [250, 300, 100, 180, "#4a7f31"],
    [360, 190, 230, 150, "#9d8f62"],
    [540, 160, 220, 130, "#7d6f4b"],
    [720, 220, 260, 170, "#4f8530"],
    [860, 300, 150, 120, "#a67b4d"],
  ];
  for (const [x, y, w, h, color] of blobs) {
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.ellipse(x, y, w, h, Math.random() * 0.5, 0, Math.PI * 2);
    ctx.fill();
  }
  const tex = new THREE.CanvasTexture(c);
  tex.colorSpace = THREE.SRGBColorSpace;
  return tex;
}

function solveKepler(M, e) {
  let E = M;
  for (let i = 0; i < 5; i += 1) {
    E = E - (E - e * Math.sin(E) - M) / (1 - e * Math.cos(E));
  }
  return E;
}

function orbitalPosition(days, el) {
  const n = (2 * Math.PI) / el.periodDays;
  const M0 = ((el.L0 - el.omega) * DEG) % (2 * Math.PI);
  const M = (M0 + n * days) % (2 * Math.PI);
  const E = solveKepler(M, el.e);
  const v = 2 * Math.atan2(Math.sqrt(1 + el.e) * Math.sin(E / 2), Math.sqrt(1 - el.e) * Math.cos(E / 2));
  const r = el.a * (1 - el.e * Math.cos(E));

  const xh = r * (Math.cos(el.Omega * DEG) * Math.cos(v + el.omega * DEG) - Math.sin(el.Omega * DEG) * Math.sin(v + el.omega * DEG) * Math.cos(el.i * DEG));
  const zh = r * (Math.sin(el.Omega * DEG) * Math.cos(v + el.omega * DEG) + Math.cos(el.Omega * DEG) * Math.sin(v + el.omega * DEG) * Math.cos(el.i * DEG));
  const yh = r * (Math.sin(v + el.omega * DEG) * Math.sin(el.i * DEG));

  return { x: xh * AU_TO_SCENE, y: yh * AU_TO_SCENE, z: zh * AU_TO_SCENE };
}

function daysSinceEpoch(dt) {
  const epoch = new Date("2000-01-01T12:00:00Z");
  return (dt.getTime() - epoch.getTime()) / (1000 * 60 * 60 * 24);
}

function updateFromRange(daysOffset) {
  const dt = new Date(state.baseDate.getTime() + daysOffset * 86400000);
  state.currentDate = dt;
  timeLabel.textContent = dt.toISOString().slice(0, 10);

  const days = daysSinceEpoch(dt);
  const earth = orbitalPosition(days, ELEMENTS.earth);
  const moonRel = orbitalPosition(days, ELEMENTS.moon);
  const mars = orbitalPosition(days, ELEMENTS.mars);

  bodies.earth.position.set(earth.x, earth.y, earth.z);
  bodies.mars.position.set(mars.x, mars.y, mars.z);
  bodies.moon.position.set(earth.x + moonRel.x, earth.y + moonRel.y, earth.z + moonRel.z);

  bodies.earth.rotation.y = days * 2.0;
  bodies.moon.rotation.y = days * 0.85;
  bodies.mars.rotation.y = days * 1.5;
  if (clouds) clouds.rotation.y = days * 2.4;

  statusEl.textContent = state.catalog?.system_name || statusEl.textContent;
}

function updateEphemeris(ephemeris) {
  statusEl.textContent = ephemeris?.render_notes?.model || statusEl.textContent;
}

function onPointerMove(event) {
  const rect = canvas.getBoundingClientRect();
  pointer.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
  pointer.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
  raycaster.setFromCamera(pointer, camera);
  const hits = raycaster.intersectObjects(pickables, true);
  hovered = hits.length ? hits[0].object : null;
  canvas.style.cursor = hovered ? "pointer" : "default";
}

function onPointerClick() {
  if (!hovered) return;
  hovered.getWorldPosition(tmpV1);
  controls.target.copy(tmpV1);
}

function positionLabels() {
  const entries = Object.entries({ sun: bodies.sun, earth: bodies.earth, moon: bodies.moon, mars: bodies.mars });
  for (const [name, obj] of entries) {
    obj.getWorldPosition(tmpV1);
    tmpV2.copy(tmpV1).project(camera);
    const x = (tmpV2.x * 0.5 + 0.5) * window.innerWidth;
    const y = (-tmpV2.y * 0.5 + 0.5) * window.innerHeight;
    labels[name].style.left = `${x}px`;
    labels[name].style.top = `${y}px`;

    const visible = tmpV2.z < 1 && tmpV2.z > -1 && (name !== "moon" || camera.position.distanceTo(obj.position) < 350);
    labels[name].style.display = state.showLabels && visible ? "block" : "none";
  }
}

function animate() {
  if (!running) return;
  requestAnimationFrame(animate);
  controls.update();

  if (!prefersReducedMotion) {
    starField.rotation.y += 0.00003;
    starField.rotation.x += 0.00001;
  }

  const d = camera.position.length();
  distanceLabel.textContent = `camera distance: ${d.toFixed(1)}`;

  const orbitAlpha = state.showOrbits ? THREE.MathUtils.clamp(1 - d / 1200, 0.15, 0.5) : 0;
  orbitLines.forEach((line) => (line.material.opacity = orbitAlpha));

  state.frameCount += 1;
  if (state.frameCount % 2 === 0) {
    positionLabels();
  }

  renderer.render(scene, camera);
}

function onVisibilityChange() {
  if (document.hidden) {
    running = false;
    return;
  }
  if (!running) {
    running = true;
    animate();
  }
}

window.addEventListener("resize", () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
