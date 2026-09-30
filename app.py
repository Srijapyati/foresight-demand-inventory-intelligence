import importlib

# Load Streamlit dynamically so editors that do not index optional app
# dependencies do not report a false unresolved-import warning.
st = importlib.import_module("streamlit")
import pandas as pd
from datetime import datetime

# Streamlit Page Config
st.set_page_config(
    page_title="FORESIGHT - AI-Powered Demand & Inventory Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

from src.style_helper import apply_custom_css
from src.data_loader import load_raw_data, filter_data

from views import (
    login,
    home,
    company_overview,
    sales_performance,
    product_performance,
    category_performance,
    inventory_health,
    stock_risk,
    overstock,
    promotion_analysis,
    seasonality,
    forecast,
    customer_insights,
    recommendation,
    what_if_simulator,
    alerts_center,
    executive_presentation
)

def main():
    # Initialize session state for authentication & theme
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = True # Default logged-in for instant access

    if "theme" not in st.session_state:
        st.session_state["theme"] = "Dark Luxury"

    # Theme selection control in top sidebar
    theme = st.sidebar.selectbox(
        "🎨 Select UI Color Theme:",
        ["Dark Luxury", "Navy Blue", "Light Corporate"],
        index=["Dark Luxury", "Navy Blue", "Light Corporate"].index(st.session_state["theme"])
    )
    st.session_state["theme"] = theme
    apply_custom_css(theme=theme)

    # Render Login Page if not authenticated
    if not st.session_state["authenticated"]:
        login.render()
        return

    # Load cached datasets
    df_trans, df_inv = load_raw_data()

    # Sidebar Header
    st.sidebar.markdown("""
    <div class="brand-header">
        <span style="color: #ff6b00;">⚡</span> FORESIGHT
    </div>
    <div class="brand-sub">
        Demand & Inventory Intelligence — NorthBay Living
    </div>
    """, unsafe_allow_html=True)

    if st.sidebar.button("🔒 Sign Out / Switch User", use_container_width=True):
        st.session_state["authenticated"] = False
        st.rerun()

    st.sidebar.markdown("---")

    # Navigation menu
    nav_selection = st.sidebar.radio(
        "Navigation",
        [
            "🏠 Home",
            "📊 Company Overview",
            "📈 Sales Analytics",
            "📦 Product Details",
            "🏷️ Category Performance",
            "🏬 Inventory Dashboard",
            "⚠️ Risk Dashboard",
            "🚨 Overstock Dashboard",
            "🏷️ Promotion Analysis",
            "📅 Seasonality Center",
            "🔮 Demand Forecast",
            "👥 Customer Insights",
            "🎯 Recommendation Engine",
            "🎛️ What-If Simulator",
            "🔔 Alerts Center",
            "📑 Executive Presentation"
        ]
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### Interactive Filters")

    # Date filter
    min_date = df_trans["Date"].min().date()
    max_date = df_trans["Date"].max().date()

    date_range = st.sidebar.date_input(
        "Date Window",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    start_d = date_range[0] if len(date_range) > 0 else min_date
    end_d = date_range[1] if len(date_range) > 1 else max_date

    categories = ["All"] + sorted(list(df_trans["Category"].unique()))
    selected_cats = st.sidebar.multiselect("Category", categories, default=["All"])

    subcategories = ["All"] + sorted(list(df_trans["Subcategory"].unique()))
    selected_subs = st.sidebar.multiselect("Subcategory", subcategories, default=["All"])

    skus = ["All"] + sorted(list(df_trans["SKU"].unique()))
    selected_skus = st.sidebar.multiselect("SKU Filter", skus, default=["All"])

    # Filter dataframe
    df_trans_filtered = filter_data(
        df_trans,
        start_date=start_d,
        end_date=end_d,
        categories=selected_cats,
        subcategories=selected_subs,
        skus=selected_skus
    )

    # View Routing
    if "Home" in nav_selection:
        home.render(df_trans_filtered, df_inv)
    elif "Company Overview" in nav_selection:
        company_overview.render(df_trans_filtered, df_inv)
    elif "Sales Analytics" in nav_selection:
        sales_performance.render(df_trans_filtered, df_inv)
    elif "Product Details" in nav_selection:
        product_performance.render(df_trans_filtered, df_inv)
    elif "Category Performance" in nav_selection:
        category_performance.render(df_trans_filtered, df_inv)
    elif "Inventory Dashboard" in nav_selection:
        inventory_health.render(df_trans_filtered, df_inv)
    elif "Risk Dashboard" in nav_selection:
        stock_risk.render(df_trans_filtered, df_inv)
    elif "Overstock Dashboard" in nav_selection:
        overstock.render(df_trans_filtered, df_inv)
    elif "Promotion Analysis" in nav_selection:
        promotion_analysis.render(df_trans_filtered, df_inv)
    elif "Seasonality Center" in nav_selection:
        seasonality.render(df_trans_filtered, df_inv)
    elif "Demand Forecast" in nav_selection:
        forecast.render(df_trans_filtered, df_inv)
    elif "Customer Insights" in nav_selection:
        customer_insights.render(df_trans_filtered, df_inv)
    elif "Recommendation Engine" in nav_selection:
        recommendation.render(df_trans_filtered, df_inv)
    elif "What-If Simulator" in nav_selection:
        what_if_simulator.render(df_trans_filtered, df_inv)
    elif "Alerts Center" in nav_selection:
        alerts_center.render(df_trans_filtered, df_inv)
    elif "Executive Presentation" in nav_selection:
        executive_presentation.render(df_trans_filtered, df_inv)

if __name__ == "__main__":
    main()
