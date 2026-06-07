from pathlib import Path

import pandas as pd


SHIP_DATE_OFFSET_DAYS = 2000


def find_project_root():
    candidates = []
    if "__file__" in globals():
        candidates.append(Path(__file__).resolve().parents[2])
    candidates.append(Path.cwd())

    for candidate in candidates:
        if (candidate / "data" / "raw" / "Candy_Sales.csv").exists():
            return candidate

    raise FileNotFoundError("Could not find data/raw/Candy_Sales.csv")


PROJECT_ROOT = find_project_root()
SALES_FILE = PROJECT_ROOT / "data" / "raw" / "Candy_Sales.csv"


def load_raw_sales(path=SALES_FILE):
    return pd.read_csv(path)


def prepare_sales(raw_data):
    prepared = raw_data.copy()
    prepared["Order Date"] = pd.to_datetime(prepared["Order Date"])
    prepared["Ship Date"] = pd.to_datetime(prepared["Ship Date"])

    raw_shipping_days = (prepared["Ship Date"] - prepared["Order Date"]).dt.days
    prepared["Raw Shipping Days"] = raw_shipping_days

    if raw_shipping_days.median() > 365:
        prepared["Ship Date"] = (
            prepared["Ship Date"]
            - pd.to_timedelta(SHIP_DATE_OFFSET_DAYS, unit="D")
        )

    prepared["Shipping Days"] = (
        prepared["Ship Date"] - prepared["Order Date"]
    ).dt.days
    return prepared


def print_report():
    print("\nRaw Date Sample Before Conversion")
    print(raw_sales[["Order Date", "Ship Date"]].head(20))

    print("\nAverage Shipping Days")
    print(sales["Shipping Days"].mean())

    print("\nMax Shipping Days")
    print(sales["Shipping Days"].max())

    print("\nMin Shipping Days")
    print(sales["Shipping Days"].min())

    print("\nTop 10 Shipping Times")
    print(
        sales[
            [
                "Order ID",
                "Order Date",
                "Ship Date",
                "Raw Shipping Days",
                "Shipping Days",
            ]
        ].head(10)
    )

    total_revenue = sales["Sales"].sum()
    total_profit = sales["Gross Profit"].sum()

    print("\nTotal Revenue")
    print(round(total_revenue, 2))

    print("\nTotal Profit")
    print(round(total_profit, 2))

    print("\nTotal Cost")
    print(round(sales["Cost"].sum(), 2))

    print("\nProfit Margin")
    print(f"{total_profit / total_revenue:.2%}")

    print("\nRevenue By Division")
    print(
        sales.groupby("Division")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    print("\nRevenue By Region")
    print(
        sales.groupby("Region")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    print("\nTop Products By Revenue")
    print(
        sales.groupby("Product Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )


raw_sales = load_raw_sales()
sales = prepare_sales(raw_sales)


if __name__ == "__main__":
    print_report()
