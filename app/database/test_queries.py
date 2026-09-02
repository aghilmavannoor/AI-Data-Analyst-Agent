from sqlalchemy import create_engine, text
from pathlib import Path


# Project directory
BASE_DIR = Path(__file__).resolve().parents[2]

# Database path
DATABASE_PATH = BASE_DIR / "data" / "ecommerce.db"

# Connect to database
engine = create_engine(f"sqlite:///{DATABASE_PATH}")


# Monthly revenue
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


# Execute query
with engine.connect() as connection:

    result = connection.execute(text(query))

    for row in result:
        print(row)