import os
os.environ["DATABASE_URL"] = "sqlite:///./test_api_navora.db"

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def client():
    from db.base import Base
    from db.session import engine
    import models  # noqa: F401
    Base.metadata.create_all(engine)

    from main import app
    with TestClient(app) as c:
        yield c

    Base.metadata.drop_all(engine)
    if os.path.exists("./test_api_navora.db"):
        os.remove("./test_api_navora.db")


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_create_decision_end_to_end(client):
    payload = {
        "commodity": "Coking Coal",
        "cargo_quantity": 80000,
        "origin": "Australia",
        "destination": "Vizag",
        "earliest_loading_date": "2026-10-01",
        "latest_delivery_date": "2026-10-30",
        "contract_preference": "AUTO",
        "currency": "USD",
    }
    resp = client.post("/api/decision", json=payload)
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "COMPLETED"
    assert body["feasibility"]["port_compatible"] is True
    assert any(r["vessel_class"] == "Capesize" and not r["is_feasible"] for r in body["recommendation"])
    assert body["recommendation"][0]["is_feasible"] is True


def test_invalid_decision_returns_422(client):
    payload = {
        "commodity": "Coking Coal",
        "cargo_quantity": 80000,
        "origin": "Australia",
        "destination": "Australia",
        "earliest_loading_date": "2026-10-01",
        "latest_delivery_date": "2026-10-30",
        "contract_preference": "AUTO",
        "currency": "USD",
    }
    resp = client.post("/api/decision", json=payload)
    assert resp.status_code == 422
