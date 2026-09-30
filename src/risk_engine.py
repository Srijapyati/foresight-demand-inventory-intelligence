import numpy as np
import pandas as pd

try:
    import streamlit as st  # type: ignore[import-not-found]
except ImportError:  # pragma: no cover - fallback for environments without Streamlit
    class _StreamlitFallback:
        @staticmethod
        def cache_data(*args, **kwargs):
            def decorator(func):
                return func
            return decorator

    st = _StreamlitFallback()

@st.cache_data(show_spinner=False)
def calculate_inventory_risk_metrics(df_trans, df_inv):
    """
    Computes comprehensive inventory analytics and risk scoring across all SKUs.
    """
    # Calculate daily average demand per SKU
    date_min = df_trans["Date"].min()
    date_max = df_trans["Date"].max()
    total_days = (date_max - date_min).days + 1

    sku_demand = df_trans.groupby("SKU").agg(
        TotalUnitsSold=("Quantity", "sum"),
        TotalRevenue=("TotalRevenue", "sum"),
        TotalCost=("TotalCost", "sum"),
        TotalProfit=("Profit", "sum")
    ).reset_index()

    sku_demand["AvgDailyDemand"] = sku_demand["TotalUnitsSold"] / total_days

    df_risk = pd.merge(df_inv, sku_demand, on="SKU", how="left").fillna(0)

    # Calculate Days of Cover (DOC)
    df_risk["DaysOfCover"] = np.where(
        df_risk["AvgDailyDemand"] > 0,
        df_risk["CurrentStock"] / df_risk["AvgDailyDemand"],
        999.0
    )

    # Lead time demand
    df_risk["LeadTimeDemand"] = df_risk["AvgDailyDemand"] * df_risk["LeadTimeDays"]

    # Reorder Point (ROP = Lead Time Demand + Safety Stock)
    df_risk["CalculatedROP"] = df_risk["LeadTimeDemand"] + df_risk["SafetyStock"]

    # Economic Order Quantity (EOQ = sqrt(2 * AnnualDemand * OrderingCost / HoldingCost))
    annual_demand = df_risk["AvgDailyDemand"] * 365
    df_risk["EOQ"] = np.sqrt(
        (2 * annual_demand * df_risk["OrderingCost"]) / np.maximum(df_risk["HoldingCostAnnual"], 0.01)
    ).round().astype(int)

    # Inventory Value
    df_risk["InventoryValue"] = df_risk["CurrentStock"] * df_risk["UnitCost"]
    df_risk["GrossMarginPct"] = np.where(
        df_risk["TotalRevenue"] > 0,
        (df_risk["TotalProfit"] / df_risk["TotalRevenue"]) * 100,
        0.0
    )

    # Risk Status Classification
    # Stockout: CurrentStock == 0
    # Critical: CurrentStock <= SafetyStock
    # High Risk: CurrentStock <= ReorderPoint
    # Overstock: DaysOfCover > 30
    # Healthy: Otherwise
    conditions = [
        (df_risk["CurrentStock"] == 0),
        (df_risk["CurrentStock"] <= df_risk["SafetyStock"]),
        (df_risk["CurrentStock"] <= df_risk["ReorderPoint"]),
        (df_risk["DaysOfCover"] > 30)
    ]
    choices = ["Stockout", "Critical", "High", "Overstock"]
    df_risk["StockRiskStatus"] = np.select(conditions, choices, default="Healthy")

    # Excess inventory calculation
    # Target stock = ReorderPoint + SafetyStock
    df_risk["TargetStock"] = df_risk["ReorderPoint"] + df_risk["SafetyStock"]
    df_risk["ExcessUnits"] = np.maximum(0, df_risk["CurrentStock"] - df_risk["TargetStock"])
    df_risk["ExcessInventoryValue"] = df_risk["ExcessUnits"] * df_risk["UnitCost"]

    # Action Recommendation
    rec_conditions = [
        (df_risk["StockRiskStatus"].isin(["Stockout", "Critical", "High"])),
        (df_risk["StockRiskStatus"] == "Overstock")
    ]
    rec_choices = ["REORDER", "OVERSTOCK"]
    df_risk["Recommendation"] = np.select(rec_conditions, rec_choices, default="HEALTHY")

    return df_risk
