import streamlit as st
import numpy as np
import plotly.express as px
import pandas as pd
from src.style_helper import render_metric_card, plotly_dark_theme
from src.risk_engine import calculate_inventory_risk_metrics

def render(df_trans, df_inv):
    st.markdown('<div class="page-title-banner" style="background: linear-gradient(90deg, #7c3aed 0%, #5b21b6 100%);">WHAT-IF SCENARIO SIMULATOR</div>', unsafe_allow_html=True)
    st.markdown("Simulate supply chain disruptions, demand surges, supplier lead time delays, and promo discounts to evaluate real-time stockout risk & financial exposure.")

    df_risk = calculate_inventory_risk_metrics(df_trans, df_inv)

    c_sim1, c_sim2, c_sim3 = st.columns(3)
    with c_sim1:
        demand_surge = st.slider("Demand Surge / Drop (%)", min_value=-50, max_value=100, value=25, step=5)
    with c_sim2:
        supplier_delay = st.slider("Supplier Lead Time Delay (Days)", min_value=0, max_value=30, value=7, step=1)
    with c_sim3:
        promo_discount = st.slider("Planned Promo Discount (%)", min_value=0, max_value=40, value=15, step=5)

    # Apply scenario multipliers
    df_sim = df_risk.copy()
    surge_mult = 1.0 + (demand_surge / 100.0)
    promo_mult = 1.0 + (promo_discount * 0.02) # Elasticity lift factor
    effective_demand_mult = surge_mult * promo_mult

    df_sim["SimulatedDailyDemand"] = df_sim["AvgDailyDemand"] * effective_demand_mult
    df_sim["SimulatedLeadTime"] = df_sim["LeadTimeDays"] + supplier_delay
    df_sim["SimulatedROP"] = (df_sim["SimulatedDailyDemand"] * df_sim["SimulatedLeadTime"]) + df_sim["SafetyStock"]

    df_sim["SimulatedStockoutDays"] = np.where(
        df_sim["SimulatedDailyDemand"] > 0,
        np.maximum(0, (df_sim["SimulatedROP"] - df_sim["CurrentStock"]) / df_sim["SimulatedDailyDemand"]),
        0
    )

    df_sim["SimulatedRequiredReorder"] = np.maximum(0, df_sim["SimulatedROP"] - df_sim["CurrentStock"])
    df_sim["SimulatedReorderCost"] = df_sim["SimulatedRequiredReorder"] * df_sim["UnitCost"]

    stockouts_count = len(df_sim[df_sim["CurrentStock"] < df_sim["SimulatedROP"]])
    total_reorder_cost = df_sim["SimulatedReorderCost"].sum()
    total_stockout_days = df_sim["SimulatedStockoutDays"].sum()

    st.markdown("---")

    c1, c2, c3 = st.columns(3)
    with c1: render_metric_card("Simulated Stockout SKUs", f"{stockouts_count}", f"Breached in scenario", "negative")
    with c2: render_metric_card("Required Reorder Budget", f"${total_reorder_cost/1e3:.2f}K", "Capital needed to buffer")
    with c3: render_metric_card("Projected Stockout Days", f"{total_stockout_days:.1f} Days", "Total risk exposure", "warning")

    st.markdown('<div class="section-header">Simulated SKU Stockout Risk Matrix</div>', unsafe_allow_html=True)
    sim_display = df_sim[["SKU", "ProductName", "CurrentStock", "AvgDailyDemand", "SimulatedDailyDemand", "LeadTimeDays", "SimulatedLeadTime", "CalculatedROP", "SimulatedROP", "SimulatedRequiredReorder", "SimulatedReorderCost"]].copy()
    sim_display.columns = ["SKU", "Product Name", "Current Stock", "Base Demand", "Simulated Demand", "Base LT", "Simulated LT", "Base ROP", "Simulated ROP", "Reorder Qty", "Reorder Cost ($)"]

    st.dataframe(sim_display.style.format({
        "Base Demand": "{:.2f}",
        "Simulated Demand": "{:.2f}",
        "Base ROP": "{:.1f}",
        "Simulated ROP": "{:.1f}",
        "Reorder Qty": "{:.0f}",
        "Reorder Cost ($)": "${:,.2f}"
    }), use_container_width=True)

    fig_sim = px.bar(df_sim, x="SKU", y=["CurrentStock", "SimulatedROP"], barmode="group",
                     title="Current Stock vs Simulated Reorder Point by SKU",
                     labels={"value": "Units", "variable": "Metric"})
    fig_sim.update_layout(**plotly_dark_theme()["layout"])
    st.plotly_chart(fig_sim, use_container_width=True)
