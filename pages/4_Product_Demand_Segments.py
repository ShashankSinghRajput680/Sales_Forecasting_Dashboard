import streamlit as st
import pandas as pd
import plotly.express as px

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

from utils.data_loader import load_data

st.title("Product Demand Segmentation")

df = load_data()

# -----------------------------
# Feature Engineering
# -----------------------------

total_sales = (
    df.groupby("Sub-Category")["Sales"]
    .sum()
    .reset_index(name="Total Sales")
)

avg_order = (
    df.groupby("Sub-Category")["Sales"]
    .mean()
    .reset_index(name="Average Order Value")
)

volatility = (
    df.groupby("Sub-Category")["Sales"]
    .std()
    .reset_index(name="Sales Volatility")
)

yearly = (
    df.groupby(
        ["Sub-Category", df["Order Date"].dt.year]
    )["Sales"]
    .sum()
    .reset_index()
)

growth = []

for sub in yearly["Sub-Category"].unique():

    temp = yearly[yearly["Sub-Category"] == sub]

    growth.append(
        [
            sub,
            temp["Sales"].pct_change().mean()
        ]
    )

growth = pd.DataFrame(
    growth,
    columns=["Sub-Category", "Growth Rate"]
)

cluster_data = (
    total_sales
    .merge(avg_order)
    .merge(volatility)
    .merge(growth)
)

cluster_data["Growth Rate"] = cluster_data["Growth Rate"].fillna(0)

# -----------------------------
# Clustering
# -----------------------------

features = cluster_data[
    [
        "Total Sales",
        "Average Order Value",
        "Sales Volatility",
        "Growth Rate"
    ]
]

scaled = StandardScaler().fit_transform(features)

kmeans = KMeans(
    n_clusters=4,
    random_state=42,
    n_init=10
)

cluster_data["Cluster"] = kmeans.fit_predict(scaled)

# Friendly Names

cluster_names = {
    0: "Moderate Demand",
    1: "Stable Demand",
    2: "High Demand",
    3: "Rapid Growth"
}

cluster_data["Demand Segment"] = (
    cluster_data["Cluster"]
    .map(cluster_names)
)

# -----------------------------
# KPI Cards
# -----------------------------

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Total Segments",
    cluster_data["Sub-Category"].nunique()
)

c2.metric(
    "High Demand",
    (cluster_data["Demand Segment"]=="High Demand").sum()
)

c3.metric(
    "Stable Demand",
    (cluster_data["Demand Segment"]=="Stable Demand").sum()
)

c4.metric(
    "Rapid Growth",
    (cluster_data["Demand Segment"]=="Rapid Growth").sum()
)

st.divider()

# -----------------------------
# PCA Visualization
# -----------------------------

pca = PCA(n_components=2)

components = pca.fit_transform(scaled)

cluster_data["PC1"] = components[:,0]
cluster_data["PC2"] = components[:,1]

fig = px.scatter(
    cluster_data,
    x="PC1",
    y="PC2",
    color="Demand Segment",
    text="Sub-Category",
    title="Product Demand Segments"
)

fig.update_layout(
    height=550
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------
# Cluster Summary
# -----------------------------

st.subheader("Cluster Summary")

summary = (
    cluster_data
    .groupby("Demand Segment")[
        [
            "Total Sales",
            "Growth Rate",
            "Sales Volatility",
            "Average Order Value"
        ]
    ]
    .mean()
    .round(2)
)

st.dataframe(
    summary,
    use_container_width=True
)

# -----------------------------
# Product Mapping
# -----------------------------

st.subheader("Product Demand Cluster Mapping")

st.dataframe(
    cluster_data[
        [
            "Sub-Category",
            "Demand Segment"
        ]
    ],
    use_container_width=True
)

# -----------------------------
# Recommendations
# -----------------------------

st.subheader("Stocking Recommendations")

recommendations = {

"High Demand":
"Increase inventory before peak demand periods. Maintain strong stock availability.",

"Stable Demand":
"Maintain consistent inventory levels and regular replenishment.",

"Moderate Demand":
"Maintain moderate inventory with periodic monitoring.",

"Rapid Growth":
"Demand is increasing rapidly. Monitor sales closely and increase stock gradually."

}

for segment, recommendation in recommendations.items():

    st.markdown(f"### {segment}")

    st.info(recommendation)