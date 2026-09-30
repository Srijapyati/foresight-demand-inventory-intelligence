# Project FORESIGHT – AI-Powered Demand & Inventory Intelligence Platform

**Project FORESIGHT** is an enterprise-grade demand forecasting, risk management, and inventory optimization analytics platform designed for retail and supply chain organizations (inspired by **NorthBay Living**). 

The platform bridges predictive machine learning with dynamic operational decision-making, providing C-suite executives, inventory planners, and supply chain managers with actionable insights to prevent stockouts, eliminate overstock capital lockup, and streamline procurement.

---

## 🌟 Key Features & Dashboard Modules

The application is structured into **16 comprehensive views**, covering all Power BI dashboard specifications and executive deck requirements:

1. **🏠 Home & System Status**: Hero overview, health checks, platform telemetry.
2. **📊 Company Overview**: Top-level executive metrics ($259.81M+ revenue, profit margins, inventory turnover, 12-month sales trends).
3. **📈 Sales Analytics**: Deep-dive into gross margins, ASP, category revenue splits, and monthly trends.
4. **📦 Product Details**: SKU-level revenue, units sold, gross margin %, and stock risk indicators.
5. **🏷️ Category Performance**: Category growth YoY %, revenue contribution %, top subcategories.
6. **🏬 Inventory Dashboard**: On-hand vs on-order units, inventory value, Days of Cover, EOQ analysis.
7. **⚠️ Stock Risk Dashboard**: Stockout SKUs, critical safety stock breaches, daily demand at risk.
8. **🚨 Overstock Dashboard**: Dead stock tracking, excess inventory units & financial holding costs.
9. **🏷️ Promotion Analysis**: Promo revenue, discount %, volume uplift (77.89%), promo vs non-promo comparisons.
10. **📅 Seasonality Center**: Q4 holiday peak analysis, seasonal demand matrix, monthly demand patterns.
11. **🔮 Demand Forecasting Center**: Time-series ML forecasting (Ridge Regressor, Random Forest, Holt-Winters) with 14-90 day future horizons, MAPE, and RMSE metrics.
12. **👥 Customer & Business Insights**: 7-day & 30-day moving averages, customer segment distributions.
13. **🎯 Recommendation Engine & Action Matrix**: Dynamic **REORDER** vs **OVERSTOCK** executive matrix and inventory value at risk.
14. **🎛️ What-If Scenario Simulator**: Interactive sliders for demand surges, supplier lead time delays, and promotional discounts to model real-time risk exposure.
15. **🔔 Alerts Center**: Real-time automated alerts categorized by severity (Critical, High, Medium).
16. **📑 Executive Presentation**: Interactive 8-slide deck covering Business Problem, Client Background, Dataset, Preprocessing, EDA, Model Architecture, Metrics, and ROI.

---

## 🛠️ Data & Machine Learning Engine

- **Dataset**: Pre-configured with transaction data modeled after the **Online Retail II UCI Dataset** (2009-12-01 to 2011-12-09), featuring 25,000+ orders across 20 core SKUs in 5 major categories.
- **Forecasting Models**:
  - **Ridge Regressor & Random Forest**: Uses time-series feature engineering including day-of-week, month, day-of-year vectors, lag features (1, 7, 14, 28 days), and rolling window averages (7, 14, 30 days).
  - **Fallback Model**: Exponential Smoothing (Holt-Winters) for sparse or newly launched SKUs.
- **Inventory & Risk Mathematics**:
  - **Reorder Point (ROP)**: $ROP = (d \times L) + SS$
  - **Safety Stock (SS)**: $SS = Z \times \sigma_d \times \sqrt{L}$
  - **Economic Order Quantity (EOQ)**: $EOQ = \sqrt{\frac{2 \cdot D \cdot S}{H}}$
  - **Days of Cover (DOC)**: $DOC = \frac{\text{Current Stock}}{\text{Average Daily Demand}}$

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.9+
- `pip` package manager

### 1. Installation
Clone or navigate to the project directory and install the required dependencies:
```bash
cd zidio
pip install -r requirements.txt
```

### 2. Generate Data (Optional - Auto-generates on first launch)
To re-generate or reset the dataset:
```bash
python data/generate_data.py
```

### 3. Run the Streamlit Application
```bash
streamlit run app.py
```

The application will open automatically in your browser at `http://localhost:8501`.

---

## 📂 Project Architecture

```
zidio/
├── app.py                      # Main Streamlit Router & Sidebar Filter Config
├── requirements.txt            # Python Dependencies
├── README.md                   # Project Documentation
├── data/
│   ├── generate_data.py        # Dataset Generator Script
│   ├── raw_transactions.csv    # Transactional Sales Data
│   └── inventory_master.csv    # Inventory & Stock Master
├── src/
│   ├── __init__.py
│   ├── data_loader.py          # Cached Data Loader & Filters
│   ├── forecast_engine.py      # ML Demand Forecasting Engine
│   ├── risk_engine.py          # Inventory Math & Risk Calculations
│   └── style_helper.py         # Custom CSS Dark Theme & UI Cards
└── views/
    ├── home.py
    ├── company_overview.py
    ├── sales_performance.py
    ├── product_performance.py
    ├── category_performance.py
    ├── inventory_health.py
    ├── stock_risk.py
    ├── overstock.py
    ├── promotion_analysis.py
    ├── seasonality.py
    ├── forecast.py
    ├── customer_insights.py
    ├── recommendation.py
    ├── what_if_simulator.py
    ├── alerts_center.py
    └── executive_presentation.py
```
