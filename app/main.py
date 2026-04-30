from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request

app = FastAPI(title="Space Twin Starter")

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/catalog")
async def catalog() -> dict:
    return {
        "system_name": "Inner Solar System (starter)",
        "bodies": ["sun", "earth", "moon", "mars"],
        "units": {"distance": "au", "time": "days"},
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/api/ephemeris")
async def ephemeris() -> dict:
    return {
        "render_notes": {
            "model": "Simplified Keplerian circular-ish orbits for visualization",
            "accuracy": "not research grade",
        },
        "source": "starter",
    }


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}
