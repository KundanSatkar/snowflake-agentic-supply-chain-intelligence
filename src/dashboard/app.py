import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="OpsPilot AI",
    layout="wide"
)

df = pd.read_csv("data/processed/clean_candy_sales.csv")

# Convert dates
df["ORDER_DATE"] = pd.to_datetime(df["ORDER_DATE"])
df["CORRECTED_SHIP_DATE"] = pd.to_datetime(df["CORRECTED_SHIP_DATE"])

# KPI calculations
total_revenue = df["SALES"].sum()
total_profit = df["GROSS_PROFIT"].sum()
total_cost = df["COST"].sum()
profit_margin = total_profit / total_revenue
total_orders = df["ORDER_ID"].nunique()
total_customers = df["CUSTOMER_ID"].nunique()
avg_shipping_days = df["SHIPPING_DAYS"].mean()
delay_rate = df["IS_DELAYED"].mean() * 100
revenue_at_risk = df["REVENUE_AT_RISK"].sum()

st.title("🚀 OpsPilot AI")
st.subheader("Snowflake Supply Chain Intelligence Platform")

st.markdown(
    "Executive analytics dashboard for revenue, profitability, regional performance, "
    "product performance, shipping delays, and revenue risk."
)

# KPI cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Revenue", f"${total_revenue:,.0f}")
col2.metric("Profit", f"${total_profit:,.0f}")
col3.metric("Orders", f"{total_orders:,}")
col4.metric("Customers", f"{total_customers:,}")

col5, col6, col7, col8 = st.columns(4)
col5.metric("Cost", f"${total_cost:,.0f}")
col6.metric("Profit Margin", f"{profit_margin:.1%}")
col7.metric("Avg Shipping Days", f"{avg_shipping_days:.1f}")
col8.metric("Revenue at Risk", f"${revenue_at_risk:,.0f}")

st.markdown("---")

# Filters
st.sidebar.header("Filters")

selected_regions = st.sidebar.multiselect(
    "Select Region",
    options=sorted(df["REGION"].unique()),
    default=sorted(df["REGION"].unique())
)

selected_divisions = st.sidebar.multiselect(
    "Select Division",
    options=sorted(df["DIVISION"].unique()),
    default=sorted(df["DIVISION"].unique())
)

filtered_df = df[
    (df["REGION"].isin(selected_regions)) &
    (df["DIVISION"].isin(selected_divisions))
]

# Charts row 1
col_a, col_b = st.columns(2)

region_sales = (
    filtered_df.groupby("REGION")["SALES"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

fig_region = px.bar(
    region_sales,
    x="REGION",
    y="SALES",
    title="Revenue by Region",
    text_auto=".2s"
)
col_a.plotly_chart(fig_region, use_container_width=True)

division_profit = (
    filtered_df.groupby("DIVISION")["GROSS_PROFIT"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

fig_division = px.bar(
    division_profit,
    x="DIVISION",
    y="GROSS_PROFIT",
    title="Profit by Division",
    text_auto=".2s"
)
col_b.plotly_chart(fig_division, use_container_width=True)

# Charts row 2
col_c, col_d = st.columns(2)

product_sales = (
    filtered_df.groupby("PRODUCT_NAME")["SALES"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig_products = px.bar(
    product_sales,
    x="SALES",
    y="PRODUCT_NAME",
    orientation="h",
    title="Top 10 Products by Revenue",
    text_auto=".2s"
)
fig_products.update_layout(yaxis={"categoryorder": "total ascending"})
col_c.plotly_chart(fig_products, use_container_width=True)

shipping_by_mode = (
    filtered_df.groupby("SHIP_MODE")["SHIPPING_DAYS"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

fig_shipping = px.bar(
    shipping_by_mode,
    x="SHIP_MODE",
    y="SHIPPING_DAYS",
    title="Average Shipping Days by Ship Mode",
    text_auto=".2f"
)
col_d.plotly_chart(fig_shipping, use_container_width=True)

# Charts row 3
col_e, col_f = st.columns(2)

risk_by_region = (
    filtered_df.groupby("REGION")["REVENUE_AT_RISK"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

fig_risk = px.bar(
    risk_by_region,
    x="REGION",
    y="REVENUE_AT_RISK",
    title="Revenue at Risk by Region",
    text_auto=".2s"
)
col_e.plotly_chart(fig_risk, use_container_width=True)

monthly_revenue = (
    filtered_df.assign(MONTH=filtered_df["ORDER_DATE"].dt.to_period("M").astype(str))
    .groupby("MONTH")["SALES"]
    .sum()
    .reset_index()
)

fig_trend = px.line(
    monthly_revenue,
    x="MONTH",
    y="SALES",
    title="Monthly Revenue Trend",
    markers=True
)
col_f.plotly_chart(fig_trend, use_container_width=True)
st.subheader("Machine Learning Model: Delivery Delay Prediction")

ml_col1, ml_col2, ml_col3, ml_col4 = st.columns(4)

ml_col1.metric("Model Type", "Random Forest")
ml_col2.metric("Delay Recall", "87.77%")
ml_col3.metric("F1 Score", "46.24%")
ml_col4.metric("Use Case", "Early Warning")

st.info(
    "The delay prediction model is optimized for high recall, meaning it is designed "
    "to catch as many risky delayed shipments as possible. In operations, missing a "
    "high-risk shipment is usually more costly than flagging extra orders for review."
)
st.markdown("---")

st.subheader("Detailed Sales Data")
st.dataframe(filtered_df.head(100))