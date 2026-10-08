
from src.database.sql_reports import (
    policies_by_carrier,
    premiums_by_coverage,
    highest_premium_policies,
)


def main():
    print("\n=== POLICIES BY CARRIER ===")
    print(policies_by_carrier().to_string(index=False))

    print("\n=== PREMIUMS BY COVERAGE TYPE ===")
    print(premiums_by_coverage().to_string(index=False))

    print("\n=== TOP 5 HIGHEST PREMIUM POLICIES ===")
    print(highest_premium_policies().to_string(index=False))


if __name__ == "__main__":
    main()
