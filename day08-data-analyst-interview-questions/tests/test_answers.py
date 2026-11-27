"""Every interview answer is checked a second, independent way."""
import os, json, sqlite3, pandas as pd
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); con = sqlite3.connect(os.path.join(H, "data", "kaveri_mart.db"))
S = json.load(open(os.path.join(H, "output", "sql_answers.json"))); P = json.load(open(os.path.join(H, "output", "pandas_answers.json")))
o, c, p = (pd.read_sql(f"SELECT * FROM {t}", con) for t in ("orders", "customers", "products"))
d = o[o.status == "Delivered"].merge(p, on="product_id"); d["value"] = d.qty * d.unit_price
def test_q1_duplicates(): assert S["q1_duplicates_count"]["rows"][0][0] == int((c.email.value_counts() > 1).sum())
def test_q2_second_highest(): assert S["q2_second_highest"]["rows"][0][0] == sorted(set(d.value))[-2]
def test_q3_top_per_city():
    r = d.merge(c, on="customer_id").groupby(["city", "customer_id", "name"]).value.sum().reset_index()
    best = r.sort_values(["value", "name"], ascending=[False, True]).groupby("city").head(1)
    assert {(x[0], x[1], x[2]) for x in S["q3_top_per_city"]["rows"]} == {(t.city, t.name, t.value) for t in best.itertuples()}
def test_q4_growth():
    m = d.groupby(d.order_date.str[:7]).value.sum(); g = (m.pct_change() * 100).round(1)
    assert [r[2] for r in S["q4_mom_growth"]["rows"]][1:] == g.iloc[1:].tolist()
def test_q5_jan_not_feb():
    jan = set(o[o.order_date.str[:7] == "2026-01"].customer_id); feb = set(o[o.order_date.str[:7] == "2026-02"].customer_id)
    assert S["q5_jan_not_feb"]["rows"][0][0] == len(jan - feb)
def test_q6_missing():
    ex = pd.read_csv(os.path.join(H, "data", "orders_export.csv"))
    assert P["q6_missing"] == {"qty": int(ex.qty.isna().sum()), "city": int(ex.city.isna().sum())}
def test_q7_one_row_per_order(): assert P["q7_rows_after"] == o.order_id.nunique() and P["q7_rows_before"] - P["q7_rows_after"] == 40
def test_q8_top2():
    for cat, prod, rev in P["q8_top2"]:
        s = d[d.category == cat].groupby("product_name").value.sum().sort_values(ascending=False)
        assert prod in s.index[:2] and s[prod] == rev
def test_q9_orphans(): assert P["q9_orphans"] == int((~o.customer_id.isin(c.customer_id)).sum())
def test_q10_rolling():
    daily = {}
    for r in d.itertuples(): daily[r.order_date] = daily.get(r.order_date, 0) + r.value
    days = pd.date_range("2026-01-01", "2026-06-30").strftime("%Y-%m-%d"); v = [daily.get(x, 0) for x in days]
    best = max(range(6, len(v)), key=lambda i: sum(v[i - 6:i + 1])); assert [days[best], round(sum(v[best - 6:best + 1]) / 7)] == P["q10_best_7day_avg"]
