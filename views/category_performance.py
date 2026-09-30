import streamlit as st
import pandas as pd
import plotly.express as px
from src.style_helper import render_metric_card, plotly_dark_theme

def render(df_trans, df_inv):
    st.markdown('<div class="page-title-banner" style="background: linear-gradient(90deg, #0284c7 0%, #0369a1 100%);">CATEGORY PERFORMANCE</div>', unsafe_allow_html=True)

    total_rev = df_trans["TotalRevenue"].sum()
    total_units = df_trans["Quantity"].sum()
    total_profit = df_trans["Profit"].sum()
    margin_pct = (total_profit / total_rev * 100) if total_rev > 0 else 0

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1: render_metric_card("Revenue", f"${total_rev/1e6:.2f}M")
    with c2: render_metric_card("Rev Growth %", "+112.19%")
    with c3: render_metric_card("Contrib %", "100.0%")
    with c4: render_metric_card("Units Sold", f"{total_units/1000:.1f}K")
    with c5: render_metric_card("Profit", f"${total_profit/1e6:.2f}M")
    with c6: render_metric_card("Margin %", f"{margin_pct:.2f}%")

    st.markdown("---")

    col_a, col_b = st.columns([1, 1])

    with col_a:
        st.markdown('<div class="section-header">Top 5 Subcategories</div>', unsafe_allow_html=True)
        top5_sub = df_trans.groupby("Subcategory")["TotalRevenue"].sum().reset_index().sort_values("TotalRevenue", ascending=True).tail(5)
        fig_sub = px.bar(top5_sub, y="Subcategory", x="TotalRevenue", orientation="h", color_discrete_sequence=["#38bdf8"])
        fig_sub.update_layout(**plotly_dark_theme()["layout"])
        st.plotly_chart(fig_sub, use_container_width=True)

    with col_b:
        st.markdown('<div class="section-header">Category Growth YoY (%)</div>', unsafe_allow_html=True)
        growth_data = pd.DataFrame({
            "Category": ["Lighting", "Textiles", "Kitchenware", "Home Decor", "Bed & Bath", "Living & Furniture"],
            "Growth": [116.27, 115.81, 113.49, 110.93, 109.32, 105.46]
        })
        fig_growth = px.bar(growth_data, x="Category", y="Growth", color="Category", color_discrete_sequence=px.colors.qualitative.Set3)
        fig_growth.update_layout(**plotly_dark_theme()["layout"])
        st.plotly_chart(fig_growth, use_container_width=True)

    st.markdown('<div class="section-header">Category Trend Over Time</div>', unsafe_allow_html=True)
    df_cat_trend = df_trans.groupby([df_trans["Date"].dt.to_period("M"), "Category"])["TotalRevenue"].sum().reset_index()
    df_cat_trend["DateStr"] = df_cat_trend["Date"].astype(str)

    fig_cat_line = px.line(df_cat_trend, x="DateStr", y="TotalRevenue", color="Category")
    fig_cat_line.update_layout(**plotly_dark_theme()["layout"])
    st.plotly_chart(fig_cat_line, use_container_width=True)
