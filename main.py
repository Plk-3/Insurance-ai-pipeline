from pathlib import Path
import pandas as pd

from src.ingestion.csv_ingestion import load_csv
from src.mapping.schema_mapper import standardize_data


def main():
    carrier_files = {
        "Carrier A": "data/carrier_a/policies.csv",
        "Carrier B": "data/carrier_b/policies.csv"
    }

    standardized_datasets = []

    for carrier, file_path in carrier_files.items():
        print(f"\nProcessing {carrier}...")

        raw_data = load_csv(file_path)
        clean_data = standardize_data(raw_data, carrier)

        standardized_datasets.append(clean_data)

        print(f"Standardized {len(clean_data)} records.")

    combined_data = pd.concat(
        standardized_datasets,
        ignore_index=True
    )

    output_path = Path("data/standardized/policies.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    combined_data.to_csv(output_path, index=False)

    print("\nPipeline completed successfully!")
    print(f"Total policies processed: {len(combined_data)}")
    print(f"Output saved to: {output_path}")
    print("\nSample standardized records:")
    print(combined_data.head())


if __name__ == "__main__":
    main()