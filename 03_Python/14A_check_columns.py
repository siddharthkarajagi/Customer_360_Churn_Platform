import pandas as pd

file_path = r"D:\Customer_360_Churn_Platform\02_Raw_Data\customer_360_rfm.csv"

df = pd.read_csv(file_path)

print("\n==============================")
print("ALL COLUMNS")
print("==============================")

for i, column in enumerate(df.columns, start=1):
    print(i, "->", column)

print("\n==============================")
print("POSSIBLE TENURE / DATE COLUMNS")
print("==============================")

for column in df.columns:
    if (
        "tenure" in column.lower()
        or "date" in column.lower()
        or "days" in column.lower()
    ):
        print(column)