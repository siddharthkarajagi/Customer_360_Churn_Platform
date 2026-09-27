import pandas as pd
import numpy as np

INPUT_PATH = r"D:\Customer_360_Churn_Platform\02_Raw_Data\customer_360_master.csv"

OUTPUT_PATH = r"D:\Customer_360_Churn_Platform\02_Raw_Data\customer_360_rfm.csv"

df = pd.read_csv(INPUT_PATH)

print("Customer 360 loaded:", len(df))

# -----------------------------
# RECENCY SCORE
# -----------------------------

df["R_score"] = pd.qcut(
    df["days_since_last_order"].rank(method="first"),
    5,
    labels=[5, 4, 3, 2, 1]
).astype(int)

# -----------------------------
# FREQUENCY SCORE
# -----------------------------

df["F_score"] = pd.qcut(
    df["total_orders"].rank(method="first"),
    5,
    labels=[1, 2, 3, 4, 5]
).astype(int)

# -----------------------------
# MONETARY SCORE
# -----------------------------

df["M_score"] = pd.qcut(
    df["total_revenue"].rank(method="first"),
    5,
    labels=[1, 2, 3, 4, 5]
).astype(int)

# -----------------------------
# RFM SCORE
# -----------------------------

df["RFM_score"] = (
    df["R_score"].astype(str)
    + df["F_score"].astype(str)
    + df["M_score"].astype(str)
)

# -----------------------------
# RFM SEGMENT
# -----------------------------

def rfm_segment(row):

    if row["R_score"] >= 4 and row["F_score"] >= 4 and row["M_score"] >= 4:
        return "Champions"

    elif row["R_score"] >= 4 and row["F_score"] >= 3:
        return "Loyal Customers"

    elif row["R_score"] >= 4:
        return "Recent Customers"

    elif row["R_score"] <= 2 and row["F_score"] >= 3:
        return "At Risk"

    elif row["R_score"] <= 2 and row["M_score"] >= 4:
        return "High Value At Risk"

    elif row["R_score"] <= 2:
        return "Hibernating"

    else:
        return "Potential Loyalists"


df["rfm_segment"] = df.apply(
    rfm_segment,
    axis=1
)

df.to_csv(
    OUTPUT_PATH,
    index=False
)

print()
print("RFM Analysis completed!")
print("Customers:", len(df))
print("Segments:")
print(df["rfm_segment"].value_counts())

print()
print("Output:")
print(OUTPUT_PATH)