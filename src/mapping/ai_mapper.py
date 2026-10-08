
import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

TARGET_COLUMNS = [
    "policy_number",
    "customer_name",
    "effective_date",
    "expiration_date",
    "coverage_type",
    "annual_premium",
    "deductible",
]

MOCK_MAPPING = {
    "PolicyRef": "policy_number",
    "Insured": "customer_name",
    "Inception": "effective_date",
    "Termination": "expiration_date",
    "InsuranceProduct": "coverage_type",
    "WrittenPremium": "annual_premium",
    "Excess": "deductible",
}


def validate_mapping(mapping, source_columns):
    """Reject unknown, duplicate, or incomplete mappings."""
    if not isinstance(mapping, dict):
        raise ValueError("Mapping must be a dictionary.")

    if set(mapping.keys()) != set(source_columns):
        raise ValueError("Mapping must include every source column.")

    if set(mapping.values()) != set(TARGET_COLUMNS):
        raise ValueError("Mapping must match the target schema exactly.")

    return mapping


def suggest_mapping(source_columns, mode="mock"):
    """Suggest a source-to-target column mapping."""

    if mode == "mock":
        mapping = {
            column: MOCK_MAPPING[column]
            for column in source_columns
        }

    elif mode == "live":
        client = OpenAI()

        prompt = (
            "You are a data engineering assistant. "
            "Map insurance source columns to target columns. "
            "Return only a JSON object with source column names "
            "as keys and target column names as values. "
            "Do not invent fields.\n\n"
            f"Source columns: {json.dumps(source_columns)}\n"
            f"Target columns: {json.dumps(TARGET_COLUMNS)}"
        )

        response = client.responses.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
            input=prompt,
        )

        mapping = json.loads(response.output_text)

    else:
        raise ValueError("Mode must be 'mock' or 'live'.")

    return validate_mapping(mapping, source_columns)
