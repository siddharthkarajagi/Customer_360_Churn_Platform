import pandas as pd
import numpy as np
import mysql.connector
from pymongo import MongoClient


# ============================================================
# CONFIGURATION
# ============================================================

MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_DATABASE = "novamart"

MONGO_URI = "mongodb://localhost:27017/"
MONGO_DATABASE = "novamart"
MONGO_COLLECTION = "customer_events"

OUTPUT_PATH = r"D:\Customer_360_Churn_Platform\02_Raw_Data\customer_360_master.csv"


# ============================================================
# MYSQL CONNECTION
# ============================================================

mysql_conn = mysql.connector.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=input("Enter MySQL password: "),
    database=MYSQL_DATABASE
)

mysql_cursor = mysql_conn.cursor()

print()
print("MySQL connected successfully")


# ============================================================
# HELPER FUNCTION
# ============================================================

def mysql_df(query):
    mysql_cursor.execute(query)

    rows = mysql_cursor.fetchall()
    columns = [column[0] for column in mysql_cursor.description]

    return pd.DataFrame(rows, columns=columns)


# ============================================================
# 1. CUSTOMERS
# ============================================================

customers = mysql_df("""
    SELECT
        customer_id,
        customer_name,
        gender,
        date_of_birth,
        city,
        state,
        registration_date,
        customer_status
    FROM customers
""")

print("Customers:", len(customers))


# ============================================================
# 2. ORDERS
# ============================================================

orders = mysql_df("""
    SELECT
        order_id,
        customer_id,
        order_date,
        order_channel,
        store_id,
        order_status,
        total_order_amount
    FROM orders
""")

print("Orders:", len(orders))


# ============================================================
# 3. ORDER FEATURES
# ============================================================

orders["order_date"] = pd.to_datetime(
    orders["order_date"],
    errors="coerce"
)

orders["total_order_amount"] = pd.to_numeric(
    orders["total_order_amount"],
    errors="coerce"
).fillna(0)

customer_orders = (
    orders
    .groupby("customer_id")
    .agg(
        total_orders=("order_id", "nunique"),
        total_revenue=("total_order_amount", "sum"),
        first_order_date=("order_date", "min"),
        last_order_date=("order_date", "max")
    )
    .reset_index()
)

print("Customer order features created")


# ============================================================
# 4. PAYMENTS
# ============================================================

payments = mysql_df("""
    SELECT
        customer_id,
        payment_amount
    FROM payments
""")

payments["payment_amount"] = pd.to_numeric(
    payments["payment_amount"],
    errors="coerce"
).fillna(0)

payment_features = (
    payments
    .groupby("customer_id")
    .agg(
        total_payment_amount=("payment_amount", "sum"),
        payment_count=("payment_amount", "count")
    )
    .reset_index()
)

print("Payment features created")


# ============================================================
# 5. RETURNS
# ============================================================

returns = mysql_df("""
    SELECT
        customer_id,
        return_amount
    FROM returns
""")

returns["return_amount"] = pd.to_numeric(
    returns["return_amount"],
    errors="coerce"
).fillna(0)

return_features = (
    returns
    .groupby("customer_id")
    .agg(
        total_return_amount=("return_amount", "sum"),
        return_count=("return_amount", "count")
    )
    .reset_index()
)

print("Return features created")


# ============================================================
# 6. SUPPORT TICKETS
# ============================================================

support = mysql_df("""
    SELECT
        customer_id,
        ticket_id,
        customer_satisfaction_score
    FROM support_tickets
""")

support["customer_satisfaction_score"] = pd.to_numeric(
    support["customer_satisfaction_score"],
    errors="coerce"
)

support_features = (
    support
    .groupby("customer_id")
    .agg(
        total_tickets=("ticket_id", "nunique"),
        avg_satisfaction=("customer_satisfaction_score", "mean")
    )
    .reset_index()
)

print("Support features created")


# ============================================================
# 7. CUSTOMER CAMPAIGNS
# ============================================================

customer_campaigns = mysql_df("""
    SELECT
        customer_id,
        campaign_id,
        sent_date,
        opened,
        clicked,
        converted,
        conversion_amount
    FROM customer_campaigns
""")

customer_campaigns["conversion_amount"] = pd.to_numeric(
    customer_campaigns["conversion_amount"],
    errors="coerce"
).fillna(0)

campaign_features = (
    customer_campaigns
    .groupby("customer_id")
    .agg(
        campaigns_received=("campaign_id", "count"),
        campaigns_opened=("opened", "sum"),
        campaigns_clicked=("clicked", "sum"),
        campaigns_converted=("converted", "sum"),
        campaign_conversion_value=("conversion_amount", "sum")
    )
    .reset_index()
)

print("Campaign features created")


# ============================================================
# 8. MONGODB CONNECTION
# ============================================================

mongo_client = MongoClient(MONGO_URI)

mongo_db = mongo_client[MONGO_DATABASE]

events_collection = mongo_db[MONGO_COLLECTION]

print("MongoDB connected successfully")


# ============================================================
# 9. READ MONGODB EVENTS
# ============================================================

events = list(
    events_collection.find(
        {},
        {
            "_id": 0,
            "customer_id": 1,
            "event_type": 1,
            "device": 1,
            "platform": 1,
            "session_id": 1
        }
    )
)

events_df = pd.DataFrame(events)

print("MongoDB events:", len(events_df))


# ============================================================
# 10. MONGODB CUSTOMER FEATURES
# ============================================================

if not events_df.empty:

    event_features = (
        events_df
        .groupby("customer_id")
        .agg(
            total_events=("event_type", "count"),
            unique_event_types=("event_type", "nunique"),
            unique_sessions=("session_id", "nunique")
        )
        .reset_index()
    )

    event_counts = pd.crosstab(
        events_df["customer_id"],
        events_df["event_type"]
    ).reset_index()

    event_features = event_features.merge(
        event_counts,
        on="customer_id",
        how="left"
    )

else:

    event_features = pd.DataFrame(
        columns=[
            "customer_id",
            "total_events",
            "unique_event_types",
            "unique_sessions"
        ]
    )

print("MongoDB behavior features created")


# ============================================================
# 11. MERGE CUSTOMER 360
# ============================================================

customer_360 = customers.copy()

customer_360 = customer_360.merge(
    customer_orders,
    on="customer_id",
    how="left"
)

customer_360 = customer_360.merge(
    payment_features,
    on="customer_id",
    how="left"
)

customer_360 = customer_360.merge(
    return_features,
    on="customer_id",
    how="left"
)

customer_360 = customer_360.merge(
    support_features,
    on="customer_id",
    how="left"
)

customer_360 = customer_360.merge(
    campaign_features,
    on="customer_id",
    how="left"
)

customer_360 = customer_360.merge(
    event_features,
    on="customer_id",
    how="left"
)

print("Customer 360 datasets merged")


# ============================================================
# 12. FILL MISSING NUMERIC VALUES
# ============================================================

numeric_columns = customer_360.select_dtypes(
    include=["number"]
).columns

customer_360[numeric_columns] = (
    customer_360[numeric_columns]
    .fillna(0)
)


# ============================================================
# 13. DATE CONVERSIONS
# ============================================================

customer_360["registration_date"] = pd.to_datetime(
    customer_360["registration_date"],
    errors="coerce"
)

customer_360["first_order_date"] = pd.to_datetime(
    customer_360["first_order_date"],
    errors="coerce"
)

customer_360["last_order_date"] = pd.to_datetime(
    customer_360["last_order_date"],
    errors="coerce"
)


# ============================================================
# 14. CUSTOMER TENURE
# ============================================================

today = pd.Timestamp.today().normalize()

customer_360["customer_tenure_days"] = (
    today - customer_360["registration_date"]
).dt.days

customer_360["customer_tenure_days"] = (
    customer_360["customer_tenure_days"]
    .fillna(0)
)


# ============================================================
# 15. RECENCY
# ============================================================

customer_360["days_since_last_order"] = np.where(
    customer_360["last_order_date"].notna(),
    (
        today -
        customer_360["last_order_date"]
    ).dt.days,
    -1
)


# ============================================================
# 16. AVERAGE ORDER VALUE
# ============================================================

customer_360["average_order_value"] = np.where(
    customer_360["total_orders"] > 0,
    customer_360["total_revenue"]
    / customer_360["total_orders"],
    0
)


# ============================================================
# 17. RETURN RATE
# ============================================================

customer_360["return_rate"] = np.where(
    customer_360["total_orders"] > 0,
    customer_360["return_count"]
    / customer_360["total_orders"],
    0
)


# ============================================================
# 18. CAMPAIGN OPEN RATE
# ============================================================

customer_360["campaign_open_rate"] = np.where(
    customer_360["campaigns_received"] > 0,
    customer_360["campaigns_opened"]
    / customer_360["campaigns_received"],
    0
)


# ============================================================
# 19. CAMPAIGN CLICK RATE
# ============================================================

customer_360["campaign_click_rate"] = np.where(
    customer_360["campaigns_received"] > 0,
    customer_360["campaigns_clicked"]
    / customer_360["campaigns_received"],
    0
)


# ============================================================
# 20. CUSTOMER VALUE SEGMENT
# ============================================================

customer_360["customer_value_segment"] = pd.cut(
    customer_360["total_revenue"],
    bins=[
        -np.inf,
        5000,
        20000,
        50000,
        np.inf
    ],
    labels=[
        "Low Value",
        "Medium Value",
        "High Value",
        "VIP"
    ]
)


# ============================================================
# 21. CHURN RISK SCORE
# ============================================================

def calculate_churn_risk(row):

    score = 0

    if row["days_since_last_order"] > 180:
        score += 40

    elif row["days_since_last_order"] > 90:
        score += 25

    elif row["days_since_last_order"] > 60:
        score += 15

    if row["total_orders"] <= 1:
        score += 20

    elif row["total_orders"] <= 3:
        score += 10

    if row["total_tickets"] >= 5:
        score += 15

    if (
        row["avg_satisfaction"] > 0
        and row["avg_satisfaction"] <= 2
    ):
        score += 15

    if (
        row["campaigns_received"] > 0
        and row["campaign_open_rate"] < 0.20
    ):
        score += 10

    return score


customer_360["churn_risk_score"] = (
    customer_360.apply(
        calculate_churn_risk,
        axis=1
    )
)


# ============================================================
# 22. CHURN RISK CATEGORY
# ============================================================

customer_360["churn_risk_category"] = pd.cut(
    customer_360["churn_risk_score"],
    bins=[
        -1,
        20,
        40,
        60,
        np.inf
    ],
    labels=[
        "Low Risk",
        "Medium Risk",
        "High Risk",
        "Critical Risk"
    ]
)


# ============================================================
# 23. REVENUE AT RISK
# ============================================================

customer_360["revenue_at_risk"] = np.where(
    customer_360["churn_risk_score"] >= 40,
    customer_360["total_revenue"],
    0
)


# ============================================================
# 24. RECOMMENDED RETENTION ACTION
# ============================================================

def retention_action(row):

    if row["churn_risk_category"] == "Critical Risk":
        return "Priority Retention + Personal Offer"

    elif row["churn_risk_category"] == "High Risk":
        return "Targeted Retention Campaign"

    elif row["churn_risk_category"] == "Medium Risk":
        return "Engagement Campaign"

    else:
        return "Regular Engagement"


customer_360["recommended_action"] = (
    customer_360.apply(
        retention_action,
        axis=1
    )
)


# ============================================================
# 25. REMOVE DUPLICATE CUSTOMERS
# ============================================================

customer_360 = customer_360.drop_duplicates(
    subset=["customer_id"]
)


# ============================================================
# 26. SORT BY CHURN RISK
# ============================================================

customer_360 = customer_360.sort_values(
    by="churn_risk_score",
    ascending=False
)


# ============================================================
# 27. SAVE FINAL CUSTOMER 360 DATASET
# ============================================================

customer_360.to_csv(
    OUTPUT_PATH,
    index=False
)


# ============================================================
# 28. FINAL SUMMARY
# ============================================================

print()
print("==========================================")
print("CUSTOMER 360 BUILD COMPLETED")
print("==========================================")

print(
    "Customers:",
    len(customer_360)
)

print(
    "Features:",
    len(customer_360.columns)
)

print(
    "High/Critical Risk Customers:",
    (
        customer_360["churn_risk_score"] >= 40
    ).sum()
)

print(
    "Revenue at Risk:",
    round(
        customer_360["revenue_at_risk"].sum(),
        2
    )
)

print(
    "Output:",
    OUTPUT_PATH
)

print()
print("MySQL connection closed")
print("MongoDB connection closed")
print("Customer 360 Master Dataset ready!")


# ============================================================
# CLOSE CONNECTIONS
# ============================================================

mysql_cursor.close()
mysql_conn.close()

mongo_client.close()


