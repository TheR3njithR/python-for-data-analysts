"""Synthetic monthly sales for Kaveri Mart (made up): 8 stores, Jan-Jun 2026, into data/kaveri.db (SQLite)."""
import sqlite3, numpy as np
rng = np.random.default_rng(1701)
stores = [("Chennai", "Chennai-1"), ("Chennai", "Chennai-2"), ("Bengaluru", "Bengaluru-1"), ("Bengaluru", "Bengaluru-2"),
          ("Hyderabad", "Hyderabad-1"), ("Pune", "Pune-1"), ("Kochi", "Kochi-1"), ("Mumbai", "Mumbai-1")]
months = ["2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "2026-06"]
rows = []
for city, store in stores:
    base = rng.integers(8, 14) * 1e5
    for i, m in enumerate(months):
        rows.append((m, city, store, int(round(base * (1 + 0.04 * i) * rng.uniform(0.85, 1.15), -3))))
jun = [r for r in rows if r[0] == "2026-06"]                       # one deliberate tie in June, to show RANK vs ROW_NUMBER
a, b = sorted(jun, key=lambda r: -r[3])[1:3]
rows[rows.index(b)] = (b[0], b[1], b[2], a[3])
con = sqlite3.connect("data/kaveri.db"); con.execute("DROP TABLE IF EXISTS monthly_sales")
con.execute("CREATE TABLE monthly_sales (month TEXT, city TEXT, store TEXT, revenue INTEGER)")
con.executemany("INSERT INTO monthly_sales VALUES (?,?,?,?)", rows); con.commit()
print(f"monthly_sales: {len(rows)} rows, {len(stores)} stores, {len(months)} months")
