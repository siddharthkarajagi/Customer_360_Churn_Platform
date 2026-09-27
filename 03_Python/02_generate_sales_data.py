import pandas as pd
import numpy as np

# ============================================================
# NOVAMART - PRODUCTS, STORES, ORDERS & ORDER ITEMS
# ============================================================

np.random.seed(42)

# ------------------------------------------------------------
# 1. PRODUCTS
# ------------------------------------------------------------

NUMBER_OF_PRODUCTS = 5000

categories = [
    "Electronics",
    "Fashion",
    "Home & Kitchen",
    "Beauty",
    "Grocery",
    "Sports",
    "Books",
    "Toys"
]

brands = [
    "NovaTech",
    "UrbanStyle",
    "HomePro",
    "FreshMart",
    "FitLife",
    "SmartBuy",
    "DailyNeeds",
    "PrimeChoice"
]

product_names = [
    "Smartphone",
    "Laptop",
    "Headphones",
    "Smart Watch",
    "T-Shirt",
    "Jeans",
    "Sneakers",
    "Backpack",
    "Mixer Grinder",
    "Coffee Maker",
    "Face Wash",
    "Shampoo",
    "Protein Bar",
    "Running Shoes",
    "Notebook",
    "Action Camera",
    "Bluetooth Speaker",
    "Desk Lamp",
    "Water Bottle",
    "Gaming Mouse"
]

products = pd.DataFrame({
    "product_id": np.arange(1, NUMBER_OF_PRODUCTS + 1),

    "product_name": [
        f"{np.random.choice(product_names)} {i}"
        for i in range(1, NUMBER_OF_PRODUCTS + 1)
    ],

    "category": np.random.choice(
        categories,
        NUMBER_OF_PRODUCTS
    ),

    "brand": np.random.choice(
        brands,
        NUMBER_OF_PRODUCTS
    ),

    "cost_price": np.round(
        np.random.uniform(100, 50000, NUMBER_OF_PRODUCTS),
        2
    )
})

# Selling price is higher than cost price
products["selling_price"] = np.round(
    products["cost_price"] * np.random.uniform(
        1.10, 1.50, NUMBER_OF_PRODUCTS
    ),
    2
)
products.to_csv(
    "../02_Raw_Data/products.csv",
    index=False
)

print("Products created:", len(products))


# ------------------------------------------------------------
# 2. STORES
# ------------------------------------------------------------

NUMBER_OF_STORES = 20

store_cities = [
    "Mumbai",
    "Pune",
    "Nashik",
    "Nagpur",
    "Solapur",
    "Kolhapur",
    "Thane",
    "Navi Mumbai",
    "Satara",
    "Aurangabad"
]

stores = pd.DataFrame({
    "store_id": np.arange(1, NUMBER_OF_STORES + 1),

    "store_name": [
        f"NovaMart Store {i}"
        for i in range(1, NUMBER_OF_STORES + 1)
    ],

    "city": np.random.choice(
        store_cities,
        NUMBER_OF_STORES
    ),

    "state": "Maharashtra",

    "store_type": np.random.choice(
        ["Mall", "High Street", "Neighborhood"],
        NUMBER_OF_STORES
    )
})

stores.to_csv(
    "../02_Raw_Data/stores.csv",
    index=False
)

print("Stores created:", len(stores))


# ------------------------------------------------------------
# 3. LOAD CUSTOMERS
# ------------------------------------------------------------

customers = pd.read_csv(
    "../02_Raw_Data/customers.csv"
)

customers["registration_date"] = pd.to_datetime(
    customers["registration_date"]
)

print("Customers loaded:", len(customers))


# ------------------------------------------------------------
# 4. ORDERS
# ------------------------------------------------------------

NUMBER_OF_ORDERS = 100000

# Generate order dates
order_dates = pd.to_datetime(
    np.random.randint(
        pd.Timestamp("2025-01-01").value // 10**9,
        pd.Timestamp("2026-08-31").value // 10**9,
        NUMBER_OF_ORDERS
    ),
    unit="s"
)

# Random customer IDs
order_customer_ids = np.random.choice(
    customers["customer_id"],
    NUMBER_OF_ORDERS
)

# Random stores
order_store_ids = np.random.randint(
    1,
    NUMBER_OF_STORES + 1,
    NUMBER_OF_ORDERS
)

# Sales channel
channels = np.random.choice(
    ["Website", "Mobile App", "Store"],
    NUMBER_OF_ORDERS,
    p=[0.45, 0.30, 0.25]
)

# Order status
order_statuses = np.random.choice(
    ["Completed", "Cancelled", "Processing"],
    NUMBER_OF_ORDERS,
    p=[0.86, 0.08, 0.06]
)

orders = pd.DataFrame({
    "order_id": np.arange(
        1,
        NUMBER_OF_ORDERS + 1
    ),

    "customer_id": order_customer_ids,

    "store_id": order_store_ids,

    "order_date": order_dates,

    "channel": channels,

    "order_status": order_statuses
})


# ------------------------------------------------------------
# 5. ORDER ITEMS
# ------------------------------------------------------------

items_per_order = np.random.choice(
    [1, 2, 3, 4, 5],
    NUMBER_OF_ORDERS,
    p=[0.35, 0.30, 0.20, 0.10, 0.05]
)

total_items = items_per_order.sum()

order_item_order_ids = np.repeat(
    orders["order_id"].values,
    items_per_order
)

order_item_ids = np.arange(
    1,
    total_items + 1
)

product_ids = np.random.randint(
    1,
    NUMBER_OF_PRODUCTS + 1,
    total_items
)

quantities = np.random.choice(
    [1, 2, 3, 4],
    total_items,
    p=[0.65, 0.22, 0.10, 0.03]
)

# Get product prices
product_price_map = products.set_index(
    "product_id"
)["selling_price"]

unit_prices = product_price_map.loc[
    product_ids
].values

discounts = np.round(
    np.random.uniform(0, 30, total_items),
    2
)

order_items = pd.DataFrame({
    "order_item_id": order_item_ids,

    "order_id": order_item_order_ids,

    "product_id": product_ids,

    "quantity": quantities,

    "unit_price": unit_prices,

    "discount": discounts
})


# ------------------------------------------------------------
# 6. CALCULATE ORDER TOTAL
# ------------------------------------------------------------

order_items["item_total"] = (
    order_items["quantity"]
    * order_items["unit_price"]
    * (1 - order_items["discount"] / 100)
)

order_totals = (
    order_items
    .groupby("order_id")["item_total"]
    .sum()
    .round(2)
)

orders["total_amount"] = (
    orders["order_id"]
    .map(order_totals)
    .fillna(0)
)


# ------------------------------------------------------------
# 7. SAVE ORDERS
# ------------------------------------------------------------

orders.to_csv(
    "../02_Raw_Data/orders.csv",
    index=False
)

order_items.to_csv(
    "../02_Raw_Data/order_items.csv",
    index=False
)


# ------------------------------------------------------------
# 8. SUMMARY
# ------------------------------------------------------------

print("\n====================================")
print("NOVAMART SALES DATA CREATED")
print("====================================")

print("Products:", len(products))
print("Stores:", len(stores))
print("Orders:", len(orders))
print("Order Items:", len(order_items))

print("\nOrder Status:")
print(orders["order_status"].value_counts())

print("\nSales Channel:")
print(orders["channel"].value_counts())

print("\nTotal Sales Value:")
print(
    round(
        orders["total_amount"].sum(),
        2
    )
)

print("\nSample Orders:")
print(
    orders.head()
)

print("\nData generation completed successfully!")
