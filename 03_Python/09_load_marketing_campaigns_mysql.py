import pandas as pd
import mysql.connector

# =========================================
# 1. LOAD CSV
# =========================================

csv_path = r"D:\Customer_360_Churn_Platform\02_Raw_Data\marketing_campaigns.csv"

df = pd.read_csv(csv_path)

print("CSV loaded successfully")
print("Total CSV rows:", len(df))

print("\nOriginal CSV columns:")
print(df.columns.tolist())


# =========================================
# 2. CONNECT TO MYSQL
# =========================================

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=input("Enter MySQL password: "),
    database="novamart"
)

cursor = conn.cursor()

print("\nMySQL connected successfully")


# =========================================
# 3. RENAME CSV COLUMNS
# =========================================

df = df.rename(columns={
    "channel": "marketing_channel",
    "budget": "campaign_budget"
})


# =========================================
# 4. CREATE CAMPAIGN TYPE
# =========================================
# CSV does not contain campaign_type.
# We derive it from the marketing channel.

channel_to_type = {
    "Email": "Retention",
    "SMS": "Retention",
    "Social Media": "Acquisition",
    "Google Ads": "Acquisition",
    "Push Notification": "Engagement",
    "Website": "Engagement",
    "Referral": "Acquisition",
    "Display Ads": "Acquisition"
}

df["campaign_type"] = (
    df["marketing_channel"]
    .map(channel_to_type)
    .fillna("General")
)


# =========================================
# 5. SHOW FINAL COLUMNS
# =========================================

print("\nFinal CSV columns:")
print(df.columns.tolist())


# =========================================
# 6. REQUIRED COLUMNS
# =========================================

required_columns = [
    "campaign_id",
    "campaign_name",
    "campaign_type",
    "start_date",
    "end_date",
    "marketing_channel",
    "campaign_budget"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:

    print("\nERROR - Missing columns:")
    print(missing_columns)

    cursor.close()
    conn.close()

    raise SystemExit(
        "Required columns are missing."
    )


# =========================================
# 7. SELECT REQUIRED COLUMNS
# =========================================

df = df[required_columns].copy()


# =========================================
# 8. CLEAN DATA TYPES
# =========================================

df["campaign_id"] = pd.to_numeric(
    df["campaign_id"],
    errors="coerce"
)

df["campaign_budget"] = pd.to_numeric(
    df["campaign_budget"],
    errors="coerce"
)

df["start_date"] = pd.to_datetime(
    df["start_date"],
    errors="coerce"
).dt.date

df["end_date"] = pd.to_datetime(
    df["end_date"],
    errors="coerce"
).dt.date


# =========================================
# 9. REMOVE INVALID ROWS
# =========================================

before_cleaning = len(df)

df = df.dropna(
    subset=required_columns
)

df = df.drop_duplicates(
    subset=["campaign_id"]
)

print("\nRows after cleaning:", len(df))

print(
    "Removed invalid/duplicate rows:",
    before_cleaning - len(df)
)


# =========================================
# 10. CHECK EXISTING CAMPAIGN IDs
# =========================================

cursor.execute(
    "SELECT campaign_id FROM marketing_campaigns"
)

existing_ids = {
    row[0]
    for row in cursor.fetchall()
}

df_valid = df[
    ~df["campaign_id"].isin(existing_ids)
].copy()

print(
    "New campaign records to insert:",
    len(df_valid)
)


# =========================================
# 11. INSERT QUERY
# =========================================

insert_query = """
INSERT INTO marketing_campaigns
(
    campaign_id,
    campaign_name,
    campaign_type,
    start_date,
    end_date,
    marketing_channel,
    campaign_budget
)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""


# =========================================
# 12. PREPARE DATA
# =========================================

data = list(
    df_valid[
        [
            "campaign_id",
            "campaign_name",
            "campaign_type",
            "start_date",
            "end_date",
            "marketing_channel",
            "campaign_budget"
        ]
    ].itertuples(
        index=False,
        name=None
    )
)


# =========================================
# 13. BATCH INSERT
# =========================================

batch_size = 5000
total_rows = len(data)

for start in range(
    0,
    total_rows,
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

    inserted = min(
        start + batch_size,
        total_rows
    )

    print(
        f"Inserted {inserted} / {total_rows} rows"
    )


# =========================================
# 14. VERIFY
# =========================================

cursor.execute(
    "SELECT COUNT(*) FROM marketing_campaigns"
)

final_count = cursor.fetchone()[0]

print(
    "\nMarketing campaigns in MySQL:",
    final_count
)


# =========================================
# 15. CLOSE CONNECTION
# =========================================

cursor.close()
conn.close()

print(
    "\nMarketing Campaigns import completed successfully!"
)