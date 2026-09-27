import pandas as pd
import numpy as np

# ============================================================
# STEP 15 - PREPARE ORANGE DATASET
# ============================================================

input_file = r"D:\Customer_360_Churn_Platform\02_Raw_Data\customer_360_rfm_churn.csv"

output_file = r"D:\Customer_360_Churn_Platform\09_Orange\churn_orange_dataset.csv"

print("Loading churn dataset...")

df = pd.read_csv(input_file)

print("Input rows:", len(df))
print("Input columns:", len(df.columns))

# ============================================================
# FEATURES FOR MACHINE LEARNING
# ============================================================

features = [
    "customer_id",
    "customer_tenure_days",
    "total_orders",
    "total_revenue",
    "average_order_value",
    "return_count",
    "return_rate",
    "total_tickets",
    "avg_satisfaction",
    "campaigns_received",
    "campaign_open_rate",
    "campaign_click_rate",
    "campaigns_converted",
    "total_events",
    "unique_event_types",
    "unique_sessions",
    "R_score",
    "F_score",
    "M_score",
    "churn_label"
]

# ============================================================
# CHECK COLUMNS
# ============================================================

missing_columns = [
    column
    for column in features
    if column not in df.columns
]

if missing_columns:
    print("\nERROR!")
    print("Missing columns:")
    print(missing_columns)
    raise SystemExit

# ============================================================
# CREATE ML DATASET
# ============================================================

df_model = df[features].copy()

# Replace infinity
numeric_columns = df_model.select_dtypes(
    include=[np.number]
).columns

df_model[numeric_columns] = (
    df_model[numeric_columns]
    .replace([np.inf, -np.inf], np.nan)
)

# Fill missing numeric values
df_model[numeric_columns] = (
    df_model[numeric_columns]
    .fillna(0)
)

# Remove duplicate customers
df_model = df_model.drop_duplicates(
    subset=["customer_id"]
)

# ============================================================
# RESULT CHECK
# ============================================================

print("\n==============================")
print("ORANGE DATASET CHECK")
print("==============================")

print("Final rows:", len(df_model))
print("Final columns:", len(df_model.columns))

print("\nChurn distribution:")
print(
    df_model["churn_label"].value_counts()
)

print("\nMissing values:")
print(
    df_model.isnull().sum().sum()
)

# ============================================================
# SAVE
# ============================================================

df_model.to_csv(
    output_file,
    index=False
)

print("\n===================================")
print("ORANGE DATASET CREATED SUCCESSFULLY")
print("===================================")

print("\nSaved file:")
print(output_file)