import streamlit as st  # pyright: ignore[reportMissingImports]
import pandas as pd
try:
    import plotly.express as px  # pyright: ignore[reportMissingImports]
except ImportError:
    px = None
from src.style_helper import render_metric_card, plotly_dark_theme
from src.risk_engine import calculate_inventory_risk_metrics

def render(df_trans, df_inv):
    st.markdown('<div class="page-title-banner" style="background: linear-gradient(90deg, #2563eb 0%, #1d4ed8 100%);">OVERSTOCK DASHBOARD</div>', unsafe_allow_html=True)

    df_risk = calculate_inventory_risk_metrics(df_trans, df_inv)

    st.write("Stock Risk Status:", df_risk["StockRiskStatus"].value_counts())

    overstock_df = df_risk[df_risk["StockRiskStatus"] == "Overstock"]
    overstock_cnt = len(overstock_df)
    excess_units = df_risk["ExcessUnits"].sum()
    excess_value = df_risk["ExcessInventoryValue"].sum()
    dead_stock_cnt = len(df_risk[(df_risk["AvgDailyDemand"] == 0) & (df_risk["CurrentStock"] > 0)])

    c1, c2, c3, c4 = st.columns(4)
    with c1: render_metric_card("Overstock SKUs", f"{overstock_cnt}")
    with c2: render_metric_card("Excess Inventory Value", f"${excess_value/1e3:.2f}K")
    with c3: render_metric_card("Excess Inventory Units", f"{excess_units:,}")
    with c4: render_metric_card("Dead Stock SKUs", f"{dead_stock_cnt}", "0 Sales in Period")

    st.markdown("---")

    col_a, col_b = st.columns([1, 1])

    with col_a:
        st.markdown('<div class="section-header">Overstock SKUs by Category</div>', unsafe_allow_html=True)
        df_risk["StockRiskStatus"] = df_risk["StockRiskStatus"].astype(str).str.strip().str.upper()

        cat_over = (
            df_risk[df_risk["StockRiskStatus"] == "OVERSTOCK"]
            .groupby("Category")
            .size()
            .reset_index(name="Count")
        )
        fig_cat = px.bar(cat_over, x="Category", y="Count", color_discrete_sequence=["#60a5fa"])
        fig_cat.update_layout(**plotly_dark_theme()["layout"])
        st.plotly_chart(fig_cat, use_container_width=True)

    with col_b:
        st.markdown('<div class="section-header">Excess Inventory Value by Category ($)</div>', unsafe_allow_html=True)
        val_over = df_risk.groupby("Category")["ExcessInventoryValue"].sum().reset_index()
        fig_val = px.bar(val_over, x="Category", y="ExcessInventoryValue", color_discrete_sequence=["#3b82f6"])
        fig_val.update_layout(**plotly_dark_theme()["layout"])
        st.plotly_chart(fig_val, use_container_width=True)

    col_c, col_d = st.columns([2, 1])

    with col_c:
        st.markdown('<div class="section-header">Overstock SKU Details</div>', unsafe_allow_html=True)
        over_details = df_risk[["SKU", "Category", "ProductName", "CurrentStock", "AvgDailyDemand", "UnitCost", "ExcessUnits", "ExcessInventoryValue"]].copy()
        over_details.columns = ["SKU ID", "Category", "Product", "On Hand", "Avg Daily Demand", "Unit Cost ($)", "Excess Units", "Excess Value ($)"]
        st.dataframe(over_details.style.format({
            "Avg Daily Demand": "{:.2f}",
            "Unit Cost ($)": "${:.2f}",
            "Excess Value ($)": "${:,.2f}"
        }), use_container_width=True)

    with col_d:
        st.markdown('<div class="section-header">Inventory vs Demand by SKU</div>', unsafe_allow_html=True)
        fig_scat = px.scatter(df_risk, x="AvgDailyDemand", y="CurrentStock", color="Category", size="ExcessUnits", hover_name="ProductName")
        fig_scat.update_layout(**plotly_dark_theme()["layout"])
        st.plotly_chart(fig_scat, use_container_width=True)
