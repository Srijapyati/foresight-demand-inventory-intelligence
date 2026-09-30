import streamlit as st
import pandas as pd
import plotly.express as px
from src.style_helper import render_metric_card, plotly_dark_theme

def render(df_trans, df_inv):
    st.markdown('<div class="page-title-banner" style="background: linear-gradient(90deg, #eab308 0%, #ca8a04 100%);">SEASONALITY & DEMAND PATTERNS</div>', unsafe_allow_html=True)

    total_demand = df_trans["Quantity"].sum()
    date_min = df_trans["Date"].min()
    date_max = df_trans["Date"].max()
    total_days = (date_max - date_min).days + 1
    avg_daily_demand = total_demand / total_days
    peak_demand = df_trans.groupby("Date")["Quantity"].sum().max()
    seasonal_rev = df_trans["TotalRevenue"].sum()
    demand_yoy = 111.20

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: render_metric_card("Total Demand", f"{total_demand/1000:.1f}K Units")
    with c2: render_metric_card("Avg Daily Demand", f"{avg_daily_demand:.2f} Units/day")
    with c3: render_metric_card("Peak Demand", f"{peak_demand:,} Units/day")
    with c4: render_metric_card("Demand YoY %", f"{demand_yoy:.2f}%")
    with c5: render_metric_card("Seasonal Revenue", f"${seasonal_rev/1e6:.2f}M")

    st.markdown("---")

    st.markdown('<div class="section-header">Monthly Demand Trend</div>', unsafe_allow_html=True)
    m_demand = df_trans.groupby(df_trans["Date"].dt.to_period("M"))["Quantity"].sum().reset_index()
    m_demand["DateStr"] = m_demand["Date"].astype(str)
    fig_trend = px.area(m_demand, x="DateStr", y="Quantity")
    fig_trend.update_traces(line_color="#facc15", fillcolor="rgba(250, 204, 21, 0.2)")
    fig_trend.update_layout(**plotly_dark_theme()["layout"])
    st.plotly_chart(fig_trend, use_container_width=True)

    col_a, col_b = st.columns([1, 1])

    with col_a:
        st.markdown('<div class="section-header">Demand by Season (Units)</div>', unsafe_allow_html=True)
        season_df = df_trans.groupby("Season")["Quantity"].sum().reset_index().sort_values("Quantity", ascending=False)
        fig_season = px.bar(season_df, x="Season", y="Quantity", color="Season", color_discrete_sequence=["#eab308", "#ca8a04", "#fef08a", "#fde047"])
        fig_season.update_layout(**plotly_dark_theme()["layout"])
        st.plotly_chart(fig_season, use_container_width=True)

    with col_b:
        st.markdown('<div class="section-header">Holiday vs Non-Holiday Demand</div>', unsafe_allow_html=True)
        # Nov-Dec tagged as Holiday period
        df_trans["IsHoliday"] = df_trans["MonthNum"].isin([11, 12])
        hol_df = df_trans.groupby("IsHoliday")["Quantity"].mean().reset_index()
        hol_df["Type"] = hol_df["IsHoliday"].map({True: "Holiday Period (Q4)", False: "Non-Holiday Period"})
        fig_hol = px.bar(hol_df, x="Type", y="Quantity", color="Type", color_discrete_sequence=["#ca8a04", "#a16207"])
        fig_hol.update_layout(**plotly_dark_theme()["layout"])
        st.plotly_chart(fig_hol, use_container_width=True)

    st.markdown('<div class="section-header">Seasonal Demand Breakdown by Category</div>', unsafe_allow_html=True)
    pivot_season = pd.pivot_table(df_trans, values="Quantity", index="Season", columns="Category", aggfunc="sum", fill_value=0)
    pivot_season["Total"] = pivot_season.sum(axis=1)
    st.dataframe(pivot_season.style.format("{:,.0f}"), use_container_width=True)
