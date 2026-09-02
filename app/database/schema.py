from sqlalchemy import create_engine, inspect
from pathlib import Path


# ==========================================
# 1. PROJECT PATH
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
# 3. GET DATABASE SCHEMA
# ==========================================

def get_database_schema():

    inspector = inspect(engine)

    tables = inspector.get_table_names()

    schema = {}

    for table in tables:

        columns = inspector.get_columns(table)

        schema[table] = [
            column["name"]
            for column in columns
        ]

    return schema


# ==========================================
# 4. TEST
# ==========================================

if __name__ == "__main__":

    schema = get_database_schema()

    print("\nDatabase Schema:\n")

    for table, columns in schema.items():

        print(f"Table: {table}")

        for column in columns:
            print(f"  - {column}")

        print()