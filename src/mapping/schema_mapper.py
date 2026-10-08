
import pandas as pd

from src.mapping.ai_mapper import suggest_mapping


# Standardized insurance policy schema
# All carrier data will be converted to these columns.

STANDARD_COLUMNS = [
    "policy_number",
    "customer_name",
    "effective_date",
    "expiration_date",
    "coverage_type",
    "annual_premium",
    "deductible",
    "source_carrier",
]


# Predefined mappings for known insurance carriers.
# Carrier C will use the AI mapping module instead.

CARRIER_MAPPINGS = {
    "Carrier A": {
        "PolicyNumber": "policy_number",
        "CustomerName": "customer_name",
        "EffectiveDate": "effective_date",
        "ExpirationDate": "expiration_date",
        "CoverageType": "coverage_type",
        "AnnualPremium": "annual_premium",
        "Deductible": "deductible",
    },

    "Carrier B": {
        "Policy_ID": "policy_number",
        "Insured_Name": "customer_name",
        "Start_Date": "effective_date",
        "End_Date": "expiration_date",
        "Product": "coverage_type",
        "Premium": "annual_premium",
        "Deductible_Amount": "deductible",
    },
}


def standardize_data(dataframe, carrier, mapping_mode="mock"):
    """
    Standardize insurance policy data from different carriers.

    Known carriers:
        Use predefined column mappings.

    Unknown carriers:
        Use the AI mapping module to suggest mappings.

    Parameters:
        dataframe: pandas DataFrame containing carrier data.
        carrier: Name of the insurance carrier.
        mapping_mode: "mock" or "live".

    Returns:
        A standardized pandas DataFrame.
    """

    # Step 1: Identify the correct column mapping

    if carrier in CARRIER_MAPPINGS:

        mapping = CARRIER_MAPPINGS[carrier]

        print(f"Using predefined mapping for {carrier}")

    else:

        print(f"Requesting intelligent mapping for {carrier}")

        mapping = suggest_mapping(
            source_columns=list(dataframe.columns),
            mode=mapping_mode,
        )

        print(f"Suggested mapping: {mapping}")

    # Step 2: Rename carrier columns to standardized names

    standardized = dataframe.rename(columns=mapping).copy()

    # Step 3: Identify the source carrier

    standardized["source_carrier"] = carrier

    # Step 4: Clean and convert currency fields

    currency_columns = [
        "annual_premium",
        "deductible",
    ]

    for column in currency_columns:

        standardized[column] = (
            standardized[column]
            .astype(str)
            .str.replace("$", "", regex=False)
            .str.replace(",", "", regex=False)
            .str.strip()
        )

        standardized[column] = pd.to_numeric(
            standardized[column],
            errors="coerce",
        )

    # Step 5: Standardize date formats

    if carrier == "Carrier B":
        date_format = "%m/%d/%Y"
    else:
        date_format = "%Y-%m-%d"

    date_columns = [
        "effective_date",
        "expiration_date",
    ]

    for column in date_columns:

        standardized[column] = pd.to_datetime(
            standardized[column],
            format=date_format,
            errors="coerce",
        ).dt.strftime("%Y-%m-%d")

    # Step 6: Ensure consistent column order

    standardized = standardized[STANDARD_COLUMNS]

    # Step 7: Return the standardized dataset

    return standardized
