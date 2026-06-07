import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer

DATA_PATH = "data/processed/clean_candy_sales.csv"
CHROMA_PATH = "vector_store/policy_chroma"

df = pd.read_csv(DATA_PATH)


# ------------------
# KPI AGENT
# ------------------

def kpi_agent():

    return {

        "revenue": float(round(df["SALES"].sum(), 2)),

        "profit": float(round(df["GROSS_PROFIT"].sum(), 2)),

        "orders": int(df["ORDER_ID"].nunique()),

        "customers": int(df["CUSTOMER_ID"].nunique())

    }


# ------------------
# RISK AGENT
# ------------------

def risk_agent():

    return {

        "revenue_at_risk": float(round(df["REVENUE_AT_RISK"].sum(), 2)),

        "delay_rate": float(round(df["IS_DELAYED"].mean() * 100, 2))

    }


# ------------------
# POLICY AGENT
# ------------------

def policy_agent(question):

    model = SentenceTransformer("all-MiniLM-L6-v2")

    client = chromadb.PersistentClient(path=CHROMA_PATH)

    collection = client.get_collection(
        name="supply_chain_policy"
    )

    query_embedding = model.encode([question]).tolist()[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=2
    )

    return results["documents"][0]


# ------------------
# RECOMMENDATION AGENT
# ------------------

def recommendation_agent(kpis, risks):

    recommendations = []

    if risks["delay_rate"] > 15:
        recommendations.append(
            "Delay rate exceeds 15%. Review logistics operations."
        )

    if risks["revenue_at_risk"] > 10000:
        recommendations.append(
            "Revenue at risk is significant. Prioritize delayed high-value orders."
        )

    if not recommendations:
        recommendations.append(
            "Operational metrics are within acceptable thresholds."
        )

    return recommendations


# ------------------
# ORCHESTRATOR
# ------------------

def main():

    print("\nOpsPilot Multi-Agent Copilot")

    question = input("\nAsk a business question: ")

    kpis = kpi_agent()
    risks = risk_agent()
    policy = policy_agent(question)
    recommendations = recommendation_agent(
        kpis,
        risks
    )

    print("\n========== KPI AGENT ==========")
    print(kpis)

    print("\n========== RISK AGENT ==========")
    print(risks)

    print("\n========== POLICY AGENT ==========")
    for item in policy:
        print("\n---")
        print(item)

    print("\n========== RECOMMENDATIONS ==========")
    for item in recommendations:
        print(f"- {item}")


if __name__ == "__main__":
    main()