"""Godavari Traders: a fully synthetic sales file for the Day 9 Streamlit dashboard (seed 901). No real company or person."""
import numpy as np, pandas as pd
rng = np.random.default_rng(901)
products = {
    "Electronics": {"Smartwatch": 3999, "Bluetooth Speaker": 2499, "Power Bank": 1299, "Earbuds": 1799},
    "Grocery": {"Basmati Rice 5 kg": 649, "Ghee 1 L": 599, "Tea 500 g": 289, "Cashews 500 g": 549},
    "Home": {"Mixer Grinder": 3299, "Pressure Cooker": 1899, "Bedsheet Set": 999, "Water Bottle": 349},
    "Personal Care": {"Trimmer": 1499, "Sunscreen": 399, "Shampoo": 299, "Face Wash": 249},
}
cities = ["Chennai", "Delhi", "Hyderabad", "Kochi", "Mumbai", "Pune"]
cw = np.array([0.18, 0.2, 0.15, 0.1, 0.22, 0.15])
rows, n = [], 9000
days = pd.date_range("2026-01-01", "2026-09-30", freq="D")
season = 1 + 0.25 * np.sin(np.arange(len(days)) / 365 * 2 * np.pi * 1.5) + np.where(days.month == 8, 0.35, 0)  # August festival push
dayp = season / season.sum()
cat_names = list(products); catw = np.array([0.24, 0.34, 0.22, 0.2])
for i in range(n):
    cat = cat_names[rng.choice(4, p=catw)]; prod = rng.choice(list(products[cat]))
    rows.append(dict(order_id=f"GT{100001 + i}", order_date=days[rng.choice(len(days), p=dayp)].date().isoformat(),
                     city=cities[rng.choice(6, p=cw)], channel="Online" if rng.random() < 0.58 else "Store",
                     category=cat, product=prod, qty=int(rng.choice([1, 1, 1, 2, 2, 3, 4])), unit_price=products[cat][prod]))
df = pd.DataFrame(rows).sort_values(["order_date", "order_id"]).reset_index(drop=True)
df["revenue"] = df.qty * df.unit_price
df.to_csv("data/sales.csv", index=False)
print(f"wrote data/sales.csv: {len(df):,} rows, {df.order_date.min()} to {df.order_date.max()}, revenue {df.revenue.sum():,}")
