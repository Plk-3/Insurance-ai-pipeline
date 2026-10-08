
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
    """Validate that the suggested mapping is complete and unique."""

    if not isinstance(mapping, dict):
        raise ValueError("Mapping must be a dictionary.")

    if len(source_columns) != len(set(source_columns)):
        raise ValueError("Duplicate source column names detected.")

    if set(mapping.keys()) != set(source_columns):
        raise ValueError(
            "Mapping must contain exactly the supplied source columns."
        )

    if set(mapping.values()) != set(TARGET_COLUMNS):
        raise ValueError(
            "Mapping must contain each target column exactly once."
        )

    return mapping


def suggest_mapping(source_columns, mode="mock"):
    """
    Suggest mappings using mock data or the OpenAI API.

    Mock mode does not make API calls.
    Live mode sends source column names to OpenAI.
    """

    if mode == "mock":
        try:
            mapping = {
                column: MOCK_MAPPING[column]
                for column in source_columns
            }
        except KeyError as error:
            raise ValueError(
                f"No mock mapping available for: {error}"
            ) from error

    elif mode == "live":
        if not os.getenv("OPENAI_API_KEY"):
            raise RuntimeError(
                "OPENAI_API_KEY is not configured."
            )

        client = OpenAI(timeout=30.0, max_retries=1)

        prompt = (
            "You are an insurance data engineering assistant. "
            "Map each source column to exactly one target column. "
            "Do not invent columns or values. "
            "Return the mapping as a JSON object.\n\n"
            f"Source columns: {json.dumps(source_columns)}\n"
            f"Target columns: {json.dumps(TARGET_COLUMNS)}"
        )

        try:
            response = client.responses.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
                input=prompt,
                text={
                    "format": {
                        "type": "json_schema",
                        "name": "insurance_column_mapping",
                        "strict": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                column: {
                                    "type": "string",
                                    "enum": TARGET_COLUMNS,
                                }
                                for column in source_columns
                            },
                            "required": source_columns,
                            "additionalProperties": False,
                        },
                    }
                },
            )

            mapping = json.loads(response.output_text)

        except Exception as error:
            raise RuntimeError(
                f"OpenAI mapping request failed: {error}"
            ) from error

    else:
        raise ValueError("Mode must be 'mock' or 'live'.")

    return validate_mapping(mapping, source_columns)
