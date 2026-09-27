import pandas as pd
import mysql.connector

# -----------------------------------------
# 1. Load CSV
# -----------------------------------------

csv_path = r"D:\Customer_360_Churn_Platform\02_Raw_Data\support_tickets.csv"

df = pd.read_csv(csv_path)

print("CSV loaded successfully")
print("Total CSV rows:", len(df))


# -----------------------------------------
# 2. Connect to MySQL
# -----------------------------------------

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=input("Enter MySQL password: "),
    database="novamart"
)

cursor = conn.cursor()

print("MySQL connected successfully")


# -----------------------------------------
# 3. Check valid customers
# -----------------------------------------

cursor.execute("SELECT customer_id FROM customers")

valid_customer_ids = {
    row[0] for row in cursor.fetchall()
}

print("Valid customers in MySQL:", len(valid_customer_ids))


# -----------------------------------------
# 4. Keep only valid customer records
# -----------------------------------------

df_valid = df[
    df["customer_id"].isin(valid_customer_ids)
].copy()

print("Valid support tickets:", len(df_valid))
print(
    "Skipped invalid tickets:",
    len(df) - len(df_valid)
)


# -----------------------------------------
# 5. Rename status column
# -----------------------------------------

df_valid = df_valid.rename(
    columns={
        "status": "resolution_status"
    }
)


# -----------------------------------------
# 6. Create Customer Satisfaction Score
# -----------------------------------------

import numpy as np

np.random.seed(42)

df_valid["customer_satisfaction_score"] = np.random.randint(
    1,
    6,
    size=len(df_valid)
)


# -----------------------------------------
# 7. Insert into MySQL
# -----------------------------------------

insert_query = """
INSERT INTO support_tickets
(
    ticket_id,
    customer_id,
    ticket_date,
    issue_type,
    priority,
    resolution_status,
    customer_satisfaction_score
)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""


data = list(
    df_valid[
        [
            "ticket_id",
            "customer_id",
            "ticket_date",
            "issue_type",
            "priority",
            "resolution_status",
            "customer_satisfaction_score"
        ]
    ].itertuples(
        index=False,
        name=None
    )
)


# -----------------------------------------
# 8. Batch Insert
# -----------------------------------------

batch_size = 5000

for start in range(
    0,
    len(data),
    batch_size
):

    batch = data[
        start:start + batch_size
    ]

    cursor.executemany(
        insert_query,
        batch
    )

    conn.commit()

    print(
        f"Inserted {min(start + batch_size, len(data))} / {len(data)} rows"
    )


# -----------------------------------------
# 9. Close connection
# -----------------------------------------

cursor.close()
conn.close()

print()
print("Support Tickets import completed successfully!")