"""Independent check: the same city totals with pandas, reading the CSV in 1-million-row chunks (bounded memory). Usage: python pandas_check.py"""
import os, sys, time, json, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    import gate
except ImportError:
    gate = None
H = os.path.dirname(os.path.abspath(__file__)); CSV = os.path.join(H, "data", "nilgiri_sales.csv")
tot = None; n = 0; s = 0.0; it = iter(pd.read_csv(CSV, usecols=["city", "qty", "unit_price", "discount_pct"], chunksize=1_000_000))
while True:
    gate and gate.wait("pandas chunk"); t = time.perf_counter()
    ch = next(it, None)
    if ch is None: break
    ch["net"] = ch.qty * ch.unit_price * (1 - ch.discount_pct / 100); g = ch.groupby("city").net.agg(["sum", "count"])
    tot = g if tot is None else tot.add(g, fill_value=0); n += len(ch); s += time.perf_counter() - t
tot = tot.sort_values("sum", ascending=False)
out = {"seconds": round(s, 2), "rows": n, "city": {c: {"net_revenue_crore": round(r["sum"] / 1e7, 2), "orders": int(r["count"])} for c, r in tot.iterrows()}}
print(f"pandas, 1M-row chunks: {n:,} rows in {s:.1f} s"); print(json.dumps(out["city"], indent=1))
json.dump(out, open(os.path.join(H, "output", "pandas_check.json"), "w"), indent=1)
