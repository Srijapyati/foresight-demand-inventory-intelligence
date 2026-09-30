import streamlit as st
import pandas as pd
import plotly.express as px
from src.style_helper import render_metric_card, plotly_dark_theme
from src.risk_engine import calculate_inventory_risk_metrics

def render(df_trans, df_inv):
    st.markdown('<div class="page-title-banner" style="background: linear-gradient(90deg, #dc2626 0%, #991b1b 100%);">STOCK RISK</div>', unsafe_allow_html=True)

    if len(df_trans) == 0:
        st.warning("No transaction data available for the selected filters.")
        return

    df_risk = calculate_inventory_risk_metrics(df_trans, df_inv)

    stockout_cnt = len(df_risk[df_risk["StockRiskStatus"] == "Stockout"])
    critical_cnt = len(df_risk[df_risk["StockRiskStatus"] == "Critical"])
    high_cnt = len(df_risk[df_risk["StockRiskStatus"] == "High"])
    healthy_cnt = len(df_risk[df_risk["StockRiskStatus"] == "Healthy"])

    demand_at_risk = df_risk[df_risk["StockRiskStatus"].isin(["Stockout", "Critical"])]["AvgDailyDemand"].sum()
    lt_demand = df_risk["LeadTimeDemand"].sum()

    c1, c2, c3 = st.columns(3)
    with c1:
        render_metric_card("Stockout SKUs", f"{stockout_cnt}", "Immediate Action Required", "negative")
        render_metric_card("High Risk SKUs", f"{high_cnt}", "Reorder Point Breached", "warning")
    with c2:
        render_metric_card("Critical SKUs", f"{critical_cnt}", "Below Safety Stock", "negative")
        render_metric_card("Healthy SKUs", f"{healthy_cnt}", "Optimal Inventory Level", "positive")
    with c3:
        render_metric_card("Daily Demand at Risk", f"{demand_at_risk:.1f} Units/day")
        render_metric_card("Lead Time Demand", f"{lt_demand:.1f} Units")

    st.markdown("---")

    col_a, col_b = st.columns([1, 1])

    with col_a:
        st.markdown('<div class="section-header">Risk Distribution</div>', unsafe_allow_html=True)
        risk_dist = df_risk["StockRiskStatus"].value_counts().reset_index()
        risk_dist.columns = ["Risk Status", "Count"]
        fig_donut = px.pie(risk_dist, values="Count", names="Risk Status", hole=0.5,
                           color="Risk Status",
                           color_discrete_map={"Stockout": "#ef4444", "Critical": "#f97316", "High": "#f59e0b", "Healthy": "#10b981", "Overstock": "#3b82f6"})
        fig_donut.update_layout(**plotly_dark_theme()["layout"])
        st.plotly_chart(fig_donut, use_container_width=True)

    with col_b:
        st.markdown('<div class="section-header">Stockout Rate by Category (%)</div>', unsafe_allow_html=True)
        cat_risk = df_risk.groupby("Category").apply(
            lambda x: (x["StockRiskStatus"].isin(["Stockout", "Critical", "High"]).sum() / len(x)) * 100
        ).reset_index(name="StockoutRate")
        fig_cat_risk = px.bar(cat_risk, y="Category", x="StockoutRate", orientation="h", color_discrete_sequence=["#ef4444"])
        fig_cat_risk.update_layout(**plotly_dark_theme()["layout"])
        st.plotly_chart(fig_cat_risk, use_container_width=True)

    st.markdown('<div class="section-header">Stock Risk Detailed Matrix</div>', unsafe_allow_html=True)
    matrix_df = df_risk[["SKU", "ProductName", "CurrentStock", "AvgDailyDemand", "DaysOfCover", "CalculatedROP", "StockRiskStatus"]].copy()
    matrix_df.columns = ["SKU ID", "Product Name", "On Hand Units", "Avg Daily Demand", "Days Of Cover", "Reorder Point", "Risk Status"]

    st.dataframe(matrix_df.style.format({
        "Avg Daily Demand": "{:.2f}",
        "Days Of Cover": "{:.2f}",
        "Reorder Point": "{:.2f}"
    }), use_container_width=True)
