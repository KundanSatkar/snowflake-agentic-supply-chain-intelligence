import pandas as pd
from pathlib import Path


RAW_DATA_PATH = Path("data/raw/Candy_Sales.csv")
PROCESSED_DATA_PATH = Path("data/processed/clean_candy_sales.csv")


def load_sales_data(path: Path) -> pd.DataFrame:
    """Load raw candy sales data."""
    return pd.read_csv(path)


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Convert column names to Snowflake-friendly format."""
    df = df.copy()
    df.columns = (
        df.columns
        .str.strip()
        .str.upper()
        .str.replace(" ", "_")
        .str.replace("/", "_")
    )
    return df


def transform_dates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert date columns and correct shifted ship dates.

    The raw dataset ship dates are shifted several years forward.
    We calculate RAW_SHIPPING_DAYS first, then create a corrected ship date
    by subtracting 2000 days from the original ship date.
    """
    df = df.copy()

    df["ORDER_DATE"] = pd.to_datetime(df["ORDER_DATE"])
    df["SHIP_DATE"] = pd.to_datetime(df["SHIP_DATE"])

    df["RAW_SHIPPING_DAYS"] = (df["SHIP_DATE"] - df["ORDER_DATE"]).dt.days

    df["CORRECTED_SHIP_DATE"] = df["SHIP_DATE"] - pd.to_timedelta(2000, unit="D")

    df["SHIPPING_DAYS"] = (
        df["CORRECTED_SHIP_DATE"] - df["ORDER_DATE"]
    ).dt.days

    return df


def create_business_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Create business metrics used for analytics and ML."""
    df = df.copy()

    df["PROFIT_MARGIN"] = df["GROSS_PROFIT"] / df["SALES"]

    df["IS_DELAYED"] = (df["SHIPPING_DAYS"] > 5).astype(int)

    df["REVENUE_AT_RISK"] = df["SALES"] * df["IS_DELAYED"]

    return df


def save_processed_data(df: pd.DataFrame, path: Path) -> None:
    """Save cleaned dataset to processed folder."""
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


def main():
    print("Starting candy sales ETL transformation...")

    sales = load_sales_data(RAW_DATA_PATH)
    print(f"Loaded raw sales data: {sales.shape}")

    sales = clean_column_names(sales)
    print("Cleaned column names.")

    sales = transform_dates(sales)
    print("Transformed and corrected date fields.")

    sales = create_business_metrics(sales)
    print("Created business metrics.")

    save_processed_data(sales, PROCESSED_DATA_PATH)
    print(f"Saved processed data to: {PROCESSED_DATA_PATH}")
    print(f"Final processed shape: {sales.shape}")


if __name__ == "__main__":
    main()