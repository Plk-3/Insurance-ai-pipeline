
import pandas as pd


REQUIRED_COLUMNS = [
    "policy_number",
    "customer_name",
    "effective_date",
    "expiration_date",
    "coverage_type",
    "annual_premium",
    "deductible",
    "source_carrier",
]


def validate_policies(dataframe):
    """Validate standardized insurance policy records."""

    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("Expected a pandas DataFrame.")

    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in dataframe.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    validated = dataframe.copy()

    validated["validation_errors"] = ""
    validated["validation_status"] = "Valid"

    seen_policies = set()

    for index, row in validated.iterrows():
        errors = []

        for column in [
            "policy_number",
            "customer_name",
            "coverage_type",
            "source_carrier",
        ]:
            if (
                pd.isna(row[column])
                or str(row[column]).strip() == ""
            ):
                errors.append(f"Missing {column}")

        premium = pd.to_numeric(
            row["annual_premium"], errors="coerce"
        )
        deductible = pd.to_numeric(
            row["deductible"], errors="coerce"
        )

        if pd.isna(premium) or premium <= 0:
            errors.append("Invalid annual premium")

        if pd.isna(deductible) or deductible < 0:
            errors.append("Invalid deductible")

        effective = pd.to_datetime(
            row["effective_date"], errors="coerce"
        )
        expiration = pd.to_datetime(
            row["expiration_date"], errors="coerce"
        )

        if pd.isna(effective):
            errors.append("Invalid effective date")

        if pd.isna(expiration):
            errors.append("Invalid expiration date")

        if (
            not pd.isna(effective)
            and not pd.isna(expiration)
            and expiration <= effective
        ):
            errors.append("Expiration must follow effective date")

        policy_number = row["policy_number"]
        carrier = row["source_carrier"]

        if pd.notna(policy_number) and pd.notna(carrier):
            policy_key = (
                str(carrier).strip().lower(),
                str(policy_number).strip().lower(),
            )

            if policy_key in seen_policies:
                errors.append("Duplicate policy number")
            else:
                seen_policies.add(policy_key)

        if errors:
            validated.at[index, "validation_status"] = "Invalid"
            validated.at[index, "validation_errors"] = "; ".join(errors)

    return validated
