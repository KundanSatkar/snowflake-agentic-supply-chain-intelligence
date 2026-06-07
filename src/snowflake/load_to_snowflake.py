from dotenv import load_dotenv
import os
from pathlib import Path
import snowflake.connector

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

CSV_PATH = PROJECT_ROOT / "data" / "processed" / "clean_candy_sales.csv"
STAGE_NAME = "CANDY_SALES_STAGE"
TABLE_NAME = "RAW_CANDY_SALES"

conn = snowflake.connector.connect(
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA"),
    role=os.getenv("SNOWFLAKE_ROLE"),
)

cursor = conn.cursor()

try:
    print("Connected to Snowflake.")

    cursor.execute(f"CREATE OR REPLACE STAGE {STAGE_NAME}")
    print(f"Stage created: {STAGE_NAME}")

    cursor.execute(f"PUT file://{CSV_PATH.resolve()} @{STAGE_NAME} AUTO_COMPRESS=TRUE")
    print("CSV uploaded to Snowflake stage.")

    cursor.execute(f"TRUNCATE TABLE {TABLE_NAME}")
    print(f"Table truncated: {TABLE_NAME}")

    copy_sql = f"""
    COPY INTO {TABLE_NAME}
    FROM @{STAGE_NAME}/clean_candy_sales.csv.gz
    FILE_FORMAT = (
        TYPE = CSV
        FIELD_OPTIONALLY_ENCLOSED_BY = '"'
        SKIP_HEADER = 1
    )
    ON_ERROR = 'ABORT_STATEMENT';
    """

    cursor.execute(copy_sql)
    print("Data loaded into Snowflake table.")

    cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
    row_count = cursor.fetchone()[0]
    print(f"Final row count in Snowflake: {row_count}")

finally:
    cursor.close()
    conn.close()
    print("Snowflake connection closed.")
