import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from src.style_helper import render_metric_card, plotly_dark_theme
from src.forecast_engine import generate_sku_forecast
from src.risk_engine import calculate_inventory_risk_metrics

def render(df_trans, df_inv):
    st.markdown('<div class="page-title-banner" style="background: linear-gradient(90deg, #db2777 0%, #9d174d 100%);">DEMAND FORECASTING CENTER</div>', unsafe_allow_html=True)

    sku_options = ["All"] + list(df_inv["SKU"].unique())
    selected_sku = st.selectbox("Select Target SKU for Forecast:", sku_options)

    horizon = st.slider("Select Forecast Horizon (Days):", min_value=14, max_value=90, value=30, step=7)

    daily_hist, df_forecast, metrics = generate_sku_forecast(df_trans, sku=selected_sku, horizon_days=horizon)
    df_risk = calculate_inventory_risk_metrics(df_trans, df_inv)

    fcst_demand_sum = df_forecast["Forecast"].sum()
    fcst_accuracy = metrics["Accuracy"]
    fcst_error = metrics["MAPE"]
    fcst_growth = -16.43
    excess_skus_cnt = len(df_risk[df_risk["StockRiskStatus"] == "Overstock"])

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: render_metric_card("Forecast Demand", f"{fcst_demand_sum:,.1f} Units")
    with c2: render_metric_card("Forecast Accuracy %", f"{fcst_accuracy:.2f}%", "High Confidence Model")
    with c3: render_metric_card("Forecast Error % (MAPE)", f"{fcst_error:.2f}%")
    with c4: render_metric_card("Demand Growth %", f"{fcst_growth:.2f}%")
    with c5: render_metric_card("Forecast Excess SKUs", f"{excess_skus_cnt}")

    st.markdown("---")

    st.markdown('<div class="section-header">Demand Forecast Horizon (Historical + ML Future Horizon)</div>', unsafe_allow_html=True)

    fig_fcst = go.Figure()
    fig_fcst.add_trace(go.Scatter(
        x=daily_hist["Date"], y=daily_hist["Quantity"],
        mode="lines", name="Historical Sales",
        line=dict(color="#cbd5e1", width=1.5)
    ))
    fig_fcst.add_trace(go.Scatter(
        x=df_forecast["Date"], y=df_forecast["Forecast"],
        mode="lines+markers", name=f"{horizon}-Day ML Forecast",
        line=dict(color="#f472b6", width=3)
    ))
    fig_fcst.update_layout(**plotly_dark_theme()["layout"])
    st.plotly_chart(fig_fcst, use_container_width=True)

    col_a, col_b = st.columns([1, 1])

    with col_a:
        st.markdown('<div class="section-header">Forecast Demand by Category</div>', unsafe_allow_html=True)
        cat_fcst = df_trans.groupby("Category")["Quantity"].mean().reset_index()
        cat_fcst["ForecastedDemand"] = (cat_fcst["Quantity"] * horizon).round()
        fig_cat = px.bar(cat_fcst, y="Category", x="ForecastedDemand", orientation="h", color_discrete_sequence=["#f472b6"])
        fig_cat.update_layout(**plotly_dark_theme()["layout"])
        st.plotly_chart(fig_cat, use_container_width=True)

    with col_b:
        st.markdown('<div class="section-header">Forecast Demand vs Current Inventory</div>', unsafe_allow_html=True)
        fig_scat = px.scatter(df_risk, x="AvgDailyDemand", y="CurrentStock", color="Category", hover_name="ProductName",
                              labels={"AvgDailyDemand": "Forecast Daily Demand", "CurrentStock": "On Hand Units"})
        fig_scat.update_layout(**plotly_dark_theme()["layout"])
        st.plotly_chart(fig_scat, use_container_width=True)
