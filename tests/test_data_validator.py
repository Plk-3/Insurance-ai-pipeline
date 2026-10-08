
import pandas as pd

from src.validation.data_validator import validate_policies


def make_policy(**overrides):
    """Create a sample policy for testing."""

    policy = {
        "policy_number": "TEST-1001",
        "customer_name": "Test Customer",
        "effective_date": "2026-01-01",
        "expiration_date": "2026-12-31",
        "coverage_type": "Auto",
        "annual_premium": 1200.00,
        "deductible": 500.00,
        "source_carrier": "Carrier A",
    }

    policy.update(overrides)
    return policy


def test_valid_policy():
    data = pd.DataFrame([make_policy()])
    result = validate_policies(data)

    assert result.iloc[0]["validation_status"] == "Valid"


def test_missing_policy_number():
    data = pd.DataFrame([
        make_policy(policy_number=None)
    ])
    result = validate_policies(data)

    assert result.iloc[0]["validation_status"] == "Invalid"
    assert "Missing policy_number" in result.iloc[0]["validation_errors"]


def test_negative_premium():
    data = pd.DataFrame([
        make_policy(annual_premium=-500)
    ])
    result = validate_policies(data)

    assert result.iloc[0]["validation_status"] == "Invalid"
    assert "Invalid annual premium" in result.iloc[0]["validation_errors"]


def test_invalid_expiration_date():
    data = pd.DataFrame([
        make_policy(expiration_date="2025-12-31")
    ])
    result = validate_policies(data)

    assert result.iloc[0]["validation_status"] == "Invalid"
    assert "Expiration must follow effective date" in result.iloc[0]["validation_errors"]


def test_duplicate_policy():
    data = pd.DataFrame([
        make_policy(),
        make_policy(customer_name="Another Customer"),
    ])
    result = validate_policies(data)

    assert result.iloc[0]["validation_status"] == "Valid"
    assert result.iloc[1]["validation_status"] == "Invalid"
    assert "Duplicate policy number" in result.iloc[1]["validation_errors"]


def test_missing_coverage_type():
    data = pd.DataFrame([
        make_policy(coverage_type="")
    ])
    result = validate_policies(data)

    assert result.iloc[0]["validation_status"] == "Invalid"
    assert "Missing coverage_type" in result.iloc[0]["validation_errors"]
