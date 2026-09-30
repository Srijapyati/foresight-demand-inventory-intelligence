import importlib

try:
    st = importlib.import_module("streamlit")
except ModuleNotFoundError as exc:
    raise RuntimeError(
        "Streamlit is required to run the alerts center. Install it with: pip install streamlit"
    ) from exc
import pandas as pd
from src.style_helper import render_metric_card
from src.risk_engine import calculate_inventory_risk_metrics

def render(df_trans, df_inv):
    st.markdown('<div class="page-title-banner" style="background: linear-gradient(90deg, #ca8a04 0%, #a16207 100%);">ALERTS & NOTIFICATION CENTER</div>', unsafe_allow_html=True)

    if len(df_trans) == 0:
        st.warning("No data available for the selected filters.")
        return

    df_risk = calculate_inventory_risk_metrics(df_trans, df_inv)

    alerts = []
    for idx, row in df_risk.iterrows():
        if row["CurrentStock"] == 0:
            alerts.append({
                "Severity": "CRITICAL",
                "SKU": row["SKU"],
                "Product": row["ProductName"],
                "Category": row["Category"],
                "Message": f"Stockout detected! Current stock is 0 units. Immediate purchase order required.",
                "Action": "Create PO"
            })
        elif row["CurrentStock"] <= row["SafetyStock"]:
            alerts.append({
                "Severity": "HIGH",
                "SKU": row["SKU"],
                "Product": row["ProductName"],
                "Category": row["Category"],
                "Message": f"Safety stock breached! Stock level ({row['CurrentStock']}) is below safety threshold ({row['SafetyStock']}).",
                "Action": "Expedite Delivery"
            })
        elif row["StockRiskStatus"] == "Overstock":
            alerts.append({
                "Severity": "MEDIUM",
                "SKU": row["SKU"],
                "Product": row["ProductName"],
                "Category": row["Category"],
                "Message": f"Excess inventory holding! Days of Cover is {row['DaysOfCover']:.1f} days. Excess holding cost: ${row['ExcessInventoryValue']:.2f}.",
                "Action": "Apply Promo Discount"
            })

    if len(alerts) > 0:
        df_alerts = pd.DataFrame(alerts)
    else:
        df_alerts = pd.DataFrame(columns=["Severity", "SKU", "Product", "Category", "Message", "Action"])

    crit_cnt = len(df_alerts[df_alerts["Severity"] == "CRITICAL"]) if "Severity" in df_alerts.columns else 0
    high_cnt = len(df_alerts[df_alerts["Severity"] == "HIGH"]) if "Severity" in df_alerts.columns else 0
    med_cnt = len(df_alerts[df_alerts["Severity"] == "MEDIUM"]) if "Severity" in df_alerts.columns else 0

    c1, c2, c3, c4 = st.columns(4)
    with c1: render_metric_card("Total System Alerts", f"{len(df_alerts)}")
    with c2: render_metric_card("Critical Alerts", f"{crit_cnt}", "Requires Immediate Action", "negative")
    with c3: render_metric_card("High Priority Alerts", f"{high_cnt}", "Threshold Breached", "warning")
    with c4: render_metric_card("Medium Alerts", f"{med_cnt}", "Optimization Opportunity")

    st.markdown("---")
    st.markdown('<div class="section-header">Active Supply Chain Alerts</div>', unsafe_allow_html=True)

    if len(df_alerts) == 0:
        st.info("🟢 No active supply chain alerts. All inventory levels are optimal for the current filter selection.")
    else:
        for idx, row in df_alerts.iterrows():
            sev_color = "#ef4444" if row["Severity"] == "CRITICAL" else ("#f59e0b" if row["Severity"] == "HIGH" else "#3b82f6")
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.03); border-left: 5px solid {sev_color}; padding: 14px 18px; border-radius: 8px; margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: 700; color: {sev_color}; font-size: 0.85rem;">[{row['Severity']}] {row['SKU']} - {row['Product']} ({row['Category']})</span>
                    <span style="background: rgba(255,255,255,0.1); padding: 2px 10px; border-radius: 12px; font-size: 0.75rem; color: #cbd5e1;">Action: {row['Action']}</span>
                </div>
                <div style="color: #cbd5e1; font-size: 0.9rem; margin-top: 6px;">{row['Message']}</div>
            </div>
            """, unsafe_allow_html=True)
