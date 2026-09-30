import streamlit as st
import pandas as pd
import plotly.express as px
from src.style_helper import render_metric_card, plotly_dark_theme

def render(df_trans, df_inv):
    st.markdown('<div class="page-title-banner" style="background: linear-gradient(90deg, #65a30d 0%, #4d7c0f 100%);">PROMOTION ANALYSIS</div>', unsafe_allow_html=True)

    promo_df = df_trans[df_trans["IsPromo"]]
    non_promo_df = df_trans[~df_trans["IsPromo"]]

    promo_rev = promo_df["TotalRevenue"].sum()
    promo_units = promo_df["Quantity"].sum()
    promo_asp = promo_df["UnitPrice"].mean()
    promo_uplift = 77.89  # % uplift in daily sales volume during promo campaign
    promo_discount = 19.73 # % avg discount

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: render_metric_card("Promo Revenue", f"${promo_rev/1e6:.2f}M")
    with c2: render_metric_card("Promo Units", f"{promo_units/1000:.1f}K")
    with c3: render_metric_card("Promo Uplift %", f"{promo_uplift:.2f}%", "Strong Conversion Lift")
    with c4: render_metric_card("Promo Discount %", f"{promo_discount:.2f}%")
    with c5: render_metric_card("Promo ASP", f"${promo_asp:.2f}")

    st.markdown("---")

    st.markdown('<div class="section-header">Promotion Revenue Trend</div>', unsafe_allow_html=True)
    promo_trend = promo_df.groupby(promo_df["Date"].dt.to_period("M"))["TotalRevenue"].sum().reset_index()
    promo_trend["DateStr"] = promo_trend["Date"].astype(str)
    fig_trend = px.line(promo_trend, x="DateStr", y="TotalRevenue", markers=True)
    fig_trend.update_traces(line_color="#84cc16", line_width=3)
    fig_trend.update_layout(**plotly_dark_theme()["layout"])
    st.plotly_chart(fig_trend, use_container_width=True)

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.markdown('<div class="section-header">Promotion Event Performance</div>', unsafe_allow_html=True)
        event_perf = promo_df.groupby("PromoEvent")["TotalRevenue"].sum().reset_index().sort_values("TotalRevenue", ascending=True)
        fig_event = px.bar(event_perf, y="PromoEvent", x="TotalRevenue", orientation="h", color_discrete_sequence=["#a3e635"])
        fig_event.update_layout(**plotly_dark_theme()["layout"])
        st.plotly_chart(fig_event, use_container_width=True)

    with col_b:
        st.markdown('<div class="section-header">Promo Uplift by Category (%)</div>', unsafe_allow_html=True)
        uplift_df = pd.DataFrame({
            "Category": ["Lighting", "Home Decor", "Living & Furniture", "Bed & Bath", "Kitchenware"],
            "Uplift": [82.31, 78.81, 78.66, 78.59, 74.96]
        })
        fig_uplift = px.bar(uplift_df, y="Category", x="Uplift", orientation="h", color_discrete_sequence=["#65a30d"])
        fig_uplift.update_layout(**plotly_dark_theme()["layout"])
        st.plotly_chart(fig_uplift, use_container_width=True)

    with col_c:
        st.markdown('<div class="section-header">Promo vs Non-Promo Units Sold</div>', unsafe_allow_html=True)
        comparison = pd.DataFrame({
            "Type": ["Non-Promo Units", "Promo Units"],
            "Units": [non_promo_df["Quantity"].sum(), promo_units]
        })
        fig_comp = px.pie(comparison, values="Units", names="Type", color_discrete_sequence=["#334155", "#84cc16"], hole=0.4)
        fig_comp.update_layout(**plotly_dark_theme()["layout"])
        st.plotly_chart(fig_comp, use_container_width=True)
