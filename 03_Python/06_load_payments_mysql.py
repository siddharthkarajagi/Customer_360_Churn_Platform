import pandas as pd
import mysql.connector

csv_path = r"D:\Customer_360_Churn_Platform\02_Raw_Data\payments.csv"

df = pd.read_csv(csv_path)

print("CSV loaded successfully")
print("Total payment rows:", len(df))

# Rename CSV column
df = df.rename(columns={
    "amount": "payment_amount"
})

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=input("Enter MySQL password: "),
    database="novamart"
)

cursor = conn.cursor()

print("MySQL connected successfully")

# Get valid orders
cursor.execute("SELECT order_id FROM orders")
valid_order_ids = {row[0] for row in cursor.fetchall()}

# Keep only payments linked to existing orders
df_valid = df[df["order_id"].isin(valid_order_ids)].copy()

print("Valid payment rows:", len(df_valid))
print("Skipped invalid rows:", len(df) - len(df_valid))

insert_query = """
INSERT INTO payments
(
    payment_id,
    order_id,
    customer_id,
    payment_date,
    payment_method,
    payment_amount,
    payment_status
)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

data = list(
    df_valid[
        [
            "payment_id",
            "order_id",
            "customer_id",
            "payment_date",
            "payment_method",
            "payment_amount",
            "payment_status"
        ]
    ].itertuples(index=False, name=None)
)

batch_size = 5000

for start in range(0, len(data), batch_size):
    batch = data[start:start + batch_size]

    cursor.executemany(insert_query, batch)
    conn.commit()

    print(
        f"Inserted {min(start + batch_size, len(data))} / {len(data)} rows"
    )

cursor.close()
conn.close()

print("Payments import completed successfully!")