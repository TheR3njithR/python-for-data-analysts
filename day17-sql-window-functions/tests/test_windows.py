import sqlite3, pandas as pd
con = sqlite3.connect("data/kaveri.db"); df = pd.read_sql("SELECT * FROM monthly_sales", con)
q = lambda f: pd.read_sql(open(f"sql/{f}").read(), con)
def test_rank_matches_pandas():
    r = q("01_rank.sql"); jun = df[df.month == "2026-06"]
    assert sorted(r.rnk) == sorted(jun.revenue.rank(method="min", ascending=False).astype(int))
def test_june_has_one_tie():
    r = q("01_rank.sql"); assert r.rnk.duplicated().sum() == 1 and r.row_num.is_unique
def test_lag_matches_pandas_diff():
    s = df[df.store == "Kochi-1"].sort_values("month").revenue.diff()
    assert q("02_lag.sql").change.iloc[1:].tolist() == s.iloc[1:].astype(int).tolist()
def test_running_total_matches_cumsum():
    s = df[df.store == "Kochi-1"].sort_values("month").revenue.cumsum()
    assert q("03_running_total.sql").running_total.tolist() == s.tolist()
def test_one_best_month_per_store():
    assert len(q("04_best_month.sql")) == 8
