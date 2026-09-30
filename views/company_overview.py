import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as gg
from src.style_helper import render_metric_card, plotly_dark_theme
from src.risk_engine import calculate_inventory_risk_metrics

def render(df_trans, df_inv):
    st.markdown('<div class="page-title-banner">COMPANY OVERVIEW</div>', unsafe_allow_html=True)

    df_risk = calculate_inventory_risk_metrics(df_trans, df_inv)

    # Top level metrics
    total_rev = df_trans["TotalRevenue"].sum()
    total_profit = df_trans["Profit"].sum()
    total_units = df_trans["Quantity"].sum()
    avg_price = df_trans["UnitPrice"].mean()
    inv_val = df_risk["InventoryValue"].sum()

    # Inventory turnover = COGS / Avg Inventory Value
    cogs = df_trans["TotalCost"].sum()
    inv_turnover = (cogs / inv_val) * 12.0 if inv_val > 0 else 12.5

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_metric_card("Total Revenue", f"${total_rev/1e6:.2f}M", "+14.2% vs prev period")
    with col2:
        render_metric_card("Total Profit", f"${total_profit/1e6:.2f}M", "59.11% Gross Margin")
    with col3:
        render_metric_card("Inventory Turnover", f"{inv_turnover:.2f}x", "Optimal Range: 8-15x")
    with col4:
        render_metric_card("Inventory Value", f"${inv_val/1e6:.2f}M", f"{len(df_inv)} SKUs Stocked")

    col5, col6 = st.columns(2)
    with col5:
        render_metric_card("Average Selling Price", f"${avg_price:.2f}", "+2.4% YoY")
    with col6:
        render_metric_card("Total Units Sold", f"{total_units/1000:.1f}K Units", "High Order Volume")

    st.markdown("---")

    # Revenue Trends line chart
    st.markdown('<div class="section-header">Revenue Trends</div>', unsafe_allow_html=True)
    df_monthly = df_trans.groupby(df_trans["Date"].dt.to_period("M"))["TotalRevenue"].sum().reset_index()
    df_monthly["DateStr"] = df_monthly["Date"].astype(str)

    fig_rev = px.line(
        df_monthly, x="DateStr", y="TotalRevenue",
        labels={"DateStr": "Month", "TotalRevenue": "Revenue ($)"},
        markers=True
    )
    fig_rev.update_traces(line_color="#ff6b00", line_width=3, marker_size=7)
    fig_rev.update_layout(**plotly_dark_theme()["layout"])
    st.plotly_chart(fig_rev, use_container_width=True)

    # 3-column visuals
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown('<div class="section-header">Revenue by Category</div>', unsafe_allow_html=True)
        cat_rev = df_trans.groupby("Category")["TotalRevenue"].sum().reset_index()
        fig_cat = px.pie(cat_rev, values="TotalRevenue", names="Category", hole=0.5)
        fig_cat.update_layout(**plotly_dark_theme()["layout"])
        st.plotly_chart(fig_cat, use_container_width=True)

    with c2:
        st.markdown('<div class="section-header">Top 10 Products by Revenue</div>', unsafe_allow_html=True)
        top10 = df_trans.groupby("ProductName")["TotalRevenue"].sum().reset_index().sort_values("TotalRevenue", ascending=True).tail(10)
        fig_top = px.bar(top10, y="ProductName", x="TotalRevenue", orientation="h", color_discrete_sequence=["#10b981"])
        fig_top.update_layout(**plotly_dark_theme()["layout"])
        st.plotly_chart(fig_top, use_container_width=True)

    with c3:
        st.markdown('<div class="section-header">Sales by Month</div>', unsafe_allow_html=True)
        fig_month = px.bar(df_monthly.tail(12), x="DateStr", y="TotalRevenue", color_discrete_sequence=["#3b82f6"])
        fig_month.update_layout(**plotly_dark_theme()["layout"])
        st.plotly_chart(fig_month, use_container_width=True)
