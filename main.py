from pathlib import Path
import os
import pandas as pd

from src.ingestion.csv_ingestion import load_csv
from src.mapping.schema_mapper import standardize_data
from src.validation.data_validator import validate_policies


def main():
    carrier_files = {
        "Carrier A": "data/carrier_a/policies.csv",
        "Carrier B": "data/carrier_b/policies.csv",
        "Carrier C": "data/carrier_c/policies.csv",
    }

    mapping_mode = os.getenv("MAPPING_MODE", "mock")

    standardized_datasets = []

    for carrier, file_path in carrier_files.items():
        print(f"\nProcessing {carrier}...")

        raw_data = load_csv(file_path)

        clean_data = standardize_data(
            raw_data,
            carrier,
            mapping_mode=mapping_mode,
        )

        standardized_datasets.append(clean_data)

        print(f"Standardized {len(clean_data)} records.")

    combined_data = pd.concat(
        standardized_datasets,
        ignore_index=True,
    )

    validated_data = validate_policies(combined_data)

    valid_data = validated_data[
        validated_data["validation_status"] == "Valid"
    ].copy()

    invalid_data = validated_data[
        validated_data["validation_status"] == "Invalid"
    ].copy()

    output_folder = Path("data/standardized")
    output_folder.mkdir(parents=True, exist_ok=True)

    valid_data.to_csv(
        output_folder / "valid_policies.csv",
        index=False,
    )

    invalid_data.to_csv(
        output_folder / "invalid_policies.csv",
        index=False,
    )

    print("\n--- Validation Summary ---")
    print(f"Total policies: {len(validated_data)}")
    print(f"Valid policies: {len(valid_data)}")
    print(f"Invalid policies: {len(invalid_data)}")

    if not invalid_data.empty:
        print("\nValidation errors:")
        print(
            invalid_data[
                ["policy_number", "validation_errors"]
            ].to_string(index=False)
        )

    print("\nPipeline completed successfully!")


if __name__ == "__main__":
    main()

