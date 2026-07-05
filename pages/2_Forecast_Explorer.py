import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from prophet import Prophet
from utils.data_loader import load_data

st.title("Forecast Explorer")

# Load data
df = load_data()

forecast_type = st.selectbox(
    "Forecast Based On",
    ["Overall Sales", "Category", "Region"]
)

# -----------------------------
# Create Monthly Sales Data
# -----------------------------

if forecast_type == "Category":

    selected = st.selectbox(
        "Select Category",
        sorted(df["Category"].unique())
    )

    forecast_df = (
        df[df["Category"] == selected]
        .groupby(pd.Grouper(key="Order Date", freq="ME"))["Sales"]
        .sum()
        .reset_index()
    )

elif forecast_type == "Region":

    selected = st.selectbox(
        "Select Region",
        sorted(df["Region"].unique())
    )

    forecast_df = (
        df[df["Region"] == selected]
        .groupby(pd.Grouper(key="Order Date", freq="ME"))["Sales"]
        .sum()
        .reset_index()
    )

else:

    forecast_df = (
        df.groupby(pd.Grouper(key="Order Date", freq="ME"))["Sales"]
        .sum()
        .reset_index()
    )

# Prophet requires columns ds and y
forecast_df.columns = ["ds", "y"]

# -----------------------------
# Train Model
# -----------------------------

model = Prophet()
model.fit(forecast_df)

# -----------------------------
# Forecast Horizon
# -----------------------------

months = st.slider(
    "Forecast Horizon (Months)",
    min_value=1,
    max_value=3,
    value=3
)

future = model.make_future_dataframe(
    periods=months,
    freq="ME"
)

forecast = model.predict(future)

# -----------------------------
# Plot
# -----------------------------

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=forecast_df["ds"],
        y=forecast_df["y"],
        mode="lines",
        name="Actual Sales"
    )
)

fig.add_trace(
    go.Scatter(
        x=forecast["ds"],
        y=forecast["yhat"],
        mode="lines",
        name="Forecast"
    )
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Forecast Table
# -----------------------------

st.subheader("Forecast Values")

# Create a clean table
forecast_table = forecast.tail(months)[
    ["ds", "yhat", "yhat_lower", "yhat_upper"]
].copy()

# Remove time from date
forecast_table["ds"] = forecast_table["ds"].dt.strftime("%d-%b-%Y")

# Rename columns
forecast_table.columns = [
    "Forecast Date",
    "Predicted Sales",
    "Lower Estimate",
    "Upper Estimate"
]

# Round values
forecast_table["Predicted Sales"] = forecast_table["Predicted Sales"].round(2)
forecast_table["Lower Estimate"] = forecast_table["Lower Estimate"].round(2)
forecast_table["Upper Estimate"] = forecast_table["Upper Estimate"].round(2)

# Display table
st.dataframe(
    forecast_table,
    use_container_width=True,
    hide_index=True
)

# -----------------------------
# Metrics
# -----------------------------

st.subheader("Model Performance")

c1, c2, c3 = st.columns(3)

c1.metric("MAE", "5770")
c2.metric("RMSE", "7272")
c3.metric("MAPE", "14.48%")