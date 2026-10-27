# ruff: noqa: S101, D100, D101, D102, D103
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.core.cors import configure_cors
from src.settings import App, Settings

ALLOWED_ORIGIN = "http://localhost:8000"
EVIL_ORIGIN = "http://evil.example"


def test_preflight_allowed_origin_has_no_credentials(api_client):
    response = api_client.options(
        "/api/v1/stores",
        headers={
            "Origin": ALLOWED_ORIGIN,
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "x-api-key",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == ALLOWED_ORIGIN
    assert "access-control-allow-credentials" not in response.headers


def test_simple_request_allowed_origin_has_no_credentials(api_client):
    response = api_client.get("/api/v1/stores", headers={"Origin": ALLOWED_ORIGIN})

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == ALLOWED_ORIGIN
    assert "access-control-allow-credentials" not in response.headers


def test_disallowed_origin_is_rejected(api_client):
    response = api_client.get("/api/v1/stores", headers={"Origin": EVIL_ORIGIN})
    assert response.status_code == 200
    assert "access-control-allow-origin" not in response.headers

    preflight = api_client.options(
        "/api/v1/stores",
        headers={
            "Origin": EVIL_ORIGIN,
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "x-api-key",
        },
    )
    assert preflight.status_code == 400
    assert "access-control-allow-origin" not in preflight.headers


def _wildcard_client() -> TestClient:
    app = FastAPI()
    configure_cors(app, Settings(app=App(cors_origins=["*"])))

    @app.get("/ping")
    def ping() -> dict[str, bool]:
        return {"ok": True}

    return TestClient(app)


def test_wildcard_origin_is_not_reflected_on_simple_request():
    response = _wildcard_client().get("/ping", headers={"Origin": EVIL_ORIGIN})

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "*"
    assert "access-control-allow-credentials" not in response.headers


def test_wildcard_origin_is_not_reflected_on_preflight():
    response = _wildcard_client().options(
        "/ping",
        headers={
            "Origin": EVIL_ORIGIN,
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "x-api-key",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "*"
    assert "access-control-allow-credentials" not in response.headers
