
import sqlite3

import pandas as pd
import pytest

from src.database import database_manager as db


@pytest.fixture
def test_database(tmp_path, monkeypatch):
    """Create an isolated database for each test."""

    database_path = tmp_path / "test_insurance.db"
    monkeypatch.setattr(db, "DATABASE_PATH", database_path)

    db.initialize_database()

    return database_path


def sample_policies():
    """Return two fictional insurance policies."""

    return pd.DataFrame([
        {
            "policy_number": "TEST-001",
            "customer_name": "Jordan Smith",
            "effective_date": "2026-01-01",
            "expiration_date": "2026-12-31",
            "coverage_type": "Auto",
            "annual_premium": 1200.00,
            "deductible": 500.00,
            "source_carrier": "Test Carrier",
        },
        {
            "policy_number": "TEST-002",
            "customer_name": "Taylor Jones",
            "effective_date": "2026-02-01",
            "expiration_date": "2027-01-31",
            "coverage_type": "Home",
            "annual_premium": 2400.00,
            "deductible": 1000.00,
            "source_carrier": "Test Carrier",
        },
    ])


def test_database_initialization(test_database):
    """Verify the policies table is created."""

    with sqlite3.connect(test_database) as connection:
        result = connection.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type='table' AND name='policies'"
        ).fetchone()

    assert result is not None


def test_save_policies(test_database):
    """Verify records can be inserted."""

    db.save_policies(sample_policies())

    assert db.get_policy_count() == 2


def test_duplicate_prevention(test_database):
    """Verify repeated imports do not create duplicates."""

    policies = sample_policies()

    db.save_policies(policies)
    db.save_policies(policies)

    assert db.get_policy_count() == 2


def test_policy_update(test_database):
    """Verify an existing policy can be updated."""

    policies = sample_policies()
    db.save_policies(policies)

    policies.loc[0, "annual_premium"] = 1500.00
    db.save_policies(policies)

    stored = db.get_all_policies()

    updated = stored[
        stored["policy_number"] == "TEST-001"
    ].iloc[0]

    assert updated["annual_premium"] == 1500.00


def test_retrieve_policies(test_database):
    """Verify policies can be queried."""

    db.save_policies(sample_policies())

    result = db.get_all_policies()

    assert len(result) == 2
    assert "policy_number" in result.columns
    assert "annual_premium" in result.columns
