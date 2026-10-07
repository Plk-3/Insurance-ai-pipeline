from src.ingestion.csv_ingestion import load_csv


def main():
    file_path = "data/carrier_a/policies.csv"

    policies = load_csv(file_path)

    print("\nCarrier A Policy Data:")
    print(policies.head())


if __name__ == "__main__":
    main()
