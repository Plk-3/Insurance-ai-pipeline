
import pytest

from src.mapping.ai_mapper import (
    MOCK_MAPPING,
    suggest_mapping,
    validate_mapping,
)


def test_mock_mapping():
    columns = list(MOCK_MAPPING.keys())

    result = suggest_mapping(columns, mode="mock")

    assert result == MOCK_MAPPING


def test_mapping_has_correct_targets():
    columns = list(MOCK_MAPPING.keys())

    result = suggest_mapping(columns, mode="mock")

    assert result["PolicyRef"] == "policy_number"
    assert result["WrittenPremium"] == "annual_premium"


def test_invalid_mode():
    with pytest.raises(ValueError):
        suggest_mapping(["PolicyRef"], mode="unknown")


def test_duplicate_target_rejected():
    invalid_mapping = MOCK_MAPPING.copy()
    invalid_mapping["Excess"] = "annual_premium"

    with pytest.raises(ValueError):
        validate_mapping(
            invalid_mapping,
            list(MOCK_MAPPING.keys()),
        )


def test_missing_source_column_rejected():
    incomplete_mapping = MOCK_MAPPING.copy()
    del incomplete_mapping["Excess"]

    with pytest.raises(ValueError):
        validate_mapping(
            incomplete_mapping,
            list(MOCK_MAPPING.keys()),
        )
