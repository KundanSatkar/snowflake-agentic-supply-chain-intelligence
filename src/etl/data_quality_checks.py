import pandas as pd

df = pd.read_csv("data/processed/clean_candy_sales.csv")

print("\n========================")
print("DATA QUALITY REPORT")
print("========================")

print("\nRow Count")
print(len(df))

print("\nMissing Values")
print(df.isnull().sum().sum())

print("\nDuplicate Rows")
print(df.duplicated().sum())

print("\nNegative Sales")
print((df["SALES"] < 0).sum())

print("\nNegative Profit")
print((df["GROSS_PROFIT"] < 0).sum())

print("\nNegative Cost")
print((df["COST"] < 0).sum())

print("\nInvalid Shipping Days")
print((df["SHIPPING_DAYS"] < 0).sum())

print("\nProfit Margin > 100%")
print((df["PROFIT_MARGIN"] > 1).sum())

print("\nUnique Orders")
print(df["ORDER_ID"].nunique())

print("\nUnique Customers")
print(df["CUSTOMER_ID"].nunique())

print("\nUnique Products")
print(df["PRODUCT_ID"].nunique())

print("\n========================")
print("QUALITY CHECK COMPLETE")
print("========================")