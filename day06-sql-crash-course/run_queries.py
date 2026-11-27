"""Run every query in queries.sql against data/ganga_retail.db and print the results (sqlite3 ships with Python). Usage: python run_queries.py"""
import os, re, json, sqlite3, time
H = os.path.dirname(os.path.abspath(__file__)); con = sqlite3.connect(os.path.join(H, "data", "ganga_retail.db"))
blocks = re.split(r"^-- name: (\w+)\n", open(os.path.join(H, "queries.sql")).read(), flags=re.M)[1:]
out = {}
for name, sql in zip(blocks[::2], blocks[1::2]):
    t = time.perf_counter(); cur = con.execute(sql); rows = cur.fetchall(); s = time.perf_counter() - t
    cols = [d[0] for d in cur.description]; out[name] = {"cols": cols, "rows": rows, "ms": round(s * 1000, 1)}
    print(f"\n== {name}  ({len(rows)} rows, {s * 1000:.1f} ms)\n{sql.strip()}\n" + " | ".join(cols))
    for r in rows: print(" | ".join(f"{v:,.0f}" if isinstance(v, float) and abs(v) >= 1000 else str(v) for v in r))
json.dump(out, open(os.path.join(H, "output", "query_results.json"), "w"), indent=1)
