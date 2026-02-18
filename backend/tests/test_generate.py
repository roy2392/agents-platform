"""Tests for agent generation."""
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "endpoints" in data


def test_generate_requires_prompt():
    response = client.post("/api/agents/generate", json={"prompt": "hi"})
    assert response.status_code == 422  # prompt too short (min 10 chars)


def test_a2a_directory_empty():
    response = client.get("/a2a/directory")
    assert response.status_code == 200
    assert response.json()["agents"] == []


def test_mcp_servers_empty():
    response = client.get("/mcp/servers")
    assert response.status_code == 200
    assert response.json()["servers"] == []


def test_deployments_empty():
    response = client.get("/api/agents/deployments")
    assert response.status_code == 200
