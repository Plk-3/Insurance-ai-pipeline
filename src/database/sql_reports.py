
import pandas as pd

from src.database.database_manager import get_connection


def policies_by_carrier():
    """Count policies and total premiums by carrier."""

    query = """
        SELECT
            source_carrier,
            COUNT(*) AS policy_count,
            ROUND(SUM(annual_premium), 2) AS total_premium
        FROM policies
        GROUP BY source_carrier
        ORDER BY source_carrier
    """

    with get_connection() as connection:
        return pd.read_sql_query(query, connection)


def premiums_by_coverage():
    """Summarize insurance premiums by coverage type."""

    query = """
        SELECT
            coverage_type,
            COUNT(*) AS policy_count,
            ROUND(AVG(annual_premium), 2) AS average_premium,
            ROUND(SUM(annual_premium), 2) AS total_premium
        FROM policies
        GROUP BY coverage_type
        ORDER BY total_premium DESC
    """

    with get_connection() as connection:
        return pd.read_sql_query(query, connection)


def highest_premium_policies(limit=5):
    """Return policies with the highest premiums."""

    query = """
        SELECT
            policy_number,
            customer_name,
            source_carrier,
            coverage_type,
            annual_premium
        FROM policies
        ORDER BY annual_premium DESC
        LIMIT ?
    """

    with get_connection() as connection:
        return pd.read_sql_query(
            query,
            connection,
            params=(limit,),
        )
