import pandas as pd
from pathlib import Path

DATA_PATH = Path("data/processed/clean_candy_sales.csv")
POLICY_PATH = Path("data/synthetic_docs/supply_chain_policy.md")


def load_data():
    return pd.read_csv(DATA_PATH)


def load_policy():
    return POLICY_PATH.read_text()


def get_kpi_summary(df):
    total_revenue = df["SALES"].sum()
    total_profit = df["GROSS_PROFIT"].sum()
    total_orders = df["ORDER_ID"].nunique()
    total_customers = df["CUSTOMER_ID"].nunique()
    revenue_at_risk = df["REVENUE_AT_RISK"].sum()
    delay_rate = df["IS_DELAYED"].mean() * 100

    return {
        "total_revenue": total_revenue,
        "total_profit": total_profit,
        "total_orders": total_orders,
        "total_customers": total_customers,
        "revenue_at_risk": revenue_at_risk,
        "delay_rate": delay_rate,
    }


def answer_question(question, df, policy_text):
    question_lower = question.lower()

    if "revenue" in question_lower and "region" in question_lower:
        result = (
            df.groupby("REGION")["SALES"]
            .sum()
            .sort_values(ascending=False)
        )
        return f"Revenue by region:\n{result}"

    if "profit" in question_lower and "division" in question_lower:
        result = (
            df.groupby("DIVISION")["GROSS_PROFIT"]
            .sum()
            .sort_values(ascending=False)
        )
        return f"Profit by division:\n{result}"

    if "product" in question_lower:
        result = (
            df.groupby("PRODUCT_NAME")["SALES"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )
        return f"Top products by revenue:\n{result}"

    if "delay" in question_lower or "delayed" in question_lower:
        result = (
            df.groupby("REGION")["IS_DELAYED"]
            .mean()
            .sort_values(ascending=False) * 100
        )
        return f"Delay rate by region:\n{result.round(2)}%"

    if "risk" in question_lower:
        result = (
            df.groupby("REGION")["REVENUE_AT_RISK"]
            .sum()
            .sort_values(ascending=False)
        )
        return f"Revenue at risk by region:\n{result}"

    if "policy" in question_lower or "escalation" in question_lower:
        return f"Relevant policy context:\n\n{policy_text}"

    summary = get_kpi_summary(df)

    return f"""
OpsPilot AI Summary:

Total Revenue: ${summary["total_revenue"]:,.2f}
Total Profit: ${summary["total_profit"]:,.2f}
Total Orders: {summary["total_orders"]:,}
Total Customers: {summary["total_customers"]:,}
Revenue at Risk: ${summary["revenue_at_risk"]:,.2f}
Delay Rate: {summary["delay_rate"]:.2f}%

Recommendation:
Review high-risk regions and delayed shipments first, then prioritize products with high revenue impact.
"""


def main():
    df = load_data()
    policy_text = load_policy()

    print("\nOpsPilot AI Supply Chain Copilot")
    print("Type 'exit' to quit.")

    while True:
        question = input("\nAsk a business question: ")

        if question.lower() == "exit":
            print("Goodbye.")
            break

        answer = answer_question(question, df, policy_text)
        print("\nAnswer:")
        print(answer)


if __name__ == "__main__":
    main()