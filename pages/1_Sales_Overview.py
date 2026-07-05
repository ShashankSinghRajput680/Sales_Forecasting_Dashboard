import streamlit as st
import pandas as pd
import plotly.express as px

import utils.data_loader as dl

st.title("Sales Overview Dashboard")

# Load Data
df = dl.load_data()

# ---------------- Sidebar ----------------

st.sidebar.header("Filters")

regions = st.sidebar.multiselect(
    "Select Region",
    options=sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

categories = st.sidebar.multiselect(
    "Select Category",
    options=sorted(df["Category"].unique()),
    default=sorted(df["Category"].unique())
)

filtered_df = df[
    (df["Region"].isin(regions)) &
    (df["Category"].isin(categories))
]

# ---------------- KPI Cards ----------------

total_sales = filtered_df["Sales"].sum()

total_orders = filtered_df["Order ID"].nunique()

avg_sales = filtered_df["Sales"].mean()

c1, c2, c3 = st.columns(3)

c1.metric("Total Sales", f"${total_sales:,.0f}")
c2.metric("Orders", total_orders)
c3.metric("Average Order Value", f"${avg_sales:,.2f}")

st.divider()

# ---------------- Total Sales by Year ----------------

sales_year = (
    filtered_df
    .groupby("Year")["Sales"]
    .sum()
    .reset_index()
)

fig = px.bar(
    sales_year,
    x="Year",
    y="Sales",
    text_auto=".2s",
    title="Total Sales by Year"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- Monthly Trend ----------------

monthly_sales = (
    filtered_df
    .groupby(pd.Grouper(key="Order Date", freq="ME"))["Sales"]
    .sum()
    .reset_index()
)

fig2 = px.line(
    monthly_sales,
    x="Order Date",
    y="Sales",
    markers=True,
    title="Monthly Sales Trend"
)

st.plotly_chart(fig2, use_container_width=True)