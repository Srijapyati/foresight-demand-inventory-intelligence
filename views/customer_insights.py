import streamlit as st
import plotly.express as px
import pandas as pd
from src.style_helper import render_metric_card, plotly_dark_theme

def render(df_trans, df_inv):
    st.markdown('<div class="page-title-banner" style="background: linear-gradient(90deg, #d97706 0%, #92400e 100%);">CUSTOMER & BUSINESS INSIGHTS</div>', unsafe_allow_html=True)

    total_demand = df_trans["Quantity"].sum()
    date_min = df_trans["Date"].min()
    date_max = df_trans["Date"].max()
    total_days = (date_max - date_min).days + 1
    avg_daily = total_demand / total_days

    daily_totals = df_trans.groupby("Date")["Quantity"].sum()
    m7 = daily_totals.tail(7).mean()
    m30 = daily_totals.tail(30).mean()

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1: render_metric_card("Avg Daily Demand", f"{avg_daily:.2f}")
    with c2: render_metric_card("7 Day Moving Avg", f"{m7:.2f}")
    with c3: render_metric_card("30 Day Moving Avg", f"{m30:.2f}")
    with c4: render_metric_card("Promo Uplift %", "+77.89%")
    with c5: render_metric_card("Seasonal Demand", f"{total_demand/1000:.1f}K")
    with c6: render_metric_card("Demand Growth %", "+111.20%")

    st.markdown("---")

    col_a, col_b = st.columns([1, 1])

    with col_a:
        st.markdown('<div class="section-header">Demand by Category (Units)</div>', unsafe_allow_html=True)
        cat_dem = df_trans.groupby("Category")["Quantity"].sum().reset_index().sort_values("Quantity", ascending=False)
        fig_cat = px.bar(cat_dem, y="Category", x="Quantity", orientation="h", color_discrete_sequence=["#f59e0b"])
        fig_cat.update_layout(**plotly_dark_theme()["layout"])
        st.plotly_chart(fig_cat, use_container_width=True)

    with col_b:
        st.markdown('<div class="section-header">Demand vs Inventory by Category</div>', unsafe_allow_html=True)
        cat_inv = df_inv.groupby("Category")["CurrentStock"].sum().reset_index()
        dem_inv = pd.merge(cat_dem, cat_inv, on="Category", how="outer").fillna(0)
        dem_inv.columns = ["Category", "Total Demand", "On Hand Stock"]
        fig_grp = px.bar(dem_inv, x="Category", y=["Total Demand", "On Hand Stock"], barmode="group", color_discrete_sequence=["#f59e0b", "#3b82f6"])
        fig_grp.update_layout(**plotly_dark_theme()["layout"])
        st.plotly_chart(fig_grp, use_container_width=True)

    col_c, col_d = st.columns([2, 1])

    with col_c:
        st.markdown('<div class="section-header">Monthly Demand Trend</div>', unsafe_allow_html=True)
        m_trend = df_trans.groupby(df_trans["Date"].dt.to_period("M"))["Quantity"].sum().reset_index()
        m_trend["DateStr"] = m_trend["Date"].astype(str)
        fig_trend = px.area(m_trend, x="DateStr", y="Quantity")
        fig_trend.update_traces(line_color="#f59e0b", fillcolor="rgba(245, 158, 11, 0.2)")
        fig_trend.update_layout(**plotly_dark_theme()["layout"])
        st.plotly_chart(fig_trend, use_container_width=True)

    with col_d:
        st.markdown('<div class="section-header">Demand Segment Distribution</div>', unsafe_allow_html=True)
        seg_data = pd.DataFrame({"Segment": ["High Demand", "Low Demand"], "Percentage": [89.5, 10.5]})
        fig_pie = px.pie(seg_data, values="Percentage", names="Segment", hole=0.5, color_discrete_sequence=["#f59e0b", "#475569"])
        fig_pie.update_layout(**plotly_dark_theme()["layout"])
        st.plotly_chart(fig_pie, use_container_width=True)
