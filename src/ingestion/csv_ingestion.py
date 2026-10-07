import pandas as pd


def load_csv(file_path):
    """Load insurance policy data from a CSV file."""

    print(f"Loading data from: {file_path}")

    dataframe = pd.read_csv(file_path)

    print(f"Successfully loaded {len(dataframe)} records.")

    return dataframe