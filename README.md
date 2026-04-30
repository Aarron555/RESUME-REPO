# Space Twin Starter

A lightweight FastAPI + Three.js starter for an interactive 3D space viewer.

## What it includes

- FastAPI backend that serves the app and exposes a small ephemeris API
- WebGL 3D scene with:
  - procedural star field
  - Sun, Earth, Moon, Mars with realistic texture maps and fallback textures
  - orbit rings
  - atmospheric glow
  - zoom / pan / rotate controls
  - time slider
- A NASA Blue Marble texture hook for Earth (with a local fallback if the remote asset does not load)

This is a starter, not a full scientific ephemeris engine. The frontend now uses approximate elliptical orbital elements (eccentricity + inclination + Kepler solver) for improved visual accuracy, but it is still intended for plausibility rather than research-grade precision. For high-fidelity outputs, wire in JPL Horizons / SPICE later.

## Run

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open:

```text
http://127.0.0.1:8000
```

## Public asset notes

NASA's 3D Resources hub says its models and textures are free to download and use, and NASA's Blue Marble pages describe the Earth mosaic as a stitched true-color mosaic from satellite observations. The NASA SVS Blue Marble pages are the best place to swap in higher-resolution or additional time slices later.


## Performance notes

The starter includes browser-friendly defaults for regular laptops/desktops:
- adaptive scene quality (reduced star count/geometry on lower-power devices)
- capped pixel ratio for render cost control
- paused animation when the tab is hidden
- reduced-motion support
- throttled label projection updates


## Test

```bash
pytest -q
```

## Deploy (Docker)

```bash
docker build -t space-twin-starter .
docker run --rm -p 8000:8000 space-twin-starter
```

Then open `http://127.0.0.1:8000` in your browser.


## Native preview (no install)

If you want to quickly check the UI without FastAPI, use the standalone page:

1. Open `quickstart.html` directly in your browser, **or**
2. Serve the repo with Python standard library:

```bash
python -m http.server 8000
```

Then open `http://127.0.0.1:8000/quickstart.html`.

Note: In native preview mode, `/api/*` endpoints are unavailable, so the app automatically falls back to `offline demo`.

