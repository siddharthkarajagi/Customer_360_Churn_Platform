import pandas as pd
import numpy as np

# -----------------------------
# NovaMart Customer Data
# -----------------------------

np.random.seed(42)

NUMBER_OF_CUSTOMERS = 10000

customer_ids = np.arange(1, NUMBER_OF_CUSTOMERS + 1)

first_names = [
    "Aarav", "Vivaan", "Aditya", "Arjun", "Rohan",
    "Rahul", "Karan", "Vikram", "Neha", "Priya",
    "Sneha", "Ananya", "Isha", "Pooja", "Riya"
]

last_names = [
    "Sharma", "Patil", "Deshmukh", "Kulkarni", "Joshi",
    "More", "Pawar", "Jadhav", "Shinde", "Kadam"
]

cities = [
    "Mumbai", "Pune", "Nashik", "Nagpur", "Solapur",
    "Aurangabad", "Kolhapur", "Thane", "Navi Mumbai", "Satara"
]

states = ["Maharashtra"] * len(cities)

genders = ["Male", "Female", "Other"]

customer_statuses = ["Active", "Inactive"]

customer_names = [
    f"{np.random.choice(first_names)} {np.random.choice(last_names)}"
    for _ in range(NUMBER_OF_CUSTOMERS)
]

customer_gender = np.random.choice(
    genders,
    size=NUMBER_OF_CUSTOMERS,
    p=[0.48, 0.48, 0.04]
)

customer_city = np.random.choice(
    cities,
    size=NUMBER_OF_CUSTOMERS
)

customer_state = [
    states[cities.index(city)]
    for city in customer_city
]

date_of_birth = pd.to_datetime(
    np.random.randint(
        pd.Timestamp("1970-01-01").value // 10**9,
        pd.Timestamp("2005-12-31").value // 10**9,
        NUMBER_OF_CUSTOMERS
    ),
    unit="s"
)

registration_date = pd.to_datetime(
    np.random.randint(
        pd.Timestamp("2021-01-01").value // 10**9,
        pd.Timestamp("2025-12-31").value // 10**9,
        NUMBER_OF_CUSTOMERS
    ),
    unit="s"
)

customer_status = np.random.choice(
    customer_statuses,
    size=NUMBER_OF_CUSTOMERS,
    p=[0.82, 0.18]
)

customers = pd.DataFrame({
    "customer_id": customer_ids,
    "customer_name": customer_names,
    "gender": customer_gender,
    "date_of_birth": date_of_birth,
    "city": customer_city,
    "state": customer_state,
    "registration_date": registration_date,
    "customer_status": customer_status
})

# Sort by customer_id
customers = customers.sort_values("customer_id")

# Save CSV
customers.to_csv(
    "../02_Raw_Data/customers.csv",
    index=False
)

print("Customer data generated successfully!")
print(f"Total customers: {len(customers)}")
print("\nFirst 5 records:")
print(customers.head())
print("\nCustomer status distribution:")
print(customers["customer_status"].value_counts())