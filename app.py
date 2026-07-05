import streamlit as st

st.set_page_config(
    page_title="Sales Forecasting Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Sales Forecasting Dashboard")

st.markdown(
"""
## Welcome

This dashboard demonstrates end-to-end sales analytics and forecasting using the Superstore Sales dataset.

### Features

- Sales Overview Dashboard
- Sales Forecasting
- Anomaly Detection
- Product Demand Segmentation

"""
)

