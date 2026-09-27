import pandas as pd
import mysql.connector

csv_path = r"D:\Customer_360_Churn_Platform\02_Raw_Data\order_items.csv"

df = pd.read_csv(csv_path)

print("CSV loaded successfully")
print("Total CSV rows:", len(df))

df = df.rename(columns={
    "item_total": "final_amount"
})

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=input("Enter MySQL password: "),
    database="novamart"
)

cursor = conn.cursor()

print("MySQL connected successfully")

# Get valid order IDs from MySQL
cursor.execute("SELECT order_id FROM orders")
valid_order_ids = {row[0] for row in cursor.fetchall()}

print("Valid orders in MySQL:", len(valid_order_ids))

# Keep only order_items whose order_id exists in orders
df_valid = df[df["order_id"].isin(valid_order_ids)].copy()

print("Valid order_items:", len(df_valid))
print("Skipped invalid order_items:", len(df) - len(df_valid))

insert_query = """
INSERT INTO order_items
(
    order_item_id,
    order_id,
    product_id,
    quantity,
    unit_price,
    discount,
    final_amount
)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

batch_size = 5000

data = list(
    df_valid[
        [
            "order_item_id",
            "order_id",
            "product_id",
            "quantity",
            "unit_price",
            "discount",
            "final_amount"
        ]
    ].itertuples(index=False, name=None)
)

for start in range(0, len(data), batch_size):

    batch = data[start:start + batch_size]

    cursor.executemany(insert_query, batch)
    conn.commit()

    print(
        f"Inserted {min(start + batch_size, len(data))} / {len(data)} rows"
    )

cursor.close()
conn.close()

print("Order Items import completed successfully!")