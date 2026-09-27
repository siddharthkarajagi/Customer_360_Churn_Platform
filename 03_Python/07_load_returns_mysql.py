import pandas as pd
import mysql.connector

csv_path = r"D:\Customer_360_Churn_Platform\02_Raw_Data\returns.csv"

# Load CSV
df = pd.read_csv(csv_path)

print("CSV loaded successfully")
print("Total return rows:", len(df))
print("CSV columns:", list(df.columns))

# Find amount column automatically
amount_columns = [
    "return_amount",
    "refund_amount",
    "amount",
    "refund",
    "return_value"
]

amount_col = next(
    (col for col in amount_columns if col in df.columns),
    None
)

if amount_col is None:
    raise ValueError(
        "Amount column not found in returns.csv"
    )

df["return_amount"] = df[amount_col]

# MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=input("Enter MySQL password: "),
    database="novamart"
)

cursor = conn.cursor()

print("MySQL connected successfully")

# Valid IDs
cursor.execute("SELECT order_id FROM orders")
valid_orders = {row[0] for row in cursor.fetchall()}

cursor.execute("SELECT customer_id FROM customers")
valid_customers = {row[0] for row in cursor.fetchall()}

cursor.execute("SELECT product_id FROM products")
valid_products = {row[0] for row in cursor.fetchall()}

# Keep valid records only
df_valid = df[
    df["order_id"].isin(valid_orders) &
    df["customer_id"].isin(valid_customers) &
    df["product_id"].isin(valid_products)
].copy()

print("Valid return rows:", len(df_valid))
print("Skipped invalid rows:", len(df) - len(df_valid))

# Insert
insert_query = """
INSERT INTO returns
(
    return_id,
    order_id,
    customer_id,
    product_id,
    return_date,
    return_reason,
    return_amount,
    return_status
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

data = list(
    df_valid[
        [
            "return_id",
            "order_id",
            "customer_id",
            "product_id",
            "return_date",
            "return_reason",
            "return_amount",
            "return_status"
        ]
    ].itertuples(index=False, name=None)
)

# Batch insert
batch_size = 1000

for start in range(0, len(data), batch_size):

    batch = data[start:start + batch_size]

    cursor.executemany(insert_query, batch)
    conn.commit()

    print(
        f"Inserted {min(start + batch_size, len(data))} / {len(data)} rows"
    )

cursor.close()
conn.close()

print("Returns import completed successfully!")