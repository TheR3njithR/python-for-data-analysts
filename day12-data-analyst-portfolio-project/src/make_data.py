"""Synthetic sales for Kaveri Mart, a made-up Indian retail chain. Seeded: every run is identical."""
import numpy as np, pandas as pd
rng = np.random.default_rng(1201)
stores = pd.DataFrame({"store_id": range(1, 9),
    "city": ["Chennai", "Chennai", "Bengaluru", "Bengaluru", "Hyderabad", "Kochi", "Pune", "Coimbatore"]})
cats = {"Groceries": 420, "Personal Care": 310, "Home": 900, "Apparel": 1200, "Electronics": 2600}
season = np.array([0.9, 0.85, 0.95, 0.95, 1.0, 0.95, 0.95, 1.0, 1.05, 1.35, 1.25, 1.1])  # Oct/Nov festive bump
n_cust, rows = 5000, []
cust_store = rng.integers(1, 9, n_cust)
cust_rate = rng.gamma(1.2, 1.0, n_cust)
order_id = 100000
for c in range(n_cust):
    k = rng.poisson(cust_rate[c] * 1.6)
    for _ in range(k):
        m = rng.choice(12, p=season / season.sum()); day = rng.integers(1, 29)
        order_id += 1
        for _ in range(rng.integers(1, 4)):
            cat = rng.choice(list(cats), p=[0.4, 0.25, 0.15, 0.12, 0.08])
            price = round(float(cats[cat] * rng.uniform(0.5, 1.6)), 2)
            rows.append((order_id, f"2025-{m+1:02d}-{day:02d}", f"C{c+1:05d}", int(cust_store[c]), cat, int(rng.integers(1, 4)), price))
o = pd.DataFrame(rows, columns=["order_id", "order_date", "customer_id", "store_id", "category", "qty", "unit_price"])
dup = o.sample(120, random_state=1); o = pd.concat([o, dup]).sample(frac=1, random_state=2)   # 120 duplicate lines, like a real export
o.loc[o.sample(40, random_state=3).index, "unit_price"] = np.nan                            # 40 lines with a missing price
o.to_csv("data/orders.csv", index=False); stores.to_csv("data/stores.csv", index=False)
print(f"orders.csv: {len(o):,} lines, {o.order_id.nunique():,} orders, {o.customer_id.nunique():,} customers; stores.csv: {len(stores)} stores")
