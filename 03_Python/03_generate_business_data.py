import pandas as pd
import numpy as np

# ============================================================
# NOVAMART - PAYMENTS, RETURNS, SUPPORT & MARKETING DATA
# ============================================================

np.random.seed(42)

RAW_PATH = "../02_Raw_Data/"

# ------------------------------------------------------------
# LOAD EXISTING DATA
# ------------------------------------------------------------

customers = pd.read_csv(
    RAW_PATH + "customers.csv"
)

orders = pd.read_csv(
    RAW_PATH + "orders.csv"
)

order_items = pd.read_csv(
    RAW_PATH + "order_items.csv"
)

products = pd.read_csv(
    RAW_PATH + "products.csv"
)

customers["registration_date"] = pd.to_datetime(
    customers["registration_date"]
)

orders["order_date"] = pd.to_datetime(
    orders["order_date"]
)

print("Existing data loaded successfully.")


# ============================================================
# 1. PAYMENTS
# ============================================================

print("\nCreating payments...")

completed_orders = orders[
    orders["order_status"] == "Completed"
].copy()

payments = pd.DataFrame({
    "payment_id": np.arange(
        1,
        len(completed_orders) + 1
    ),

    "order_id": completed_orders["order_id"].values,

    "customer_id": completed_orders["customer_id"].values,

    "payment_date": completed_orders["order_date"].values,

    "payment_method": np.random.choice(
        [
            "UPI",
            "Credit Card",
            "Debit Card",
            "Net Banking",
            "Cash on Delivery",
            "Wallet"
        ],
        len(completed_orders),
        p=[
            0.35,
            0.22,
            0.15,
            0.08,
            0.12,
            0.08
        ]
    ),

    "payment_status": np.random.choice(
        [
            "Successful",
            "Failed",
            "Refunded"
        ],
        len(completed_orders),
        p=[
            0.94,
            0.03,
            0.03
        ]
    ),

    "amount": completed_orders[
        "total_amount"
    ].values
})

payments.to_csv(
    RAW_PATH + "payments.csv",
    index=False
)

print("Payments created:", len(payments))


# ============================================================
# 2. RETURNS
# ============================================================

print("\nCreating returns...")

# Approximately 7% of completed order items are returned

return_count = int(
    len(order_items) * 0.07
)

return_indices = np.random.choice(
    order_items.index,
    return_count,
    replace=False
)

return_items = order_items.loc[
    return_indices
].copy()

return_items = return_items.merge(
    orders[
        [
            "order_id",
            "customer_id",
            "order_date"
        ]
    ],
    on="order_id",
    how="left"
)

return_items = return_items.merge(
    products[
        [
            "product_id",
            "product_name"
        ]
    ],
    on="product_id",
    how="left"
)

return_dates = (
    return_items["order_date"]
    + pd.to_timedelta(
        np.random.randint(
            2,
            31,
            len(return_items)
        ),
        unit="D"
    )
)

returns = pd.DataFrame({
    "return_id": np.arange(
        1,
        len(return_items) + 1
    ),

    "order_id": return_items["order_id"].values,

    "customer_id": return_items["customer_id"].values,

    "product_id": return_items["product_id"].values,

    "return_date": return_dates,

    "return_reason": np.random.choice(
        [
            "Damaged Product",
            "Wrong Product",
            "Size Issue",
            "Quality Issue",
            "Changed Mind",
            "Late Delivery"
        ],
        len(return_items)
    ),

    "refund_amount": np.round(
        return_items["item_total"].values,
        2
    ),

    "return_status": np.random.choice(
        [
            "Approved",
            "Rejected",
            "Processing"
        ],
        len(return_items),
        p=[
            0.82,
            0.08,
            0.10
        ]
    )
})

returns.to_csv(
    RAW_PATH + "returns.csv",
    index=False
)

print("Returns created:", len(returns))


# ============================================================
# 3. SUPPORT TICKETS
# ============================================================

print("\nCreating support tickets...")

NUMBER_OF_TICKETS = 100000

ticket_customer_ids = np.random.choice(
    customers["customer_id"],
    NUMBER_OF_TICKETS
)

ticket_dates = pd.to_datetime(
    np.random.randint(
        pd.Timestamp("2025-01-01").value // 10**9,
        pd.Timestamp("2026-08-31").value // 10**9,
        NUMBER_OF_TICKETS
    ),
    unit="s"
)

support_tickets = pd.DataFrame({

    "ticket_id": np.arange(
        1,
        NUMBER_OF_TICKETS + 1
    ),

    "customer_id": ticket_customer_ids,

    "ticket_date": ticket_dates,

    "issue_type": np.random.choice(
        [
            "Delivery Delay",
            "Payment Issue",
            "Product Quality",
            "Return Request",
            "Refund Issue",
            "Account Issue",
            "Technical Issue"
        ],
        NUMBER_OF_TICKETS
    ),

    "priority": np.random.choice(
        [
            "Low",
            "Medium",
            "High",
            "Critical"
        ],
        NUMBER_OF_TICKETS,
        p=[
            0.25,
            0.50,
            0.20,
            0.05
        ]
    ),

    "status": np.random.choice(
        [
            "Open",
            "In Progress",
            "Resolved",
            "Closed"
        ],
        NUMBER_OF_TICKETS,
        p=[
            0.08,
            0.12,
            0.40,
            0.40
        ]
    ),

    "resolution_time_hours": np.round(
        np.random.gamma(
            shape=2.5,
            scale=8,
            size=NUMBER_OF_TICKETS
        ),
        2
    )
})

support_tickets.to_csv(
    RAW_PATH + "support_tickets.csv",
    index=False
)

print(
    "Support tickets created:",
    len(support_tickets)
)


# ============================================================
# 4. MARKETING CAMPAIGNS
# ============================================================

print("\nCreating marketing campaigns...")

NUMBER_OF_CAMPAIGNS = 50

campaign_start_dates = pd.date_range(
    "2025-01-01",
    "2026-06-01",
    periods=NUMBER_OF_CAMPAIGNS
)

marketing_campaigns = pd.DataFrame({

    "campaign_id": np.arange(
        1,
        NUMBER_OF_CAMPAIGNS + 1
    ),

    "campaign_name": [
        f"NovaMart Campaign {i}"
        for i in range(
            1,
            NUMBER_OF_CAMPAIGNS + 1
        )
    ],

    "channel": np.random.choice(
        [
            "Email",
            "SMS",
            "Push Notification",
            "Social Media",
            "Search Ads"
        ],
        NUMBER_OF_CAMPAIGNS
    ),

    "start_date": campaign_start_dates,

    "end_date": (
        campaign_start_dates
        + pd.to_timedelta(
            np.random.randint(
                7,
                31,
                NUMBER_OF_CAMPAIGNS
            ),
            unit="D"
        )
    ),

    "budget": np.round(
        np.random.uniform(
            10000,
            500000,
            NUMBER_OF_CAMPAIGNS
        ),
        2
    )
})

marketing_campaigns.to_csv(
    RAW_PATH + "marketing_campaigns.csv",
    index=False
)

print(
    "Marketing campaigns created:",
    len(marketing_campaigns)
)


# ============================================================
# 5. CUSTOMER CAMPAIGN PARTICIPATION
# ============================================================

print("\nCreating customer campaign interactions...")

NUMBER_OF_CAMPAIGN_RECORDS = 200000

campaign_customer_ids = np.random.choice(
    customers["customer_id"],
    NUMBER_OF_CAMPAIGN_RECORDS
)

campaign_ids = np.random.choice(
    marketing_campaigns["campaign_id"],
    NUMBER_OF_CAMPAIGN_RECORDS
)

engagement_dates = pd.to_datetime(
    np.random.randint(
        pd.Timestamp("2025-01-01").value // 10**9,
        pd.Timestamp("2026-08-31").value // 10**9,
        NUMBER_OF_CAMPAIGN_RECORDS
    ),
    unit="s"
)

customer_campaigns = pd.DataFrame({

    "customer_campaign_id": np.arange(
        1,
        NUMBER_OF_CAMPAIGN_RECORDS + 1
    ),

    "customer_id": campaign_customer_ids,

    "campaign_id": campaign_ids,

    "engagement_date": engagement_dates,

    "response_status": np.random.choice(
        [
            "Clicked",
            "Opened",
            "Converted",
            "Ignored",
            "Unsubscribed"
        ],
        NUMBER_OF_CAMPAIGN_RECORDS,
        p=[
            0.15,
            0.25,
            0.10,
            0.45,
            0.05
        ]
    )
})

customer_campaigns.to_csv(
    RAW_PATH + "customer_campaigns.csv",
    index=False
)

print(
    "Customer campaign records created:",
    len(customer_campaigns)
)


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n")
print("================================================")
print("NOVAMART BUSINESS DATA GENERATION COMPLETED")
print("================================================")

print("Customers:", len(customers))
print("Orders:", len(orders))
print("Payments:", len(payments))
print("Returns:", len(returns))
print("Support Tickets:", len(support_tickets))
print("Marketing Campaigns:", len(marketing_campaigns))
print("Customer Campaign Records:", len(customer_campaigns))

print("\nFiles generated successfully!")

print("\nNext step:")
print("CSV validation and MySQL loading.")
