import random
from datetime import datetime, timedelta

from pymongo import MongoClient
import numpy as np


# -----------------------------
# SETTINGS
# -----------------------------

NUMBER_OF_EVENTS = 200000

np.random.seed(42)
random.seed(42)


# -----------------------------
# MONGODB CONNECTION
# -----------------------------

client = MongoClient("mongodb://localhost:27017/")

db = client["novamart"]
collection = db["customer_events"]

print("MongoDB connected successfully")


# -----------------------------
# EVENT DATA
# -----------------------------

event_types = [
    "page_view",
    "product_view",
    "search",
    "add_to_cart",
    "remove_from_cart",
    "wishlist",
    "checkout_start",
    "login"
]

devices = [
    "Mobile",
    "Desktop",
    "Tablet"
]

platforms = [
    "Android",
    "iOS",
    "Web"
]

pages = [
    "Home",
    "Product",
    "Search",
    "Category",
    "Cart",
    "Wishlist",
    "Checkout",
    "Account"
]

search_terms = [
    "shoes",
    "laptop",
    "headphones",
    "backpack",
    "watch",
    "gaming mouse",
    "face wash",
    "notebook"
]


# -----------------------------
# GENERATE EVENTS
# -----------------------------

events = []

start_date = datetime(2025, 1, 1)

for i in range(1, NUMBER_OF_EVENTS + 1):

    event_type = random.choice(event_types)

    customer_id = random.randint(1, 10000)

    event_date = start_date + timedelta(
        days=random.randint(0, 364),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
        seconds=random.randint(0, 59)
    )

    event = {
        "event_id": i,
        "customer_id": customer_id,
        "event_type": event_type,
        "event_timestamp": event_date,
        "device": random.choice(devices),
        "platform": random.choice(platforms),
        "page": random.choice(pages),
        "session_id": f"SES_{random.randint(100000, 999999)}"
    }

    # Product-related events
    if event_type in [
        "product_view",
        "add_to_cart",
        "remove_from_cart",
        "wishlist"
    ]:
        event["product_id"] = random.randint(1, 5000)

    # Search event
    if event_type == "search":
        event["search_term"] = random.choice(search_terms)

    events.append(event)


print("Events generated:", len(events))


# -----------------------------
# INSERT INTO MONGODB
# -----------------------------

collection.delete_many({})

batch_size = 5000

for start in range(0, len(events), batch_size):

    batch = events[start:start + batch_size]

    collection.insert_many(batch)

    print(
        f"Inserted {min(start + batch_size, len(events))} / {len(events)} events"
    )


# -----------------------------
# CREATE INDEXES
# -----------------------------

collection.create_index("customer_id")
collection.create_index("event_type")
collection.create_index("event_timestamp")


# -----------------------------
# VERIFY
# -----------------------------

total = collection.count_documents({})

print("\nCustomer events in MongoDB:", total)

print("\nMongoDB indexes created successfully")

client.close()

print("\nMongoDB Customer Events completed successfully!")