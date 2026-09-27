import pandas as pd
import numpy as np
from pathlib import Path

# ============================================================
# CUSTOMER 360 - POWER BI DATASET PREPARATION
# ============================================================

PROJECT_PATH = Path(r"D:\Customer_360_Churn_Platform")

INPUT_FILE = (
    PROJECT_PATH
    / "02_Raw_Data"
    / "customer_360_rfm.csv"
)

OUTPUT_FILE = (
    PROJECT_PATH
    / "02_Raw_Data"
    / "customer_360_dashboard.csv"
)

print("=" * 60)
print("CUSTOMER 360 - POWER BI DATASET PREPARATION")
print("=" * 60)

# ============================================================
# 1. LOAD DATA
# ============================================================

print("\n[1/6] Loading customer 360 RFM data...")

df = pd.read_csv(INPUT_FILE)

print(f"Rows loaded: {len(df):,}")
print(f"Columns loaded: {len(df.columns)}")

# ============================================================
# 2. CLEANING
# ============================================================

print("\n[2/6] Cleaning data...")

# Remove duplicate customers
df = df.drop_duplicates(
    subset=["customer_id"]
).copy()

# Replace infinite values
df.replace(
    [np.inf, -np.inf],
    np.nan,
    inplace=True
)

# Numeric columns
numeric_columns = [
    "customer_tenure_days",
    "total_orders",
    "total_revenue",
    "average_order_value",
    "days_since_last_order",
    "return_count",
    "return_rate",
    "total_tickets",
    "avg_satisfaction",
    "campaigns_received",
    "campaigns_opened",
    "campaigns_clicked",
    "campaigns_converted",
    "campaign_conversion_value",
    "campaign_open_rate",
    "campaign_click_rate",
    "total_events",
    "unique_event_types",
    "unique_sessions",
    "R_score",
    "F_score",
    "M_score",
    "RFM_score",
    "revenue_at_risk"
]

for col in numeric_columns:

    if col in df.columns:

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

        df[col] = df[col].fillna(0)

# ============================================================
# 3. BUSINESS METRICS
# ============================================================

print("\n[3/6] Creating business metrics...")

# Customer value segment
if "customer_value_segment" in df.columns:

    df["customer_value_segment"] = (
        df["customer_value_segment"]
        .fillna("Unknown")
        .astype(str)
    )

# Churn risk category
if "churn_risk_category" in df.columns:

    df["churn_risk_category"] = (
        df["churn_risk_category"]
        .fillna("Low")
        .astype(str)
    )

# Recommended action
if "recommended_action" in df.columns:

    df["recommended_action"] = (
        df["recommended_action"]
        .fillna("Monitor")
        .astype(str)
    )

# Revenue at risk
if "revenue_at_risk" in df.columns:

    df["revenue_at_risk"] = pd.to_numeric(
        df["revenue_at_risk"],
        errors="coerce"
    ).fillna(0)

# ============================================================
# 4. RETENTION PRIORITY
# ============================================================

print("\n[4/6] Creating retention priority...")


def retention_priority(row):

    risk = str(
        row.get(
            "churn_risk_category",
            "Low"
        )
    )

    value = str(
        row.get(
            "customer_value_segment",
            "Unknown"
        )
    )

    revenue = float(
        row.get(
            "total_revenue",
            0
        )
    )

    if risk in ["High", "Critical"] and revenue >= 5000:

        return "Immediate"

    elif risk in ["High", "Critical"]:

        return "High"

    elif risk == "Medium" and value in [
        "High Value",
        "Premium"
    ]:

        return "High"

    elif risk == "Medium":

        return "Medium"

    else:

        return "Monitor"


df["retention_priority"] = df.apply(
    retention_priority,
    axis=1
)

# ============================================================
# 5. DASHBOARD FLAGS
# ============================================================

print("\n[5/6] Creating dashboard flags...")

# ------------------------------------------------------------
# Create churn_label
# ------------------------------------------------------------

if "churn_label" not in df.columns:

    if "churn_flag" in df.columns:

        df["churn_label"] = np.where(
            df["churn_flag"] == 1,
            "Churn",
            "Active"
        )

    elif "churn_risk_category" in df.columns:

        df["churn_label"] = np.where(
            df["churn_risk_category"].isin(
                ["High", "Critical"]
            ),
            "Churn",
            "Active"
        )

    else:

        print(
            "ERROR: Cannot create churn_label."
        )

        raise SystemExit

# ------------------------------------------------------------
# Churn flag
# ------------------------------------------------------------

df["is_churn"] = np.where(

    df["churn_label"]
    .astype(str)
    .str.lower()
    .eq("churn"),

    1,
    0
)

# ------------------------------------------------------------
# High-risk flag
# ------------------------------------------------------------

df["is_high_risk"] = np.where(

    df["churn_risk_category"].isin(
        ["High", "Critical"]
    ),

    1,
    0
)

# ------------------------------------------------------------
# Returning customer
# ------------------------------------------------------------

df["is_returning_customer"] = np.where(

    df["total_orders"] > 1,

    1,
    0
)

# ------------------------------------------------------------
# Support ticket
# ------------------------------------------------------------

df["has_support_ticket"] = np.where(

    df["total_tickets"] > 0,

    1,
    0
)

# ------------------------------------------------------------
# Campaign engagement
# ------------------------------------------------------------

df["has_campaign_engagement"] = np.where(

    df["campaigns_opened"] > 0,

    1,
    0
)

# ------------------------------------------------------------
# Digital activity
# ------------------------------------------------------------

df["has_digital_activity"] = np.where(

    df["total_events"] > 0,

    1,
    0
)

# ============================================================
# 6. SAVE POWER BI DATASET
# ============================================================

print("\n[6/6] Saving Power BI dataset...")

df.to_csv(

    OUTPUT_FILE,

    index=False,

    encoding="utf-8-sig"
)

# ============================================================
# FINAL VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("SUCCESS")
print("=" * 60)

print(
    f"Final rows: {len(df):,}"
)

print(
    f"Final columns: {len(df.columns)}"
)

print("\nOutput file:")

print(OUTPUT_FILE)

print("\nChurn distribution:")

print(
    df["churn_label"].value_counts()
)

print("\nRetention priority:")

print(
    df["retention_priority"].value_counts()
)

print("\nHigh-risk customers:")

print(
    df["is_high_risk"].sum()
)

print("\nRevenue at risk:")

print(
    f"{df['revenue_at_risk'].sum():,.2f}"
)

print("\nFinal columns:")

for i, col in enumerate(
    df.columns,
    start=1
):

    print(
        f"{i}. {col}"
    )

print("\nPower BI dataset preparation completed.")
