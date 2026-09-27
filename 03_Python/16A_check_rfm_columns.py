import pandas as pd

file_path = r"D:\Customer_360_Churn_Platform\02_Raw_Data\customer_360_rfm.csv"

df = pd.read_csv(file_path)

print("\n==============================")
print("RFM FILE COLUMN CHECK")
print("==============================")

print("\nTotal columns:", len(df.columns))

print("\nColumns available in file:")

for column in df.columns:
    print(column)

print("\n==============================")
print("CHURN COLUMN CHECK")
print("==============================")

if "churn_label" in df.columns:
    print("churn_label FOUND")
    print(df["churn_label"].value_counts())
else:
    print("churn_label NOT FOUND")

if "churn_flag" in df.columns:
    print("\nchurn_flag FOUND")
    print(df["churn_flag"].value_counts())
else:
    print("\nchurn_flag NOT FOUND")