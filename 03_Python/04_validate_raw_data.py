import pandas as pd
from pathlib import Path


# ============================================================
# NOVAMART - RAW DATA VALIDATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BASE_DIR / "02_Raw_Data"


# Files expected in the project
expected_files = [
    "customers.csv",
    "products.csv",
    "stores.csv",
    "orders.csv",
    "order_items.csv",
    "payments.csv",
    "returns.csv",
    "support_tickets.csv",
    "marketing_campaigns.csv",
    "customer_campaigns.csv"
]


print("\n" + "=" * 60)
print("NOVAMART RAW DATA VALIDATION")
print("=" * 60)


# ------------------------------------------------------------
# STEP 1 - FILE EXISTENCE CHECK
# ------------------------------------------------------------

print("\n1. FILE EXISTENCE CHECK")
print("-" * 40)

missing_files = []

for file_name in expected_files:

    file_path = RAW_DATA_DIR / file_name

    if file_path.exists():
        print(f"[OK] {file_name}")
    else:
        print(f"[MISSING] {file_name}")
        missing_files.append(file_name)


# ------------------------------------------------------------
# STEP 2 - LOAD AVAILABLE CSV FILES
# ------------------------------------------------------------

print("\n2. LOADING CSV FILES")
print("-" * 40)

dataframes = {}

for file_name in expected_files:

    file_path = RAW_DATA_DIR / file_name

    if file_path.exists():

        try:
            df = pd.read_csv(file_path)

            dataframes[file_name] = df

            print(
                f"[LOADED] {file_name} "
                f"-> {len(df):,} rows, {len(df.columns)} columns"
            )

        except Exception as error:

            print(f"[ERROR] {file_name} -> {error}")


# ------------------------------------------------------------
# STEP 3 - NULL VALUE CHECK
# ------------------------------------------------------------

print("\n3. NULL VALUE CHECK")
print("-" * 40)

for file_name, df in dataframes.items():

    total_nulls = df.isnull().sum().sum()

    if total_nulls == 0:

        print(f"[OK] {file_name} -> No NULL values")

    else:

        print(f"[WARNING] {file_name} -> {total_nulls:,} NULL values")

        null_columns = df.isnull().sum()

        null_columns = null_columns[null_columns > 0]

        for column, count in null_columns.items():

            print(f"       {column}: {count:,}")


# ------------------------------------------------------------
# STEP 4 - DUPLICATE ROW CHECK
# ------------------------------------------------------------

print("\n4. DUPLICATE ROW CHECK")
print("-" * 40)

for file_name, df in dataframes.items():

    duplicates = df.duplicated().sum()

    if duplicates == 0:

        print(f"[OK] {file_name} -> No duplicate rows")

    else:

        print(
            f"[WARNING] {file_name} "
            f"-> {duplicates:,} duplicate rows"
        )


# ------------------------------------------------------------
# STEP 5 - DATASET SIZE SUMMARY
# ------------------------------------------------------------

print("\n5. DATASET SIZE SUMMARY")
print("-" * 40)

for file_name, df in dataframes.items():

    print(f"{file_name:<30} {len(df):>10,} rows")


# ------------------------------------------------------------
# STEP 6 - PRIMARY KEY DUPLICATE CHECK
# ------------------------------------------------------------

print("\n6. PRIMARY KEY CHECK")
print("-" * 40)

primary_keys = {
    "customers.csv": "customer_id",
    "products.csv": "product_id",
    "stores.csv": "store_id",
    "orders.csv": "order_id",
    "order_items.csv": "order_item_id",
    "payments.csv": "payment_id",
    "returns.csv": "return_id",
    "support_tickets.csv": "ticket_id",
    "marketing_campaigns.csv": "campaign_id"
}


for file_name, primary_key in primary_keys.items():

    if file_name not in dataframes:
        continue

    df = dataframes[file_name]

    if primary_key not in df.columns:

        print(
            f"[WARNING] {file_name} "
            f"-> {primary_key} column not found"
        )

        continue

    duplicate_ids = df[primary_key].duplicated().sum()

    null_ids = df[primary_key].isnull().sum()

    if duplicate_ids == 0 and null_ids == 0:

        print(
            f"[OK] {file_name} "
            f"-> {primary_key} unique & complete"
        )

    else:

        print(
            f"[WARNING] {file_name} "
            f"-> duplicate IDs: {duplicate_ids:,}, "
            f"NULL IDs: {null_ids:,}"
        )


# ------------------------------------------------------------
# FINAL SUMMARY
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("VALIDATION SUMMARY")
print("=" * 60)

print(f"Expected files : {len(expected_files)}")
print(f"Loaded files   : {len(dataframes)}")
print(f"Missing files  : {len(missing_files)}")

if len(missing_files) == 0:

    print("\nSTATUS: ALL EXPECTED FILES ARE AVAILABLE")

else:

    print("\nSTATUS: SOME FILES ARE MISSING")

print("\nRAW DATA VALIDATION COMPLETED.")
print("=" * 60)