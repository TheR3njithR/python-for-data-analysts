"""Every SQL answer is recomputed independently with pandas."""
import os, json, sqlite3, pandas as pd
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); con = sqlite3.connect(os.path.join(H, "data", "ganga_retail.db"))
o, c, p = (pd.read_sql(f"SELECT * FROM {t}", con) for t in ("orders", "customers", "products"))
R = json.load(open(os.path.join(H, "output", "query_results.json")))
d = o.merge(p, on="product_id").merge(c, on="customer_id"); d["net"] = d.qty * d.unit_price * (1 - d.discount_pct / 100)
dl = d[d.status == "Delivered"]
def test_where_count(): assert R["q1_where_count"]["rows"][0][0] == len(o[(o.status == "Delivered") & (o.order_date >= "2026-10-01") & (o.qty >= 3)])
def test_order_by(): assert [r[0] for r in R["q2_order_by"]["rows"]] == p.sort_values("unit_price", ascending=False).product_name.head(5).tolist()
def test_group_by():
    g = dl.groupby("category").net.sum()
    sql = {r[0]: r[2] for r in R["q3_group_by"]["rows"]}
    assert sql.keys() == g.to_dict().keys() and all(abs(sql[k] - g[k]) <= 1 for k in sql)       # whole rupees: allow rounding of the last rupee
def test_having():
    g = (d.assign(nd=d.status != "Delivered").groupby("city").nd.mean() * 100).round(1)
    assert {r[0] for r in R["q4_having"]["rows"]} == set(g[g > 15].index)
def test_join_top5():
    g = dl.groupby(["segment", "city"]).net.sum().sort_values(ascending=False).head(5)
    assert [tuple(r[:2]) for r in R["q5_join"]["rows"]] == list(g.index) and all(abs(r[2] - v) <= 1 for r, v in zip(R["q5_join"]["rows"], g))
def test_left_join(): assert R["q6_left_join"]["rows"][0][0] == len(set(c.customer_id) - set(o.customer_id))
