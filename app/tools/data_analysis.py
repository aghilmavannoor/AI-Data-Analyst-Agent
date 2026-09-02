import pandas as pd
from sqlalchemy import create_engine, text
from pathlib import Path


# Project directory
BASE_DIR = Path(__file__).resolve().parents[2]

# Database path
DATABASE_PATH = BASE_DIR / "data" / "ecommerce.db"


# Create database connection
engine = create_engine(
    f"sqlite:///{DATABASE_PATH}"
)


def run_query(query):
    """
    Execute a SQL query and return the result
    as a Pandas DataFrame.
    """

    with engine.connect() as connection:
        dataframe = pd.read_sql(
            text(query),
            connection
        )

    return dataframe


# Test query
query = """
SELECT
    p.category,
    SUM(o.quantity * p.price) AS total_revenue
FROM orders o
JOIN products p
    ON o.product_id = p.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;
"""


# Run query
df = run_query(query)


# Display result
print(df)