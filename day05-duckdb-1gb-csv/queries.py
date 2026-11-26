"""Query the big CSV with SQL using DuckDB (no server), timing every query. Usage: python queries.py
DuckDB is held to 4 threads and a 2 GB memory limit, like a modest laptop."""
import os, sys, time, json, duckdb
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    import gate
except ImportError:
    gate = None
H = os.path.dirname(os.path.abspath(__file__)); CSV = os.path.join(H, "data", "nilgiri_sales.csv"); PQ = os.path.join(H, "data", "nilgiri_sales.parquet")
con = duckdb.connect(); con.execute("SET threads = 4; SET memory_limit = '2GB'")
res = {"csv_bytes": os.path.getsize(CSV), "duckdb": duckdb.__version__}
def q(name, sql, show=True):
    while True:
        gate and gate.wait(name); t = time.perf_counter(); df = con.execute(sql).df(); s = time.perf_counter() - t
        if not (gate and gate.busy()): break        # a clone started mid-query: the timing is not clean, run it again
    res[name] = {"seconds": round(s, 2), "rows": df.head(12).to_dict("records")}
    print(f"\n-- {name}: {s:.2f} s\n{sql.strip()}"); show and print(df.head(12).to_string(index=False)); return df
F = f"'{CSV}'"
q("q1_count", f"SELECT count(*) AS orders FROM {F}")
q("q2_city_revenue", f"""SELECT city, round(sum(qty * unit_price * (1 - discount_pct / 100)) / 1e7, 2) AS net_revenue_crore, count(*) AS orders
FROM {F} GROUP BY city ORDER BY net_revenue_crore DESC, city""")
q("q3_monthly", f"""SELECT strftime(order_date, '%Y-%m') AS month, round(sum(qty * unit_price * (1 - discount_pct / 100)) / 1e7, 2) AS net_revenue_crore
FROM {F} GROUP BY month ORDER BY month""")
q("q4_top_products", f"""SELECT product_id, category, sum(qty) AS units FROM {F}
WHERE city = 'Kochi' AND order_date >= DATE '2026-10-01' GROUP BY ALL ORDER BY units DESC, product_id LIMIT 5""")
gate and gate.wait("parquet"); t = time.perf_counter(); con.execute(f"COPY (SELECT * FROM {F}) TO '{PQ}' (FORMAT parquet)"); res["to_parquet_seconds"] = round(time.perf_counter() - t, 2)
res["parquet_bytes"] = os.path.getsize(PQ); print(f"\n-- CSV -> Parquet: {res['to_parquet_seconds']} s, {res['parquet_bytes']:,} bytes")
P = f"'{PQ}'"
q("q2_city_revenue_parquet", f"""SELECT city, round(sum(qty * unit_price * (1 - discount_pct / 100)) / 1e7, 2) AS net_revenue_crore, count(*) AS orders
FROM {P} GROUP BY city ORDER BY net_revenue_crore DESC, city""")
q("q4_top_products_parquet", f"""SELECT product_id, category, sum(qty) AS units FROM {P}
WHERE city = 'Kochi' AND order_date >= DATE '2026-10-01' GROUP BY ALL ORDER BY units DESC, product_id LIMIT 5""")
json.dump(res, open(os.path.join(H, "output", "query_results.json"), "w"), indent=1, default=str)
