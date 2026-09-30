import os
import pandas as pd
import numpy as np
import streamlit as st

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

@st.cache_data(show_spinner=False)
def load_raw_data():
    trans_path = os.path.join(DATA_DIR, "raw_transactions.csv")
    inv_path = os.path.join(DATA_DIR, "inventory_master.csv")

    if not os.path.exists(trans_path) or not os.path.exists(inv_path):
        from data.generate_data import generate_foresight_data
        generate_foresight_data()

    df_trans = pd.read_csv(trans_path)
    df_inv = pd.read_csv(inv_path)

    df_trans["Date"] = pd.to_datetime(df_trans["Date"])
    df_trans["Year"] = df_trans["Date"].dt.year
    df_trans["Month"] = df_trans["Date"].dt.strftime("%b %Y")
    df_trans["MonthNum"] = df_trans["Date"].dt.month

    # Season Mapping
    def get_season(month):
        if month in [12, 1, 2]:
            return "Winter"
        elif month in [3, 4, 5]:
            return "Spring"
        elif month in [6, 7, 8]:
            return "Summer"
        else:
            return "Fall"

    df_trans["Season"] = df_trans["MonthNum"].apply(get_season)

    # Subcategory mapping
    subcat_map = {
        "LIV-SOFA-01": "Sofas", "LIV-TABL-02": "Tables", "LIV-CHAIR-03": "Chairs", "LIV-SHELF-04": "Shelving",
        "LGT-PNDT-10": "Pendant Lights", "LGT-LAMP-11": "Table Lamps", "LGT-WALL-12": "Wall Art", "LGT-STRIP-13": "Floor Lamps",
        "DEC-VASH-20": "Vases", "DEC-MIRR-21": "Mirrors", "DEC-RUG-22": "Rugs", "DEC-ART-23": "Wall Art",
        "KTC-COOK-30": "Cookware", "KTC-CUTL-31": "Dinnerware", "KTC-DISH-32": "Dinnerware", "KTC-MUG-33": "Storage Containers",
        "BED-SHET-40": "Bedding", "BED-PILL-41": "Cushions", "BTH-TWEL-42": "Throws", "BTH-MAT-43": "Baskets"
    }
    df_trans["Subcategory"] = df_trans["SKU"].map(subcat_map).fillna("General")
    df_inv["Subcategory"] = df_inv["SKU"].map(subcat_map).fillna("General")

    # Add promotion indicators
    # 15% of transactions tagged as promotions
    np.random.seed(42)
    promo_indices = np.random.choice(df_trans.index, size=int(len(df_trans) * 0.18), replace=False)
    df_trans["IsPromo"] = False
    df_trans.loc[promo_indices, "IsPromo"] = True
    df_trans["PromoEvent"] = "Regular"

    events = ["Black Friday", "Cyber Monday", "Holiday Gift", "New Year Sale", "Labor Day Sale", "Valentine's Sale", "July 4th Sale", "Memorial Day Sale"]
    df_trans.loc[promo_indices, "PromoEvent"] = np.random.choice(events, size=len(promo_indices))

    return df_trans, df_inv

def filter_data(df_trans, start_date=None, end_date=None, categories=None, subcategories=None, skus=None, seasons=None):
    df_filtered = df_trans.copy()

    if start_date:
        df_filtered = df_filtered[df_filtered["Date"] >= pd.to_datetime(start_date)]
    if end_date:
        df_filtered = df_filtered[df_filtered["Date"] <= pd.to_datetime(end_date)]

    if categories and "All" not in categories and len(categories) > 0:
        df_filtered = df_filtered[df_filtered["Category"].isin(categories)]

    if subcategories and "All" not in subcategories and len(subcategories) > 0:
        df_filtered = df_filtered[df_filtered["Subcategory"].isin(subcategories)]

    if skus and "All" not in skus and len(skus) > 0:
        df_filtered = df_filtered[df_filtered["SKU"].isin(skus)]

    if seasons and "All" not in seasons and len(seasons) > 0:
        df_filtered = df_filtered[df_filtered["Season"].isin(seasons)]

    return df_filtered
