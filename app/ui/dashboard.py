from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text


# ==========================================
# 1. DATABASE
# ==========================================

BASE_DIR = Path(__file__).resolve().parents[2]

DATABASE_PATH = BASE_DIR / "data" / "ecommerce.db"

engine = create_engine(
    f"sqlite:///{DATABASE_PATH}"
)


# ==========================================
# 2. GET FILTER OPTIONS
# ==========================================

def get_filter_options():

    with engine.connect() as connection:

        years = pd.read_sql(
            text("""
                SELECT DISTINCT
                    strftime('%Y', order_date) AS year
                FROM orders
                ORDER BY year
            """),
            connection
        )["year"].tolist()

        categories = pd.read_sql(
            text("""
                SELECT DISTINCT category
                FROM products
                ORDER BY category
            """),
            connection
        )["category"].tolist()

        regions = pd.read_sql(
            text("""
                SELECT DISTINCT region
                FROM customers
                ORDER BY region
            """),
            connection
        )["region"].tolist()

    return years, categories, regions


# ==========================================
# 3. BUILD FILTER CONDITIONS
# ==========================================

def build_filters(
    year="All",
    category="All",
    region="All"
):

    conditions = []

    parameters = {}


    # --------------------------------------
    # Year
    # --------------------------------------

    if year != "All":

        conditions.append(
            "strftime('%Y', o.order_date) = :year"
        )

        parameters["year"] = year


    # --------------------------------------
    # Category
    # --------------------------------------

    if category != "All":

        conditions.append(
            "p.category = :category"
        )

        parameters["category"] = category


    # --------------------------------------
    # Region
    # --------------------------------------

    if region != "All":

        conditions.append(
            "c.region = :region"
        )

        parameters["region"] = region


    if conditions:

        where_clause = (
            "WHERE "
            + " AND ".join(conditions)
        )

    else:

        where_clause = ""


    return where_clause, parameters


# ==========================================
# 4. DASHBOARD METRICS
# ==========================================

def get_dashboard_metrics(
    year="All",
    category="All",
    region="All"
):

    where_clause, parameters = build_filters(
        year,
        category,
        region
    )


    query = f"""
        SELECT

            COALESCE(
                SUM(
                    o.quantity * p.price
                ),
                0
            ) AS total_revenue,

            COUNT(
                DISTINCT o.order_id
            ) AS total_orders,

            COUNT(
                DISTINCT o.customer_id
            ) AS total_customers,

            COUNT(
                DISTINCT o.product_id
            ) AS total_products

        FROM orders o

        JOIN products p
            ON o.product_id = p.product_id

        JOIN customers c
            ON o.customer_id = c.customer_id

        {where_clause}
    """


    with engine.connect() as connection:

        result = pd.read_sql(
            text(query),
            connection,
            params=parameters
        )


    row = result.iloc[0]


    return {
        "total_revenue": float(
            row["total_revenue"]
        ),

        "total_orders": int(
            row["total_orders"]
        ),

        "total_customers": int(
            row["total_customers"]
        ),

        "total_products": int(
            row["total_products"]
        )
    }


# ==========================================
# 5. FILTERED REVENUE BY CATEGORY
# ==========================================

def get_revenue_by_category(
    year="All",
    category="All",
    region="All"
):

    where_clause, parameters = build_filters(
        year,
        category,
        region
    )


    query = f"""
        SELECT
            p.category,
            SUM(
                o.quantity * p.price
            ) AS revenue

        FROM orders o

        JOIN products p
            ON o.product_id = p.product_id

        JOIN customers c
            ON o.customer_id = c.customer_id

        {where_clause}

        GROUP BY p.category

        ORDER BY revenue DESC
    """


    with engine.connect() as connection:

        return pd.read_sql(
            text(query),
            connection,
            params=parameters
        )


# ==========================================
# 6. FILTERED MONTHLY REVENUE
# ==========================================

def get_monthly_revenue(
    year="All",
    category="All",
    region="All"
):

    where_clause, parameters = build_filters(
        year,
        category,
        region
    )


    query = f"""
        SELECT

            strftime(
                '%Y-%m',
                o.order_date
            ) AS month,

            SUM(
                o.quantity * p.price
            ) AS revenue

        FROM orders o

        JOIN products p
            ON o.product_id = p.product_id

        JOIN customers c
            ON o.customer_id = c.customer_id

        {where_clause}

        GROUP BY month

        ORDER BY month
    """


    with engine.connect() as connection:

        return pd.read_sql(
            text(query),
            connection,
            params=parameters
        )