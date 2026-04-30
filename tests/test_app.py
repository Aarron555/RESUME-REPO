from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_index_page_renders() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "Space Twin Starter" in response.text
    assert "<canvas id=\"scene\"></canvas>" in response.text


def test_catalog_endpoint() -> None:
    response = client.get("/api/catalog")
    assert response.status_code == 200
    payload = response.json()
    assert payload["system_name"] == "Inner Solar System (starter)"
    assert set(payload["bodies"]) == {"sun", "earth", "moon", "mars"}
    assert payload["units"] == {"distance": "au", "time": "days"}


def test_ephemeris_endpoint() -> None:
    response = client.get("/api/ephemeris")
    assert response.status_code == 200
    payload = response.json()
    assert "render_notes" in payload
    assert payload["source"] == "starter"
