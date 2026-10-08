
import sqlite3
from pathlib import Path

import pandas as pd


DATABASE_PATH = Path("data/insurance_policies.db")


def get_connection():
    """Create a connection to the SQLite database."""

    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    return sqlite3.connect(DATABASE_PATH)


def initialize_database():
    """Create the insurance policies table if it doesn't exist."""

    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS policies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                policy_number TEXT NOT NULL,
                customer_name TEXT NOT NULL,
                effective_date TEXT NOT NULL,
                expiration_date TEXT NOT NULL,
                coverage_type TEXT NOT NULL,
                annual_premium REAL NOT NULL,
                deductible REAL NOT NULL,
                source_carrier TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(source_carrier, policy_number)
            )
        """)

    print("Database initialized successfully.")


def save_policies(dataframe):
    """Save valid policies to the database."""

    if dataframe.empty:
        print("No valid policies to save.")
        return

    columns = [
        "policy_number",
        "customer_name",
        "effective_date",
        "expiration_date",
        "coverage_type",
        "annual_premium",
        "deductible",
        "source_carrier",
    ]

    records = list(
        dataframe[columns].itertuples(
            index=False,
            name=None,
        )
    )

    with get_connection() as connection:
        connection.executemany("""
            INSERT INTO policies (
                policy_number,
                customer_name,
                effective_date,
                expiration_date,
                coverage_type,
                annual_premium,
                deductible,
                source_carrier
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(source_carrier, policy_number)
            DO UPDATE SET
                customer_name = excluded.customer_name,
                effective_date = excluded.effective_date,
                expiration_date = excluded.expiration_date,
                coverage_type = excluded.coverage_type,
                annual_premium = excluded.annual_premium,
                deductible = excluded.deductible
        """, records)

    print(f"Processed {len(records)} policies for database storage.")


def get_policy_count():
    """Return the number of policies stored."""

    with get_connection() as connection:
        result = connection.execute(
            "SELECT COUNT(*) FROM policies"
        ).fetchone()

    return result[0]


def get_all_policies():
    """Retrieve stored policies as a DataFrame."""

    with get_connection() as connection:
        return pd.read_sql_query(
            "SELECT * FROM policies ORDER BY id",
            connection,
        )
