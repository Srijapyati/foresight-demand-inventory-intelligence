import streamlit as st
import pandas as pd
import plotly.express as px
from src.style_helper import render_metric_card, plotly_dark_theme
from src.risk_engine import calculate_inventory_risk_metrics

def render(df_trans, df_inv):
    st.markdown('<div class="page-title-banner" style="background: linear-gradient(90deg, #ea580c 0%, #c2410c 100%);">INVENTORY HEALTH</div>', unsafe_allow_html=True)

    df_risk = calculate_inventory_risk_metrics(df_trans, df_inv)

    on_hand_units = df_risk["CurrentStock"].sum()
    on_order_units = int(on_hand_units * 0.45)
    inv_value = df_risk["InventoryValue"].sum()
    avg_inv_val = df_risk["InventoryValue"].mean()
    potential_val = inv_value * 1.8
    cogs = df_trans["TotalCost"].sum()
    inv_turnover = (cogs / inv_value) if inv_value > 0 else 12.0
    avg_doc = df_risk[df_risk["DaysOfCover"] < 900]["DaysOfCover"].mean()

    c1, c2, c3, c4 = st.columns(4)
    with c1: render_metric_card("On Hand Units", f"{on_hand_units:,}")
    with c2: render_metric_card("On Order Units", f"{on_order_units:,}")
    with c3: render_metric_card("Inventory Value", f"${inv_value/1e6:.2f}M")
    with c4: render_metric_card("Inventory Turnover", f"{inv_turnover:.2f}x")

    c5, c6, c7 = st.columns(3)
    with c5: render_metric_card("Potential Inventory Val", f"${potential_val/1e6:.2f}M")
    with c6: render_metric_card("Avg Inventory Val", f"${avg_inv_val/1e3:.2f}K")
    with c7: render_metric_card("Days Of Cover", f"{avg_doc:.2f} Days")

    st.markdown("---")

    col_a, col_b = st.columns([1, 1])

    with col_a:
        st.markdown('<div class="section-header">Inventory by Category (Units)</div>', unsafe_allow_html=True)
        cat_inv = df_risk.groupby("Category")["CurrentStock"].sum().reset_index().sort_values("CurrentStock", ascending=False)
        fig_cat = px.bar(cat_inv, y="Category", x="CurrentStock", orientation="h", color_discrete_sequence=["#fb923c"])
        fig_cat.update_layout(**plotly_dark_theme()["layout"])
        st.plotly_chart(fig_cat, use_container_width=True)

    with col_b:
        st.markdown('<div class="section-header">Inventory Value by Category Treemap</div>', unsafe_allow_html=True)
        cat_val = df_risk.groupby("Category")["InventoryValue"].sum().reset_index()
        fig_tree = px.treemap(cat_val, path=["Category"], values="InventoryValue", color="InventoryValue", color_continuous_scale="Oranges")
        fig_tree.update_layout(**plotly_dark_theme()["layout"])
        st.plotly_chart(fig_tree, use_container_width=True)

    col_c, col_d = st.columns([2, 1])

    with col_c:
        st.markdown('<div class="section-header">On-Hand Inventory vs Reorder Point (Top 30)</div>', unsafe_allow_html=True)
        top30 = df_risk.head(30)
        fig_scatter = px.scatter(
            top30, x="CalculatedROP", y="CurrentStock", color="Category",
            size="SafetyStock", hover_name="ProductName",
            labels={"CalculatedROP": "Reorder Point", "CurrentStock": "On Hand Units"}
        )
        fig_scatter.update_layout(**plotly_dark_theme()["layout"])
        st.plotly_chart(fig_scatter, use_container_width=True)

    with col_d:
        st.markdown('<div class="section-header">Days of Cover by Category</div>', unsafe_allow_html=True)
        doc_cat = df_risk.groupby("Category")["DaysOfCover"].mean().reset_index()
        fig_doc = px.bar(doc_cat, y="Category", x="DaysOfCover", orientation="h", color_discrete_sequence=["#fdba74"])
        fig_doc.update_layout(**plotly_dark_theme()["layout"])
        st.plotly_chart(fig_doc, use_container_width=True)
