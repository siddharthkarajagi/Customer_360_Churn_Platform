import pandas as pd
import numpy as np

INPUT_PATH = r"D:\Customer_360_Churn_Platform\02_Raw_Data\churn_model_dataset.csv"

df = pd.read_csv(INPUT_PATH)

print("=" * 60)
print("CUSTOMER 360 DATA QUALITY VALIDATION")
print("=" * 60)

print()
print("Rows:", len(df))
print("Columns:", len(df.columns))

# -----------------------------
# DUPLICATES
# -----------------------------

duplicate_customers = df["customer_id"].duplicated().sum()

print()
print("Duplicate customer IDs:", duplicate_customers)

# -----------------------------
# NULLS
# -----------------------------

null_count = df.isnull().sum().sum()

print("Total NULL values:", null_count)

# -----------------------------
# INFINITE VALUES
# -----------------------------

numeric_df = df.select_dtypes(
    include=["number"]
)

infinite_count = np.isinf(
    numeric_df.to_numpy()
).sum()

print("Infinite values:", infinite_count)

# -----------------------------
# NEGATIVE VALUES
# -----------------------------

if "total_revenue" in df.columns:

    negative_revenue = (
        df["total_revenue"] < 0
    ).sum()

    print("Negative revenue records:", negative_revenue)

# -----------------------------
# CHURN DISTRIBUTION
# -----------------------------

print()
print("Churn distribution:")
print(df["churn_label"].value_counts())

# -----------------------------
# QUALITY RESULT
# -----------------------------

if (
    duplicate_customers == 0
    and null_count == 0
    and infinite_count == 0
):
    print()
    print("DATA QUALITY CHECK: PASSED")
else:
    print()
    print("DATA QUALITY CHECK: REVIEW REQUIRED")

print()
print("Validation completed!")