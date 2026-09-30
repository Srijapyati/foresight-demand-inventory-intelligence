import streamlit as st
import pandas as pd
import plotly.express as px
from src.style_helper import render_metric_card, plotly_dark_theme
from src.risk_engine import calculate_inventory_risk_metrics

def render(df_trans, df_inv):
    st.markdown('<div class="page-title-banner" style="background: linear-gradient(90deg, #ec4899 0%, #be185d 100%);">PRODUCT PERFORMANCE</div>', unsafe_allow_html=True)

    df_risk = calculate_inventory_risk_metrics(df_trans, df_inv)

    total_skus = len(df_inv)
    avg_sku_rev = df_risk["TotalRevenue"].mean()
    top_sku_rev = df_risk["TotalRevenue"].max()
    low_performers = len(df_risk[df_risk["TotalRevenue"] < avg_sku_rev * 0.5])
    gross_margin = (df_risk["TotalProfit"].sum() / df_risk["TotalRevenue"].sum() * 100) if df_risk["TotalRevenue"].sum() > 0 else 0

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        render_metric_card("Total SKUs", f"{total_skus}")
    with c2:
        render_metric_card("Avg SKU Revenue", f"${avg_sku_rev/1e3:.1f}K")
    with c3:
        render_metric_card("Top SKU Revenue", f"${top_sku_rev/1e3:.1f}K")
    with c4:
        render_metric_card("Low Performing SKUs", f"{low_performers}", "Needs Optimization", "warning")
    with c5:
        render_metric_card("Gross Margin %", f"{gross_margin:.2f}%")

    st.markdown("---")

    col_a, col_b = st.columns([1, 1])

    with col_a:
        st.markdown('<div class="section-header">Product Revenue vs Gross Margin % (Top 20)</div>', unsafe_allow_html=True)
        top20 = df_risk.sort_values("TotalRevenue", ascending=False).head(20)
        fig_scatter = px.scatter(
            top20, x="TotalRevenue", y="GrossMarginPct", color="Category",
            size="TotalUnitsSold", hover_name="ProductName",
            labels={"TotalRevenue": "Revenue ($)", "GrossMarginPct": "Gross Margin (%)"}
        )
        fig_scatter.update_layout(**plotly_dark_theme()["layout"])
        st.plotly_chart(fig_scatter, use_container_width=True)

    with col_b:
        st.markdown('<div class="section-header">Top 20 Products by Revenue</div>', unsafe_allow_html=True)
        fig_bar = px.bar(top20.sort_values("TotalRevenue", ascending=True), y="ProductName", x="TotalRevenue", orientation="h", color_discrete_sequence=["#ec4899"])
        fig_bar.update_layout(**plotly_dark_theme()["layout"])
        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown('<div class="section-header">SKU Level Detailed Performance</div>', unsafe_allow_html=True)
    display_df = df_risk[["SKU", "ProductName", "Category", "TotalRevenue", "TotalUnitsSold", "TotalProfit", "GrossMarginPct", "InventoryValue", "StockRiskStatus"]].copy()
    display_df.columns = ["SKU ID", "Product Name", "Category", "Total Revenue ($)", "Units Sold", "Total Profit ($)", "Gross Margin (%)", "Inventory Value ($)", "Risk Status"]

    st.dataframe(display_df.style.format({
        "Total Revenue ($)": "${:,.2f}",
        "Total Profit ($)": "${:,.2f}",
        "Gross Margin (%)": "{:.2f}%",
        "Inventory Value ($)": "${:,.2f}"
    }), use_container_width=True)
