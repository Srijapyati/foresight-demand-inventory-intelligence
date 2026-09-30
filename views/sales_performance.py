import streamlit as st
import pandas as pd
import plotly.express as px
from src.style_helper import render_metric_card, plotly_dark_theme

def render(df_trans, df_inv):
    st.markdown('<div class="page-title-banner" style="background: linear-gradient(90deg, #d97706 0%, #b45309 100%);">SALES PERFORMANCE</div>', unsafe_allow_html=True)

    total_rev = df_trans["TotalRevenue"].sum()
    gross_profit = df_trans["Profit"].sum()
    units_sold = df_trans["Quantity"].sum()
    margin_pct = (gross_profit / total_rev * 100) if total_rev > 0 else 0
    asp = df_trans["UnitPrice"].mean()

    c1, c2, c3 = st.columns(3)
    with c1:
        render_metric_card("Total Revenue", f"${total_rev/1e6:.2f}M")
        render_metric_card("Gross Profit", f"${gross_profit/1e6:.2f}M")
    with c2:
        render_metric_card("Average Selling Price", f"${asp:.2f}")
        render_metric_card("Gross Margin %", f"{margin_pct:.2f}%")
    with c3:
        render_metric_card("Total Units Sold", f"{units_sold/1000:.1f}K")
        render_metric_card("Revenue YOY %", "+12.4%", "Outperforming Target")

    st.markdown("---")

    col_a, col_b = st.columns([1, 1])

    with col_a:
        st.markdown('<div class="section-header">Revenue by Category</div>', unsafe_allow_html=True)
        cat_df = df_trans.groupby("Category")["TotalRevenue"].sum().reset_index().sort_values("TotalRevenue", ascending=False)
        fig_cat = px.bar(cat_df, x="Category", y="TotalRevenue", color="Category", color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_cat.update_layout(**plotly_dark_theme()["layout"])
        st.plotly_chart(fig_cat, use_container_width=True)

    with col_b:
        st.markdown('<div class="section-header">Revenue by Subcategory</div>', unsafe_allow_html=True)
        sub_df = df_trans.groupby("Subcategory")["TotalRevenue"].sum().reset_index().sort_values("TotalRevenue", ascending=True)
        fig_sub = px.bar(sub_df, y="Subcategory", x="TotalRevenue", orientation="h", color_discrete_sequence=["#f59e0b"])
        fig_sub.update_layout(**plotly_dark_theme()["layout"])
        st.plotly_chart(fig_sub, use_container_width=True)

    st.markdown('<div class="section-header">Monthly Revenue Trend</div>', unsafe_allow_html=True)
    df_trend = df_trans.groupby(df_trans["Date"].dt.to_period("M"))["TotalRevenue"].sum().reset_index()
    df_trend["DateStr"] = df_trend["Date"].astype(str)
    fig_trend = px.area(df_trend, x="DateStr", y="TotalRevenue")
    fig_trend.update_traces(line_color="#f59e0b", fillcolor="rgba(245, 158, 11, 0.2)")
    fig_trend.update_layout(**plotly_dark_theme()["layout"])
    st.plotly_chart(fig_trend, use_container_width=True)
