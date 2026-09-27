import pandas as pd
import mysql.connector

csv_path = r"D:\Customer_360_Churn_Platform\02_Raw_Data\customer_campaigns.csv"

df = pd.read_csv(csv_path)

print("CSV loaded successfully")
print("Total rows:", len(df))

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=input("Enter MySQL password: "),
    database="novamart"
)

cursor = conn.cursor()

print("\nMySQL connected successfully")

# Validate customers
cursor.execute("SELECT customer_id FROM customers")
valid_customers = {row[0] for row in cursor.fetchall()}

# Validate campaigns
cursor.execute("SELECT campaign_id FROM marketing_campaigns")
valid_campaigns = {row[0] for row in cursor.fetchall()}

print("Valid customers in MySQL:", len(valid_customers))
print("Valid campaigns in MySQL:", len(valid_campaigns))

# Keep valid records
df = df[
    df["customer_id"].isin(valid_customers)
    & df["campaign_id"].isin(valid_campaigns)
].copy()

print("Valid customer campaign records:", len(df))

# Convert date
df["sent_date"] = pd.to_datetime(
    df["engagement_date"],
    errors="coerce"
)

# Response mapping
df["opened"] = df["response_status"].isin(
    ["Opened", "Clicked", "Converted"]
).astype(int)

df["clicked"] = df["response_status"].isin(
    ["Clicked", "Converted"]
).astype(int)

df["converted"] = (
    df["response_status"] == "Converted"
).astype(int)

# No conversion amount available in CSV
df["conversion_amount"] = 0.00

# Remove invalid dates
df = df.dropna(subset=["sent_date"])

# Remove duplicate primary IDs
df = df.drop_duplicates(
    subset=["customer_campaign_id"]
)

print("Records after cleaning:", len(df))

# Check existing IDs
cursor.execute(
    "SELECT customer_campaign_id FROM customer_campaigns"
)

existing_ids = {row[0] for row in cursor.fetchall()}

df = df[
    ~df["customer_campaign_id"].isin(existing_ids)
].copy()

print("New customer campaign records to insert:", len(df))

# Insert
insert_query = """
INSERT INTO customer_campaigns
(
    customer_campaign_id,
    customer_id,
    campaign_id,
    sent_date,
    opened,
    clicked,
    converted,
    conversion_amount
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

data = list(
    df[
        [
            "customer_campaign_id",
            "customer_id",
            "campaign_id",
            "sent_date",
            "opened",
            "clicked",
            "converted",
            "conversion_amount"
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

# Verify
cursor.execute(
    "SELECT COUNT(*) FROM customer_campaigns"
)

count = cursor.fetchone()[0]

print("\nCustomer campaigns in MySQL:", count)

cursor.close()
conn.close()

print("\nCustomer Campaigns import completed successfully!")