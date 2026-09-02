import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from pathlib import Path


# -----------------------------
# 1. Project paths
# -----------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DATABASE_PATH = DATA_DIR / "ecommerce.db"


# -----------------------------
# 2. Create sample customers
# -----------------------------

customers = pd.DataFrame({
    "customer_id": range(1, 101),
    "customer_name": [f"Customer_{i}" for i in range(1, 101)],
    "city": np.random.choice(
        ["Kochi", "Mumbai", "Delhi", "Bangalore", "Chennai",
         "Hyderabad", "Pune", "Kolkata"],
        100
    ),
    "state": np.random.choice(
        ["Kerala", "Maharashtra", "Delhi", "Karnataka",
         "Tamil Nadu", "Telangana", "West Bengal"],
        100
    ),
    "region": np.random.choice(
        ["North", "South", "East", "West"],
        100
    )
})


# -----------------------------
# 3. Create products
# -----------------------------

products = pd.DataFrame({
    "product_id": range(1, 21),
    "product_name": [
        "Laptop Pro",
        "Laptop Air",
        "Gaming Laptop",
        "Smartphone X",
        "Smartphone Pro",
        "Tablet",
        "Wireless Mouse",
        "Mechanical Keyboard",
        "Monitor",
        "Webcam",
        "Headphones",
        "Smart Watch",
        "Power Bank",
        "USB-C Hub",
        "External SSD",
        "Printer",
        "Office Chair",
        "Desk Lamp",
        "Router",
        "Bluetooth Speaker"
    ],
    "category": [
        "Laptop",
        "Laptop",
        "Laptop",
        "Smartphone",
        "Smartphone",
        "Tablet",
        "Accessories",
        "Accessories",
        "Accessories",
        "Accessories",
        "Audio",
        "Wearable",
        "Accessories",
        "Accessories",
        "Storage",
        "Office",
        "Office",
        "Office",
        "Networking",
        "Audio"
    ],
    "price": [
        75000,
        65000,
        95000,
        45000,
        55000,
        30000,
        1500,
        4500,
        18000,
        5000,
        8000,
        12000,
        2500,
        3500,
        9000,
        15000,
        12000,
        3000,
        6000,
        7000
    ]
})


# -----------------------------
# 4. Create orders
# -----------------------------

np.random.seed(42)

num_orders = 5000

orders = pd.DataFrame({
    "order_id": range(1, num_orders + 1),

    "customer_id": np.random.randint(
        1, 101, num_orders
    ),

    "product_id": np.random.randint(
        1, 21, num_orders
    ),

    "order_date": pd.to_datetime(
        np.random.choice(
            pd.date_range(
                start="2025-01-01",
                end="2026-08-28"
            ),
            num_orders
        )
    ),

    "quantity": np.random.randint(
        1, 6, num_orders
    )
})


# -----------------------------
# 5. Connect to SQLite
# -----------------------------

engine = create_engine(
    f"sqlite:///{DATABASE_PATH}"
)


# -----------------------------
# 6. Save tables
# -----------------------------

customers.to_sql(
    "customers",
    engine,
    if_exists="replace",
    index=False
)

products.to_sql(
    "products",
    engine,
    if_exists="replace",
    index=False
)

orders.to_sql(
    "orders",
    engine,
    if_exists="replace",
    index=False
)


# -----------------------------
# 7. Confirmation
# -----------------------------

print("Database created successfully!")
print(f"Database location: {DATABASE_PATH}")

print("\nCustomers:", len(customers))
print("Products:", len(products))
print("Orders:", len(orders))