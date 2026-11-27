import sqlite3, pandas as pd
db = sqlite3.connect("data/kaveri.db"); o = pd.read_sql("SELECT * FROM orders", db)
def test_no_duplicate_lines(): assert not o.duplicated().any()
def test_no_missing_prices(): assert o.unit_price.notna().all()
def test_sql_total_matches_pandas():
    sql = pd.read_sql("SELECT SUM(revenue) AS t FROM orders", db).t[0]
    assert abs(sql - (o.qty * o.unit_price).round(2).sum()) < 1
def test_city_totals_add_up():
    city = pd.read_sql(open("sql/01_revenue_by_city.sql").read(), db)
    assert abs(city.revenue_lakh.sum() - o.revenue.sum() / 1e5) < 0.5
