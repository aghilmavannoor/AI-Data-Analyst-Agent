import sys
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text


# ==========================================
# PROJECT PATH
# ==========================================

BASE_DIR = Path(__file__).resolve().parents[2]

DATABASE_PATH = BASE_DIR / "data" / "ecommerce.db"


# ==========================================
# DATABASE CONNECTION
# ==========================================

engine = create_engine(
    f"sqlite:///{DATABASE_PATH}"
)


# ==========================================
# SQL TOOL
# ==========================================

def run_sql(sql):
    """
    Execute a read-only SQL query and return
    a Pandas DataFrame.
    """

    sql_lower = sql.strip().lower()

    forbidden = [
        "insert",
        "update",
        "delete",
        "drop",
        "alter",
        "create",
        "replace",
        "truncate"
    ]

    for keyword in forbidden:

        if keyword in sql_lower:

            raise ValueError(
                f"Unsafe SQL detected: {keyword}"
            )

    if not sql_lower.startswith("select"):

        raise ValueError(
            "Only SELECT queries are allowed."
        )

    with engine.connect() as connection:

        result = pd.read_sql(
            text(sql),
            connection
        )

    return result


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    query = """
    SELECT
        p.category,
        SUM(o.quantity * p.price) AS revenue
    FROM orders o
    JOIN products p
        ON o.product_id = p.product_id
    GROUP BY p.category
    ORDER BY revenue DESC;
    """

    result = run_sql(query)

    print("\nSQL Tool Result:\n")
    print(result)