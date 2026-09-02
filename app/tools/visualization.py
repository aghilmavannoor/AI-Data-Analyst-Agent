import pandas as pd
import plotly.express as px

from sqlalchemy import create_engine, text
from pathlib import Path


# ==========================================
# 1. PROJECT PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parents[2]

DATABASE_PATH = BASE_DIR / "data" / "ecommerce.db"


# ==========================================
# 2. DATABASE CONNECTION
# ==========================================

engine = create_engine(
    f"sqlite:///{DATABASE_PATH}"
)


# ==========================================
# 3. RUN SQL QUERY
# ==========================================

def run_query(query):
    """
    Execute a SQL query and return
    the result as a Pandas DataFrame.
    """

    with engine.connect() as connection:

        dataframe = pd.read_sql(
            text(query),
            connection
        )

    return dataframe


# ==========================================
# 4. CREATE BAR CHART
# ==========================================

def create_bar_chart(
    df,
    x_column,
    y_column,
    title
):
    """
    Create an interactive Plotly bar chart.
    """

    fig = px.bar(
        df,
        x=x_column,
        y=y_column,
        title=title
    )

    return fig


# ==========================================
# 5. SQL QUERY
# ==========================================

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


# ==========================================
# 6. RUN QUERY
# ==========================================

df = run_query(query)


# ==========================================
# 7. DISPLAY DATA
# ==========================================

print("\nRevenue by Category:")
print(df)


# ==========================================
# 8. CREATE CHART
# ==========================================

fig = create_bar_chart(
    df,
    "category",
    "total_revenue",
    "Revenue by Category"
)


# ==========================================
# 9. DISPLAY CHART
# ==========================================

fig.show()