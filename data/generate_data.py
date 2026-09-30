import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_foresight_data():
    np.random.seed(42)
    output_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(output_dir, exist_ok=True)

    # Date range: 2009-12-01 to 2011-12-09
    start_date = datetime(2009, 12, 1)
    end_date = datetime(2011, 12, 9)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')

    categories = {
        "Living & Furniture": ["LIV-SOFA-01", "LIV-TABL-02", "LIV-CHAIR-03", "LIV-SHELF-04"],
        "Lighting": ["LGT-PNDT-10", "LGT-LAMP-11", "LGT-WALL-12", "LGT-STRIP-13"],
        "Home Decor": ["DEC-VASH-20", "DEC-MIRR-21", "DEC-RUG-22", "DEC-ART-23"],
        "Kitchenware": ["KTC-COOK-30", "KTC-CUTL-31", "KTC-DISH-32", "KTC-MUG-33"],
        "Bed & Bath": ["BED-SHET-40", "BED-PILL-41", "BTH-TWEL-42", "BTH-MAT-43"]
    }

    sku_master = []
    transactions = []

    sku_names = {
        "LIV-SOFA-01": "Nordic Fabric Sofa 3-Seater",
        "LIV-TABL-02": "Minimalist Oak Coffee Table",
        "LIV-CHAIR-03": "Ergonomic Accent Lounge Chair",
        "LIV-SHELF-04": "Modular Floating Wall Shelf",
        "LGT-PNDT-10": "Industrial Brass Pendant Light",
        "LGT-LAMP-11": "Dimmable Ceramic Table Lamp",
        "LGT-WALL-12": "Modern Sconce Wall Fixture",
        "LGT-STRIP-13": "Smart RGB LED Ambient Strip",
        "DEC-VASH-20": "Handcrafted Ceramic Flower Vase",
        "DEC-MIRR-21": "Round Brass Framed Wall Mirror",
        "DEC-RUG-22": "Bohemian Handwoven Wool Rug",
        "DEC-ART-23": "Abstract Canvas Wall Art Set",
        "KTC-COOK-30": "Non-Stick Cast Iron Skillet Set",
        "KTC-CUTL-31": "Stainless Steel Chef Knife Set",
        "KTC-DISH-32": "Porcelain Dinnerware 16-Piece",
        "KTC-MUG-33": "Matte Stoneware Coffee Mugs",
        "BED-SHET-40": "100% Egyptian Cotton Sheet Set",
        "BED-PILL-41": "Memory Foam Ergonomic Pillow",
        "BTH-TWEL-42": "Organic Turkish Bath Towels",
        "BTH-MAT-43": "Quick-Dry Diatomite Bath Mat"
    }

    base_prices = {
        "LIV-SOFA-01": 899.0, "LIV-TABL-02": 299.0, "LIV-CHAIR-03": 199.0, "LIV-SHELF-04": 120.0,
        "LGT-PNDT-10": 149.0, "LGT-LAMP-11": 89.0,  "LGT-WALL-12": 75.0,  "LGT-STRIP-13": 45.0,
        "DEC-VASH-20": 55.0,  "DEC-MIRR-21": 135.0, "DEC-RUG-22": 240.0, "DEC-ART-23": 110.0,
        "KTC-COOK-30": 160.0, "KTC-CUTL-31": 95.0,  "KTC-DISH-32": 130.0, "KTC-MUG-33": 35.0,
        "BED-SHET-40": 115.0, "BED-PILL-41": 65.0,  "BTH-TWEL-42": 48.0,  "BTH-MAT-43": 38.0
    }

    unit_costs = {sku: round(price * np.random.uniform(0.45, 0.60), 2) for sku, price in base_prices.items()}

    # Create SKU Master dataframe
    for cat, skus in categories.items():
        for sku in skus:
            lead_time = int(np.random.choice([5, 7, 10, 14, 21]))
            current_stock = int(np.random.randint(20, 350))
            reorder_point = int(np.random.randint(30, 100))
            safety_stock = int(np.random.randint(15, 50))
            holding_cost_annual = round(unit_costs[sku] * 0.18, 2)
            ordering_cost = float(np.random.choice([50.0, 75.0, 100.0]))
            supplier = f"Supplier-{np.random.choice(['Alpha', 'Apex', 'Beacon', 'Crown', 'Delta'])}"

            sku_master.append({
                "SKU": sku,
                "ProductName": sku_names[sku],
                "Category": cat,
                "UnitPrice": base_prices[sku],
                "UnitCost": unit_costs[sku],
                "CurrentStock": current_stock,
                "SafetyStock": safety_stock,
                "ReorderPoint": reorder_point,
                "LeadTimeDays": lead_time,
                "HoldingCostAnnual": holding_cost_annual,
                "OrderingCost": ordering_cost,
                "Supplier": supplier,
                "WarehouseLocation": np.random.choice(["WH-North", "WH-East", "WH-West", "WH-Central"])
            })

    df_sku = pd.DataFrame(sku_master)

    # Generate daily sales transactions
    countries = ["United Kingdom", "Germany", "France", "United States", "EIRE", "Spain", "Netherlands"]
    country_weights = [0.65, 0.10, 0.08, 0.07, 0.04, 0.03, 0.03]

    trans_id = 100000
    for day in date_range:
        day_of_year = day.dayofyear
        # Seasonality factor (peaks in Nov-Dec)
        seasonality = 1.0 + 0.6 * np.exp(-((day.month - 11.5)**2) / 1.2) + 0.15 * np.sin(2 * np.pi * day_of_year / 365.25)
        is_weekend = 1.2 if day.weekday() >= 5 else 1.0

        for sku, name in sku_names.items():
            base_demand = np.random.poisson(lam=max(1, int(12 * seasonality * is_weekend * (base_prices[sku]**-0.2))))
            if base_demand > 0:
                # Divide demand into multiple customer orders
                num_orders = max(1, int(np.random.exponential(scale=base_demand / 3)))
                qty_per_order = max(1, base_demand // num_orders)

                for _ in range(num_orders):
                    country = np.random.choice(countries, p=country_weights)
                    qty = max(1, int(np.random.negative_binomial(n=3, p=0.4)))
                    discount = float(np.random.choice([0.0, 0.05, 0.10, 0.15], p=[0.7, 0.15, 0.10, 0.05]))
                    price = round(base_prices[sku] * (1.0 - discount), 2)
                    revenue = round(qty * price, 2)
                    cost = round(qty * unit_costs[sku], 2)

                    transactions.append({
                        "InvoiceNo": f"INV-{trans_id}",
                        "Date": day.strftime("%Y-%m-%d"),
                        "SKU": sku,
                        "ProductName": name,
                        "Category": [c for c, sks in categories.items() if sku in sks][0],
                        "Quantity": qty,
                        "UnitPrice": price,
                        "TotalRevenue": revenue,
                        "TotalCost": cost,
                        "Profit": round(revenue - cost, 2),
                        "Country": country,
                        "CustomerID": f"CUST-{np.random.randint(1000, 1800)}"
                    })
                    trans_id += 1

    df_trans = pd.DataFrame(transactions)

    # Save to CSV files
    df_sku.to_csv(os.path.join(output_dir, "inventory_master.csv"), index=False)
    df_trans.to_csv(os.path.join(output_dir, "raw_transactions.csv"), index=False)
    print(f"Generated {len(df_trans)} transactions and {len(df_sku)} SKUs successfully.")

if __name__ == "__main__":
    generate_foresight_data()
