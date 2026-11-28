"""Synthetic sales lines for Kaveri Mart (made up): 8 stores, 1 Sep - 31 Oct 2026."""
import numpy as np, pandas as pd
rng = np.random.default_rng(1501)
stores = ["Chennai-1", "Chennai-2", "Bengaluru-1", "Bengaluru-2", "Hyderabad-1", "Pune-1", "Kochi-1", "Mumbai-1"]
items = {"Rice 5 kg": 420, "Atta 10 kg": 480, "Sunflower Oil 1 L": 165, "Tea 500 g": 260, "Detergent 2 kg": 390, "Biscuits": 40, "Milk 1 L": 62, "Soap x4": 180}
rows = []
for day in pd.date_range("2026-09-01", "2026-10-31"):
    for s in stores:
        for _ in range(int(rng.integers(30, 60))):
            it = rng.choice(list(items)); q = int(rng.integers(1, 5))
            rows.append((day.date(), s, it, q, items[it] * q))
df = pd.DataFrame(rows, columns=["date", "store", "item", "qty", "amount"])
df.to_csv("data/sales.csv", index=False); print(f"wrote {len(df):,} sales lines, {df.date.nunique()} days, {len(stores)} stores")
