
import pytest
import pandas as pd
from fastapi.testclient import TestClient

from src.api.app import app
from src.database import database_manager as db


@pytest.fixture
def client(tmp_path, monkeypatch):
    """Create an isolated test database and API client."""

    test_db = tmp_path / "test_api.db"
    monkeypatch.setattr(db, "DATABASE_PATH", test_db)

    db.initialize_database()

    sample_data = pd.DataFrame([
        {
            "policy_number": "API-001",
            "customer_name": "Jordan Smith",
            "effective_date": "2026-01-01",
            "expiration_date": "2026-12-31",
            "coverage_type": "Auto",
            "annual_premium": 1200.00,
            "deductible": 500.00,
            "source_carrier": "Test Carrier",
        },
        {
            "policy_number": "API-002",
            "customer_name": "Taylor Jones",
            "effective_date": "2026-02-01",
            "expiration_date": "2027-01-31",
            "coverage_type": "Home",
            "annual_premium": 2400.00,
            "deductible": 1000.00,
            "source_carrier": "Test Carrier",
        },
    ])

    db.save_policies(sample_data)

    with TestClient(app) as test_client:
        yield test_client


def test_home(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_policy_count(client):
    response = client.get("/policies/count")

    assert response.status_code == 200
    assert response.json()["total_policies"] == 2


def test_list_policies(client):
    response = client.get("/policies")

    assert response.status_code == 200
    assert response.json()["total"] == 2
    assert len(response.json()["policies"]) == 2


def test_policy_pagination(client):
    response = client.get("/policies?limit=1&offset=1")

    assert response.status_code == 200
    assert len(response.json()["policies"]) == 1
    assert response.json()["policies"][0]["policy_number"] == "API-002"


def test_get_specific_policy(client):
    response = client.get("/policies/API-001")

    assert response.status_code == 200
    assert response.json()["policy_number"] == "API-001"
    assert response.json()["customer_name"] == "Jordan Smith"


def test_policy_not_found(client):
    response = client.get("/policies/DOES-NOT-EXIST")

    assert response.status_code == 404


def test_invalid_pagination(client):
    response = client.get("/policies?limit=0")

    assert response.status_code == 422
