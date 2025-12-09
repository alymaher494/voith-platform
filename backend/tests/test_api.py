"""
Tests for src/api.py main FastAPI application.
"""
import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

from src.api import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


def test_root_endpoint(client):
    """Test the root endpoint returns correct information."""
    response = client.get("/")
    assert response.status_code == 200

    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "status" in data
    assert "services" in data
    assert "documentation" in data
    assert "features" in data
    assert "usage" in data

    assert data["message"] == "🎬 Media Processing Studio API"
    assert data["version"] == "2.0.0"
    assert data["status"] == "running"


def test_health_check_endpoint(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "libraries" in data

    # Check that all libraries are reported as available
    libraries = data["libraries"]
    assert libraries["downloader"] == "available"
    assert libraries["converter"] == "available"
    assert libraries["asr"] == "available"


def test_app_initialization():
    """Test that the FastAPI app is properly initialized with routers and static files."""
    from src.api import app

    # Check that routers are included
    router_count = len(app.routes)
    # Should have at least the root route, health route, and 3 router prefixes
    assert router_count >= 5  # root + health + 3 routers

    # Check that static files are mounted
    mount_count = len([route for route in app.routes if hasattr(route, 'path') and ('files' in str(route.path) or 'downloads' in str(route.path))])
    assert mount_count >= 2  # /files and /downloads


def test_services_structure_in_root_response(client):
    """Test that the services structure in root response is correct."""
    response = client.get("/")
    data = response.json()

    services = data["services"]

    # Check current services
    current_services = services["current"]
    assert "downloader" in current_services
    assert "converter" in current_services
    assert "asr" in current_services

    # Check planned services
    planned_services = services["planned"]
    assert "translator" in planned_services
    assert "chat" in planned_services
    assert "editor" in planned_services


def test_documentation_links_in_root_response(client):
    """Test that documentation links are provided in root response."""
    response = client.get("/")
    data = response.json()

    docs = data["documentation"]
    assert docs["interactive"] == "/docs"
    assert docs["reference"] == "/redoc"
    assert docs["schema"] == "/openapi.json"


def test_features_in_root_response(client):
    """Test that features are listed in root response."""
    response = client.get("/")
    data = response.json()

    features = data["features"]
    assert features["file_access"] == "/files"
    assert features["health_check"] == "/health"
    assert features["background_processing"] is True
    assert features["microservices"] is True


def test_usage_examples_in_root_response(client):
    """Test that usage examples are provided in root response."""
    response = client.get("/")
    data = response.json()

    usage = data["usage"]
    assert "unified_server" in usage
    assert "converter_server" in usage
    assert usage["unified_server"] == "python main.py --api"
    assert usage["converter_server"] == "python main.py --converter-api"


def test_openapi_schema_available(client):
    """Test that OpenAPI schema is available."""
    response = client.get("/openapi.json")
    assert response.status_code == 200

    schema = response.json()
    assert "openapi" in schema
    assert "info" in schema
    assert "paths" in schema


def test_docs_endpoint_accessible(client):
    """Test that docs endpoint is accessible (returns HTML)."""
    response = client.get("/docs")
    # FastAPI docs returns HTML, so we just check it's not an error
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")


def test_redoc_endpoint_accessible(client):
    """Test that redoc endpoint is accessible (returns HTML)."""
    response = client.get("/redoc")
    # ReDoc returns HTML, so we just check it's not an error
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")