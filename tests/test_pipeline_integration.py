
from pathlib import Path

import pandas as pd

from src.ingestion.csv_ingestion import load_csv
from src.mapping.schema_mapper import standardize_data
from src.validation.data_validator import validate_policies


def test_three_carrier_pipeline():
    carrier_files = {
        "Carrier A": "data/carrier_a/policies.csv",
        "Carrier B": "data/carrier_b/policies.csv",
        "Carrier C": "data/carrier_c/policies.csv",
    }

    datasets = []

    for carrier, file_path in carrier_files.items():
        assert Path(file_path).exists()

        raw_data = load_csv(file_path)

        standardized = standardize_data(
            raw_data,
            carrier,
            mapping_mode="mock",
        )

        datasets.append(standardized)

    combined = pd.concat(datasets, ignore_index=True)
    result = validate_policies(combined)

    assert len(result) == 25
    assert (result["validation_status"] == "Valid").all()
    assert result["source_carrier"].nunique() == 3
