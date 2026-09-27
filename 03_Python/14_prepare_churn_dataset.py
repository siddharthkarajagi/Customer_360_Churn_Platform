import pandas as pd
import numpy as np

# ============================================================
# STEP 14 - CREATE CHURN DATASET
# ============================================================

input_file = r"D:\Customer_360_Churn_Platform\02_Raw_Data\customer_360_rfm.csv"

output_file = r"D:\Customer_360_Churn_Platform\02_Raw_Data\customer_360_rfm_churn.csv"

print("Loading RFM dataset...")

df = pd.read_csv(input_file)

print("Rows:", len(df))
print("Columns:", len(df.columns))

# ============================================================
# REQUIRED COLUMNS
# ============================================================

required_columns = [
    "customer_id",
    "days_since_last_order",
    "total_orders",
    "customer_tenure_days"
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:
    print("\nERROR!")
    print("Missing columns:")
    print(missing_columns)
    raise SystemExit

# ============================================================
# CREATE CHURN FLAG
# ============================================================

df["churn_flag"] = np.where(
    (
        df["days_since_last_order"] > 90
    )
    |
    (
        (df["total_orders"] <= 1)
        &
        (df["customer_tenure_days"] > 90)
    ),
    1,
    0
)

# ============================================================
# CREATE CHURN LABEL
# ============================================================

df["churn_label"] = np.where(
    df["churn_flag"] == 1,
    "Churn",
    "Active"
)

# ============================================================
# CHURN DISTRIBUTION
# ============================================================

print("\n==============================")
print("CHURN DISTRIBUTION")
print("==============================")

print(
    df["churn_label"].value_counts()
)

# ============================================================
# CHURN FLAG DISTRIBUTION
# ============================================================

print("\n==============================")
print("CHURN FLAG DISTRIBUTION")
print("==============================")

print(
    df["churn_flag"].value_counts()
)

# ============================================================
# QUALITY CHECK
# ============================================================

print("\n==============================")
print("QUALITY CHECK")
print("==============================")

print(
    "Duplicate customers:",
    df["customer_id"].duplicated().sum()
)

print(
    "Missing churn labels:",
    df["churn_label"].isnull().sum()
)

print(
    "Missing churn flags:",
    df["churn_flag"].isnull().sum()
)

# ============================================================
# SAVE
# ============================================================

df.to_csv(
    output_file,
    index=False
)

print("\n===================================")
print("CHURN DATASET CREATED SUCCESSFULLY")
print("===================================")

print("\nSaved file:")
print(output_file)