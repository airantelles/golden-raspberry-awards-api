"""Integration tests for the running API surface."""

from fastapi.testclient import TestClient

from app.main import create_app


def test_health_reports_that_the_api_is_available() -> None:
    """The application factory exposes the minimal health endpoint."""
    with TestClient(create_app()) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
