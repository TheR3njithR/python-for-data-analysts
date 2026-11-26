"""Write a ~1 GB synthetic sales CSV for Day 5 (seeded; 'Nilgiri Mart' is a made-up chain, every row is invented).
Usage: python make_big_csv.py [ROWS]   (default 15,000,000 rows -> data/nilgiri_sales.csv)"""
import sys, os, time
import numpy as np, pandas as pd
H = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(H, "data", "nilgiri_sales.csv")
ROWS = int(sys.argv[1]) if len(sys.argv) > 1 else 15_000_000; CHUNK = 500_000
cities = np.array(["Kochi", "Chennai", "Bengaluru", "Hyderabad", "Pune", "Mumbai", "Delhi", "Kolkata"])
stores = np.array([f"S{i:03d}" for i in range(1, 121)]); store_city = cities[np.arange(120) % 8]
cats = np.array(["Grocery", "Snacks", "Beverages", "Personal Care", "Home", "Electronics"])
base_price = np.array([120, 60, 80, 220, 450, 2500]); pay = np.array(["UPI", "Card", "Cash", "Wallet"])
days = pd.date_range("2025-01-01", "2026-10-31").strftime("%Y-%m-%d").to_numpy()
sys.path.insert(0, H)
try:
    import gate
except ImportError:
    gate = None
work = 0.0
with open(OUT, "w") as f:
    f.write("order_id,order_date,store_id,city,category,product_id,qty,unit_price,discount_pct,payment\n")
    for start in range(0, ROWS, CHUNK):
        gate and gate.wait(f'chunk {start}'); t0 = time.perf_counter()
        n = min(CHUNK, ROWS - start); rng = np.random.default_rng([501, start])
        s = rng.integers(0, 120, n); c = rng.choice(6, n, p=[0.32, 0.2, 0.18, 0.12, 0.12, 0.06])
        df = pd.DataFrame({"order_id": np.arange(start + 1, start + n + 1), "order_date": days[rng.integers(0, len(days), n)],
            "store_id": stores[s], "city": store_city[s], "category": cats[c], "product_id": [f"P{x:05d}" for x in c * 1000 + rng.integers(0, 1000, n)],
            "qty": rng.integers(1, 6, n), "unit_price": np.round(base_price[c] * rng.uniform(0.6, 1.6, n), 2),
            "discount_pct": rng.choice([0, 0, 0, 5, 10, 15], n), "payment": pay[rng.choice(4, n, p=[0.55, 0.2, 0.15, 0.1])]})
        df.to_csv(f, header=False, index=False); work += time.perf_counter() - t0
print(f"wrote {ROWS:,} rows, {os.path.getsize(OUT):,} bytes ({os.path.getsize(OUT) / 1e9:.2f} GB) to data/nilgiri_sales.csv in {work:.0f} s of work")
