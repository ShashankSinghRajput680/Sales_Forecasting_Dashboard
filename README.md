# 📈 Sales Forecasting & Demand Intelligence Dashboard

An end-to-end Data Science project that analyzes historical retail sales data, forecasts future demand, detects unusual sales patterns, and segments products into demand-based groups. The project also includes an interactive Streamlit dashboard for business users to explore insights and support inventory planning.

---

## 🚀 Live Demo

🌐 **Streamlit App:**  
https://salesforecastingdashboard-ke7ptcayswzez6fuvjx4an.streamlit.app/

📂 **GitHub Repository:**  
https://github.com/ShashankSinghRajput680/Sales_Forecasting_Dashboard

---

## 📌 Project Overview

Retail businesses need accurate sales forecasts to optimize inventory, reduce stock shortages, and improve supply chain planning.

This project combines **time series forecasting**, **anomaly detection**, **machine learning**, and **interactive dashboards** to provide business-friendly insights for decision-makers.

---

## ✨ Features

### 📊 Sales Overview Dashboard
- Total Sales, Orders, and Average Order Value
- Year-wise Sales Analysis
- Monthly Sales Trend
- Interactive Region and Category Filters

### 📈 Forecast Explorer
- Forecast based on Overall Sales, Category, or Region
- Select forecast horizon (1–3 months)
- Forecast visualization
- Forecast values with prediction intervals
- Model performance metrics (MAE, RMSE, MAPE)

### 🚨 Sales Anomaly Report
- Weekly anomaly detection using Isolation Forest
- Interactive anomaly visualization
- Summary table of detected anomalies
- Downloadable anomaly report

### 📦 Product Demand Segmentation
- Product clustering using K-Means
- PCA-based cluster visualization
- Demand segment mapping
- Cluster summary statistics
- Inventory stocking recommendations

---

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Plotly
- Streamlit
- Prophet
- Scikit-learn
- Statsmodels
- XGBoost
- Git & GitHub

---

## 🤖 Machine Learning Techniques

- Time Series Forecasting (Prophet)
- Isolation Forest (Anomaly Detection)
- K-Means Clustering
- Principal Component Analysis (PCA)
- StandardScaler
- Time Series Feature Engineering

---

## 📂 Project Structure

```
Sales_Forecasting_Dashboard/
│
├── app.py
├── train.csv
├── requirements.txt
├── README.md
│
├── pages/
│   ├── 1_Sales_Overview.py
│   ├── 2_Forecast_Explorer.py
│   ├── 3_Anomaly_Report.py
│   └── 4_Product_Demand_Segments.py
│
├── utils/
│   ├── data_loader.py
│   ├── forecast.py
│   ├── anomaly.py
│   └── clustering.py
│
└── assets/
```

---

## 📊 Dashboard Preview

### Sales Overview

<img src="charts/sales_overview.png" width="900">

### Forecast Explorer

<img src="charts/forecast.png" width="900">

### Sales Anomaly Report

<img src="charts/anomaly.png" width="900">

### Product Demand Segmentation

<img src="charts/product_segmentation.png" width="900">

---

## 📈 Model Performance

| Metric | Value |
|---------|------:|
| MAE | 5,770 |
| RMSE | 7,272 |
| MAPE | 14.48% |

---

## 📌 Business Insights

- Sales showed a steady growth trend from 2015 to 2018.
- The forecasting model provides reliable short-term sales predictions.
- 11 anomalous sales weeks (5.3%) were detected for further business investigation.
- Products were segmented into four demand groups to support inventory planning.
- Interactive dashboards enable business users to monitor sales and make informed decisions.

---

## ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/ShashankSinghRajput680/Sales_Forecasting_Dashboard.git
```

Move into the project directory

```bash
cd Sales_Forecasting_Dashboard
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run app.py
```

---

## 👨‍💻 Author

**Shashank Singh Rajput**

- GitHub: https://github.com/ShashankSinghRajput680

---

## 📄 License

This project was developed as part of the **XYlofy AI Data Science Internship** for educational and portfolio purposes.
