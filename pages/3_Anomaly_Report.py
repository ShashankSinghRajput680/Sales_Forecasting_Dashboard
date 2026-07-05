import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from sklearn.ensemble import IsolationForest

from utils.data_loader import load_data

# -----------------------------
# PAGE TITLE
# -----------------------------

st.title("Sales Anomaly Report")

# -----------------------------
# LOAD DATA
# -----------------------------

df = load_data()

# Weekly Sales
weekly_sales = (
    df.groupby(pd.Grouper(key="Order Date", freq="W"))["Sales"]
    .sum()
    .reset_index()
)

# -----------------------------
# ANOMALY DETECTION
# -----------------------------

model = IsolationForest(
    contamination=0.05,
    random_state=42
)

weekly_sales["Anomaly"] = model.fit_predict(
    weekly_sales[["Sales"]]
)

weekly_sales["Anomaly"] = weekly_sales["Anomaly"].map(
    {
        1: "Normal",
        -1: "Anomaly"
    }
)

anomalies = weekly_sales[
    weekly_sales["Anomaly"] == "Anomaly"
]

# -----------------------------
# KPI CARDS
# -----------------------------

c1, c2, c3 = st.columns(3)

c1.metric(
    "Total Weeks",
    len(weekly_sales)
)

c2.metric(
    "Detected Anomalies",
    len(anomalies)
)

c3.metric(
    "Anomaly Rate",
    f"{len(anomalies)/len(weekly_sales)*100:.1f}%"
)

st.divider()

# -----------------------------
# CHART
# -----------------------------

st.subheader("Weekly Sales Trend with Detected Anomalies")

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=weekly_sales["Order Date"],
        y=weekly_sales["Sales"],
        mode="lines",
        name="Weekly Sales",
        line=dict(width=2)
    )
)

fig.add_trace(
    go.Scatter(
        x=anomalies["Order Date"],
        y=anomalies["Sales"],
        mode="markers",
        marker=dict(
            color="red",
            size=11,
            symbol="diamond"
        ),
        name="Detected Anomalies"
    )
)

fig.update_layout(
    height=550,
    xaxis_title="Week",
    yaxis_title="Sales",
    legend_title="Legend"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# -----------------------------
# TABLE
# -----------------------------

st.subheader("Detected Anomalies")

display = anomalies[
    [
        "Order Date",
        "Sales"
    ]
].copy()

# Remove Time
display["Order Date"] = display["Order Date"].dt.strftime("%d-%m-%Y")

# Round Sales
display["Sales"] = display["Sales"].round(2)

st.dataframe(
    display,
    use_container_width=True
)

# -----------------------------
# DOWNLOAD BUTTON
# -----------------------------

csv = display.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Download Anomaly Report",
    data=csv,
    file_name="Sales_Anomaly_Report.csv",
    mime="text/csv"
)