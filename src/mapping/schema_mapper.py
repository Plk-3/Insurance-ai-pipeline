import pandas as pd

STANDARD_COLUMNS = [
    "policy_number",
    "customer_name",
    "effective_date",
    "expiration_date",
    "coverage_type",
    "annual_premium",
    "deductible",
    "source_carrier"
]

CARRIER_MAPPINGS = {
    "Carrier A": {
        "PolicyNumber": "policy_number",
        "CustomerName": "customer_name",
        "EffectiveDate": "effective_date",
        "ExpirationDate": "expiration_date",
        "CoverageType": "coverage_type",
        "AnnualPremium": "annual_premium",
        "Deductible": "deductible"
    },
    "Carrier B": {
        "Policy_ID": "policy_number",
        "Insured_Name": "customer_name",
        "Start_Date": "effective_date",
        "End_Date": "expiration_date",
        "Product": "coverage_type",
        "Premium": "annual_premium",
        "Deductible_Amount": "deductible"
    }
}


def standardize_data(dataframe, carrier):
    """Map carrier-specific fields to a common schema."""

    mapping = CARRIER_MAPPINGS[carrier]
    standardized = dataframe.rename(columns=mapping).copy()

    standardized["source_carrier"] = carrier

    for column in ["annual_premium", "deductible"]:
        standardized[column] = (
            standardized[column]
            .astype(str)
            .str.replace("$", "", regex=False)
            .str.replace(",", "", regex=False)
        )
        standardized[column] = pd.to_numeric(
            standardized[column], errors="coerce"
        )

    date_format = "%m/%d/%Y" if carrier == "Carrier B" else "%Y-%m-%d"

    for column in ["effective_date", "expiration_date"]:
        standardized[column] = pd.to_datetime(
            standardized[column],
            format=date_format,
            errors="coerce"
        ).dt.strftime("%Y-%m-%d")

    return standardized[STANDARD_COLUMNS]