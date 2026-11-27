"""Q6-Q10: the pandas interview questions, on data/orders_export.csv (messy export) and data/kaveri_mart.db. Saves output/pandas_answers.json.
Usage: python pandas_answers.py"""
import os, json, sqlite3, pandas as pd
H = os.path.dirname(os.path.abspath(__file__)); con = sqlite3.connect(os.path.join(H, "data", "kaveri_mart.db"))
ex = pd.read_csv(os.path.join(H, "data", "orders_export.csv"))
A = {}
# Q6 missing values per column, then fill city with 'Unknown'
miss = ex.isna().sum(); A["q6_missing"] = {k: int(v) for k, v in miss[miss > 0].items()}
# Q7 duplicates: keep the latest export of each order
latest = ex.sort_values("exported_at").drop_duplicates("order_id", keep="last")
A["q7_rows_before"], A["q7_rows_after"] = len(ex), len(latest)
first_seen = ex.sort_values("exported_at").drop_duplicates("order_id", keep="first").set_index("order_id").status.sort_index()
A["q7_status_changed"] = int((first_seen != latest.set_index("order_id").status.sort_index()).sum())
# Q8 top 2 products per category by delivered revenue
o = pd.read_sql("SELECT * FROM orders", con); p = pd.read_sql("SELECT * FROM products", con); c = pd.read_sql("SELECT * FROM customers", con)
d = o[o.status == "Delivered"].merge(p, on="product_id"); d["revenue"] = d.qty * d.unit_price
top = (d.groupby(["category", "product_name"]).revenue.sum().reset_index().sort_values(["category", "revenue"], ascending=[True, False])
         .groupby("category").head(2))
A["q8_top2"] = [[r.category, r.product_name, int(r.revenue)] for r in top.itertuples()]
# Q9 orders whose customer_id is not in customers (merge indicator)
m = o.merge(c[["customer_id"]], on="customer_id", how="left", indicator=True)
A["q9_orphans"] = int((m._merge == "left_only").sum())
# Q10 7-day rolling average of daily delivered revenue
daily = d.assign(order_date=pd.to_datetime(d.order_date)).set_index("order_date").revenue.resample("D").sum()
roll = daily.rolling(7).mean()
A["q10_best_7day_avg"] = [roll.idxmax().strftime("%Y-%m-%d"), round(float(roll.max()))]
A["q10_days"] = len(daily)
json.dump(A, open(os.path.join(H, "output", "pandas_answers.json"), "w"), indent=1); print(json.dumps(A, indent=1))
