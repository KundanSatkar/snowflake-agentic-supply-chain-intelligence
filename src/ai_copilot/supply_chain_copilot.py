import pandas as pd
from pathlib import Path

DATA_PATH = Path("data/processed/clean_candy_sales.csv")
POLICY_PATH = Path("data/synthetic_docs/supply_chain_policy.md")


def load_data():
    return pd.read_csv(DATA_PATH)


def load_policy():
    return POLICY_PATH.read_text()


def get_business_context(df):
    total_revenue = df["SALES"].sum()
    total_profit = df["GROSS_PROFIT"].sum()
    total_orders = df["ORDER_ID"].nunique()
    total_customers = df["CUSTOMER_ID"].nunique()
    revenue_at_risk = df["REVENUE_AT_RISK"].sum()
    delay_rate = df["IS_DELAYED"].mean() * 100

    top_region = df.groupby("REGION")["SALES"].sum().sort_values(ascending=False)
    top_products = df.groupby("PRODUCT_NAME")["SALES"].sum().sort_values(ascending=False).head(5)
    delay_by_region = df.groupby("REGION")["IS_DELAYED"].mean().sort_values(ascending=False) * 100
    risk_by_region = df.groupby("REGION")["REVENUE_AT_RISK"].sum().sort_values(ascending=False)

    context = f"""
BUSINESS KPI CONTEXT

Total Revenue: ${total_revenue:,.2f}
Total Profit: ${total_profit:,.2f}
Total Orders: {total_orders:,}
Total Customers: {total_customers:,}
Revenue at Risk: ${revenue_at_risk:,.2f}
Overall Delay Rate: {delay_rate:.2f}%

Revenue by Region:
{top_region.to_string()}

Top Products by Revenue:
{top_products.to_string()}

Delay Rate by Region:
{delay_by_region.round(2).to_string()}

Revenue at Risk by Region:
{risk_by_region.to_string()}
"""
    return context


def get_relevant_policy(question, policy_text):
    question_lower = question.lower()

    sections = policy_text.split("##")
    relevant_sections = []

    for section in sections:
        section_lower = section.lower()

        if "delay" in question_lower and "delivery" in section_lower:
            relevant_sections.append(section)

        if "risk" in question_lower and "revenue" in section_lower:
            relevant_sections.append(section)

        if "region" in question_lower and "regional" in section_lower:
            relevant_sections.append(section)

        if "product" in question_lower and "product" in section_lower:
            relevant_sections.append(section)

        if "escalation" in question_lower and "escalation" in section_lower:
            relevant_sections.append(section)

    if not relevant_sections:
        return policy_text

    return "\n\n".join(relevant_sections)


def generate_executive_answer(question, business_context, policy_context):
    answer = f"""
QUESTION:
{question}

DATA-DRIVEN ANSWER:
Based on the current supply chain analytics data, the system reviewed revenue, profit, delay risk, product performance, and revenue-at-risk metrics.

BUSINESS CONTEXT USED:
{business_context}

POLICY CONTEXT USED:
{policy_context}

EXECUTIVE RECOMMENDATION:
1. Prioritize regions and products with high revenue exposure.
2. Review delayed shipments because they directly contribute to revenue at risk.
3. Escalate high-value delayed orders to operations leadership.
4. Continue monitoring product and regional trends through the dashboard.
"""
    return answer


def main():
    df = load_data()
    policy_text = load_policy()
    business_context = get_business_context(df)

    print("\nOpsPilot AI Supply Chain Copilot")
    print("Type 'exit' to quit.")

    while True:
        question = input("\nAsk a business question: ")

        if question.lower() == "exit":
            print("Goodbye.")
            break

        policy_context = get_relevant_policy(question, policy_text)
        answer = generate_executive_answer(
            question,
            business_context,
            policy_context
        )

        print("\nAnswer:")
        print(answer)


if __name__ == "__main__":
    main()