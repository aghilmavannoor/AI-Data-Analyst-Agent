import sys
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text


# ==========================================
# 1. MAKE APP DIRECTORY AVAILABLE
# ==========================================

APP_DIR = Path(__file__).resolve().parents[1]

sys.path.insert(0, str(APP_DIR))


# ==========================================
# 2. IMPORT
# ==========================================

from agent.llm import ask_llm
from database.schema import get_database_schema


# ==========================================
# 3. DATABASE PATH
# ==========================================

BASE_DIR = Path(__file__).resolve().parents[2]

DATABASE_PATH = BASE_DIR / "data" / "ecommerce.db"


# ==========================================
# 4. DATABASE CONNECTION
# ==========================================

engine = create_engine(
    f"sqlite:///{DATABASE_PATH}"
)


# ==========================================
# 5. GET DATABASE SCHEMA
# ==========================================

schema = get_database_schema()

schema_text = ""

for table, columns in schema.items():

    schema_text += f"\nTable: {table}\n"

    for column in columns:

        schema_text += f"- {column}\n"


# ==========================================
# 6. GENERATE SQL
# ==========================================

def generate_sql(question):

    prompt = f"""
You are an expert SQLite data analyst.

Your job is to convert the user's natural-language
question into ONE correct SQLite SELECT query.

All monetary values are in Indian Rupees (INR).

DATABASE SCHEMA:
{schema_text}

BUSINESS RULE:
Revenue = orders.quantity * products.price


IMPORTANT SQL RULES:

1. Return ONLY one SQLite SELECT statement.
2. Never return markdown.
3. Never explain the query.
4. Never use INSERT, UPDATE, DELETE, DROP, ALTER, CREATE,
   REPLACE, TRUNCATE, or other database-modifying commands.
5. Use ONLY tables and columns from the schema.
6. Revenue MUST be calculated as:
   orders.quantity * products.price
7. Always use the correct JOIN when data comes from
   multiple tables.
8. IMPORTANT: Preserve EVERY filter mentioned in the
   user's question.
9. If the user specifies a product, category, customer,
   city, state, region, month, year, or date range,
   the SQL MUST contain the corresponding WHERE condition.
10. Do NOT remove or ignore a filter just because it is
    not required to calculate the aggregation.
11. For monthly trends, group by:
    strftime('%Y-%m', orders.order_date)
12. For monthly trends, order results chronologically.
13. For "highest" or "top" results, use:
    ORDER BY <value> DESC
14. For "lowest" results, use:
    ORDER BY <value> ASC
15. If the question asks for one highest result,
    use LIMIT 1.
16. Do not invent products, categories, customers,
    columns, or tables.


IMPORTANT CATEGORY RULE:

The database contains these exact category values:

- Laptop
- Smartphone
- Tablet
- Accessories
- Audio
- Wearable
- Storage
- Networking
- Office

When filtering by category, use a CASE-INSENSITIVE
comparison so that lowercase or uppercase wording
from the user does not cause an empty result.

Use this pattern:

LOWER(products.category) = LOWER('Laptop')

For example, if the user asks:

Show revenue for Laptop.

Use:

WHERE LOWER(products.category) = LOWER('Laptop')

NOT:

WHERE products.category = 'laptop'


IMPORTANT REGION RULE:

When filtering by region, use a case-insensitive
comparison as well.

Use:

LOWER(customers.region) = LOWER('North')


IMPORTANT FILTER COMBINATION:

If multiple filters are mentioned, ALL filters must
be included.

For example:

Show Laptop revenue for 2025.

Generate a query containing BOTH:

LOWER(products.category) = LOWER('Laptop')

AND:

strftime('%Y', orders.order_date) = '2025'


IMPORTANT EXAMPLES:


If the question is:

Show revenue by category.

Generate:

SELECT
    products.category,
    SUM(orders.quantity * products.price) AS revenue
FROM orders
JOIN products
    ON orders.product_id = products.product_id
GROUP BY products.category;


If the question is:

Show monthly revenue for the Laptop category.

Generate:

SELECT
    strftime('%Y-%m', orders.order_date) AS month,
    SUM(orders.quantity * products.price) AS revenue
FROM orders
JOIN products
    ON orders.product_id = products.product_id
WHERE LOWER(products.category) = LOWER('Laptop')
GROUP BY month
ORDER BY month;


If the question is:

Show monthly revenue for the Smartphone category.

Generate:

SELECT
    strftime('%Y-%m', orders.order_date) AS month,
    SUM(orders.quantity * products.price) AS revenue
FROM orders
JOIN products
    ON orders.product_id = products.product_id
WHERE LOWER(products.category) = LOWER('Smartphone')
GROUP BY month
ORDER BY month;


If the question is:

Show Laptop revenue for 2025.

Generate:

SELECT
    products.category,
    SUM(orders.quantity * products.price) AS revenue
FROM orders
JOIN products
    ON orders.product_id = products.product_id
WHERE LOWER(products.category) = LOWER('Laptop')
    AND strftime('%Y', orders.order_date) = '2025'
GROUP BY products.category;


If the question is:

Which product generated the highest revenue?

Generate:

SELECT
    products.product_name,
    SUM(orders.quantity * products.price) AS revenue
FROM orders
JOIN products
    ON orders.product_id = products.product_id
GROUP BY products.product_id, products.product_name
ORDER BY revenue DESC
LIMIT 1;


If the question is:

What is the average product price?

Generate:

SELECT
    AVG(products.price) AS average_price
FROM products;


USER QUESTION:

{question}


FINAL REQUIREMENT:

The user's filters are mandatory.

Do not remove any filter.

Return ONLY the SQL query.
"""

    sql = ask_llm(prompt)

    # ------------------------------------------
    # Remove markdown fences if Qwen adds them
    # ------------------------------------------

    sql = sql.strip()

    sql = sql.replace(
        "```sql",
        ""
    )

    sql = sql.replace(
        "```",
        ""
    )

    sql = sql.strip()

    return sql
# ==========================================
# 7. VALIDATE SQL
# ==========================================

def validate_sql(sql):

    if not sql:

        raise ValueError(
            "Empty SQL query generated."
        )

    sql_lower = sql.strip().lower()

    # ------------------------------------------
    # Only SELECT statements
    # ------------------------------------------

    if not sql_lower.startswith("select"):

        raise ValueError(
            "Only SELECT queries are allowed."
        )

    # ------------------------------------------
    # Forbidden operations
    # ------------------------------------------

    forbidden_keywords = [
        "insert",
        "update",
        "delete",
        "drop",
        "alter",
        "create",
        "replace",
        "truncate",
        "attach",
        "detach",
        "pragma"
    ]

    for keyword in forbidden_keywords:

        if keyword in sql_lower:

            raise ValueError(
                f"Unsafe SQL detected: {keyword}"
            )

    return True


# ==========================================
# 8. EXECUTE SQL
# ==========================================

def execute_sql(sql):

    with engine.connect() as connection:

        dataframe = pd.read_sql(
            text(sql),
            connection
        )

    return dataframe


# ==========================================
# 9. COMPLETE ANALYSIS
# ==========================================

def analyze_question(question):

    # ------------------------------------------
    # Generate SQL
    # ------------------------------------------

    sql = generate_sql(
        question
    )

    # ------------------------------------------
    # Validate SQL
    # ------------------------------------------

    validate_sql(
        sql
    )

    # ------------------------------------------
    # Execute SQL
    # ------------------------------------------

    result = execute_sql(
        sql
    )

    return sql, result


# ==========================================
# 10. TEST
# ==========================================

if __name__ == "__main__":

    question = input(
        "\nAsk a question about the sales data: "
    )

    print(
        "\nAnalyzing..."
    )

    try:

        sql, result = analyze_question(
            question
        )

        print(
            "\n" + "=" * 60
        )

        print(
            "\nGenerated SQL:"
        )

        print(sql)

        print(
            "\n" + "=" * 60
        )

        print(
            "\nQuery Result:"
        )

        print(result)

        print(
            "\n" + "=" * 60
        )

    except Exception as e:

        print(
            "\nSQL Error:"
        )

        print(e)

        print(
            "\n" + "=" * 60
        )