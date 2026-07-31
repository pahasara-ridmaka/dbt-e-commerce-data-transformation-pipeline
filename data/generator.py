import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta


# Helper function to create messy strings
def make_messy_string(text: str):
    options = [text, text.upper(), text.lower(), f" {text}", "N/A"]
    return random.choice(options)


# 1. Generate Users data (100 records)
users_data = {
    "user_id": list(range(101, 201)),
    "full_name": [make_messy_string(f"User_{i}") for i in range(100)],
    "email": [f"user{i}@example.com" if i % 10 != 0 else None for i in range(100)],
    "signup_date": [
        (datetime(2023, 1, 1) + timedelta(days=random.randint(0, 365))).strftime(
            "%Y-%m-%d"
        )
        for _ in range(100)
    ],
    "region": [
        random.choice(["North", "South", "East", "West", "north", "WEST"])
        for _ in range(100)
    ],
}

df_users = pd.DataFrame(users_data)
df_users.to_csv("users.csv", index=False)

# 2. Generate Products Data (50 Records)
products_data = {
    "product_id": list(range(501, 551)),
    "product_name": [f"Product_{i}" for i in range(50)],
    "category": [
        random.choice(["Electronics", "Clothing", "Home", "elec", "HOME"])
        for _ in range(50)
    ],
    "price": [random.randint(10, 1000) if i % 5 != 0 else None for i in range(50)],
    "stock_level": [random.randint(0, 100) for _ in range(50)],
}

df_products = pd.DataFrame(products_data)

# Add some duplcate products
df_products = pd.concat([df_products, df_products.iloc[[0, 1, 2]]]).reset_index(
    drop=True
)
df_products.to_csv("products.csv", index=False)

# 3. Generate Orders Data (200 Records)
orders_data = {
    "order_id": list(range(1000, 1200)) + [1000, 1001],  # for duplicates
    "user_id": [random.randint(101, 200) for _ in range(202)],
    "product_id": [random.randint(501, 550) for _ in range(202)],
    "order_date": [
        (datetime(2023, 6, 1) + timedelta(days=random.randint(0, 180))).strftime(
            "%m/%d/%Y"
        )
        for _ in range(202)
    ],
    "quantity": [random.randint(1, 5) for _ in range(202)],
}

df_orders = pd.DataFrame(orders_data)
df_orders.to_csv("orders.csv", index=False)

# 4.  Generate Promotion Data (  20 records)
promo_data = {
    "promo_id": list(range(1, 21)),
    "promo_code": [f"SAVE{i}" for i in range(1, 21)],
    "discount_pct": [random.randint(5, 50) for _ in range(20)],
}

df_promo = pd.DataFrame(promo_data)
df_promo.to_csv("promotions.csv", index=False)

print(
    "Data generation complete. Files created: users.csv, products.csv, promotions.csv"
)
