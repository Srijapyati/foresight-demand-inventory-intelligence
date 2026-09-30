import streamlit as st
import pandas as pd
from src.style_helper import render_metric_card
from src.risk_engine import calculate_inventory_risk_metrics

def render(df_trans, df_inv):
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(255, 107, 0, 0.15) 0%, rgba(30, 27, 75, 0.6) 100%); border: 1px solid rgba(255, 107, 0, 0.3); border-radius: 16px; padding: 28px; margin-bottom: 24px;">
        <h1 style="color: #ffffff; margin-bottom: 8px; font-weight: 800;">⚡ FORESIGHT</h1>
        <p style="color: #ff9d42; font-size: 1.1rem; font-weight: 600; margin-bottom: 12px;">Intelligence at scale.</p>
        <p style="color: #cbd5e1; font-size: 1.0rem; max-width: 800px; line-height: 1.6;">
            Transform your raw retail transaction data into actionable supply chain intelligence with NorthBay Living's advanced predictive demand & inventory analytics platform.
        </p>
    </div>
    """, unsafe_allow_html=True)

    df_risk = calculate_inventory_risk_metrics(df_trans, df_inv)

    tot_rev = df_trans["TotalRevenue"].sum()
    tot_skus = len(df_inv)
    stockouts = len(df_risk[df_risk["StockRiskStatus"] == "Stockout"])
    overstock = len(df_risk[df_risk["StockRiskStatus"] == "Overstock"])

    c1, c2, c3, c4 = st.columns(4)
    with c1: render_metric_card("System Status", "OPTIMAL PERFORMANCE", "Edge ML Engine Active", "positive")
    with c2: render_metric_card("Total Revenue (2009-2011)", f"${tot_rev/1e6:.2f}M", "25,000+ Transactions")
    with c3: render_metric_card("Total SKUs Managed", f"{tot_skus} SKUs", "5 Categories")
    with c4: render_metric_card("Stock Risk Exposure", f"{stockouts} Stockouts / {overstock} Overstock", "Action Recommended", "warning")

    st.markdown("---")

    st.markdown("### 🛠️ Platform Capability Modules")
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown("""
        #### 📈 Executive Dashboards
        - **Company Overview**: High-level C-suite metrics, profit & turnover.
        - **Sales Performance**: Revenue by subcategory & YoY trends.
        - **Category & Product Performance**: SKU drilldown & margin matrix.
        """)
    with m2:
        st.markdown("""
        #### 📦 Inventory & Risk Analytics
        - **Inventory Health**: Days of cover & EOQ calculation.
        - **Stock Risk**: Stockout risk matrix & daily demand exposure.
        - **Overstock Dashboard**: Dead stock tracking & excess holding cost.
        """)
    with m3:
        st.markdown("""
        #### 🔮 Predictive AI & Simulation
        - **Demand Forecast**: Machine Learning 30-90 day SKU forecast.
        - **What-If Simulator**: Real-time demand surge & lead time shock modeling.
        - **Executive Deck**: 8-slide strategic presentation.
        """)
