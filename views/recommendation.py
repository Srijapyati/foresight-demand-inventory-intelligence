import pandas as pd
import importlib

# Load Streamlit dynamically so the view remains importable in environments
# where the editor's selected Python environment does not expose the package.
st = importlib.import_module("streamlit")

try:
    px = importlib.import_module("plotly.express")
except ImportError:
    px = None
from src.style_helper import render_metric_card, plotly_dark_theme
from src.risk_engine import calculate_inventory_risk_metrics

def render(df_trans, df_inv):
    st.markdown('<div class="page-title-banner" style="background: linear-gradient(90deg, #991b1b 0%, #7f1d1d 100%);">RECOMMENDATION ENGINE & ACTION MATRIX</div>', unsafe_allow_html=True)

    if len(df_trans) == 0:
        st.warning("No transaction data available for the selected filters.")
        return

    df_risk = calculate_inventory_risk_metrics(df_trans, df_inv)

    reorder_cnt = len(df_risk[df_risk["Recommendation"] == "REORDER"])
    overstock_cnt = len(df_risk[df_risk["Recommendation"] == "OVERSTOCK"])
    healthy_cnt = len(df_risk[df_risk["Recommendation"] == "HEALTHY"])
    val_at_risk = df_risk[df_risk["Recommendation"].isin(["REORDER", "OVERSTOCK"])]["InventoryValue"].sum()

    c1, c2, c3, c4 = st.columns(4)
    with c1: render_metric_card("Reorder SKUs", f"{reorder_cnt}", "Replenish Stock", "negative")
    with c2: render_metric_card("Overstock SKUs", f"{overstock_cnt}", "Clear Excess Stock", "warning")
    with c3: render_metric_card("Healthy SKUs", f"{healthy_cnt}", "Optimal Balance", "positive")
    with c4: render_metric_card("Inventory Value at Risk", f"${val_at_risk/1e3:.2f}K", "Total Financial Exposure")

    st.markdown("---")

    col_a, col_b = st.columns([2, 1])

    with col_a:
        st.markdown('<div class="section-header">Executive Action Matrix</div>', unsafe_allow_html=True)
        action_df = df_risk[["SKU", "ProductName", "CurrentStock", "AvgDailyDemand", "ExcessUnits", "ExcessInventoryValue", "Recommendation"]].copy()
        action_df.columns = ["SKU ID", "Product Name", "On Hand Units", "Forecast Daily Demand", "Excess Units", "Excess Value ($)", "Action Recommendation"]

        st.dataframe(action_df.style.format({
            "Forecast Daily Demand": "{:.2f}",
            "Excess Value ($)": "${:,.2f}"
        }), use_container_width=True)

    with col_b:
        st.markdown('<div class="section-header">Recommendation Action Split</div>', unsafe_allow_html=True)
        rec_split = df_risk["Recommendation"].value_counts().reset_index()
        rec_split.columns = ["Action", "Count"]
        fig_donut = px.pie(rec_split, values="Count", names="Action", hole=0.5,
                           color="Action", color_discrete_map={"REORDER": "#ef4444", "OVERSTOCK": "#3b82f6", "HEALTHY": "#10b981"})
        fig_donut.update_layout(**plotly_dark_theme()["layout"])
        st.plotly_chart(fig_donut, use_container_width=True)

    col_c, col_d = st.columns([1, 1])

    with col_c:
        st.markdown(
            '<div class="section-header">Category-Level Recommendations</div>',
            unsafe_allow_html=True
        )

        cat_rec = (
            df_risk.groupby(["Category", "Recommendation"])
            .size()
            .unstack(fill_value=0)
            .reindex(
                columns=["REORDER", "OVERSTOCK", "HEALTHY"],
                fill_value=0
            )
            .reset_index()
        )

        # Convert to long format for Plotly
        cat_long = cat_rec.melt(
            id_vars="Category",
            var_name="Recommendation",
            value_name="Count"
        )

        fig_bar = px.bar(
            cat_long,
            x="Category",
            y="Count",
            color="Recommendation",
            barmode="group",
            color_discrete_map={
                "REORDER": "#ef4444",
                "OVERSTOCK": "#3b82f6",
                "HEALTHY": "#22c55e"
            }
        )

        fig_bar.update_layout(
            **plotly_dark_theme()["layout"]
        )

        st.plotly_chart(
            fig_bar,
            use_container_width=True
        )

    with col_d:
        st.markdown(
            '<div class="section-header">Inventory Risk vs Demand</div>',
            unsafe_allow_html=True
        )

        fig_scat = px.scatter(
            df_risk,
            x="AvgDailyDemand",
            y="CurrentStock",
            color="Recommendation",
            size="CalculatedROP",
            hover_name="ProductName",
            color_discrete_map={
                "REORDER": "#ef4444",
                "OVERSTOCK": "#3b82f6",
                "HEALTHY": "#10b981"
            }
        )

        fig_scat.update_layout(
            **plotly_dark_theme()["layout"]
        )

        st.plotly_chart(
            fig_scat,
            use_container_width=True
        )