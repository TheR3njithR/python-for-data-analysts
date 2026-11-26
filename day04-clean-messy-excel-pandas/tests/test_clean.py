import os, sys, pandas as pd
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, H)
import clean_sales as cs
df, issues = cs.clean(os.path.join(H, "input", "Kaveri_Orders_Oct2026.xlsx"), log=lambda s: None)
key = pd.read_csv(os.path.join(H, "_answer_key", "clean_truth.csv"), parse_dates=["order_date"]).sort_values("order_id").reset_index(drop=True)
def test_row_count_matches_truth(): assert len(df) == len(key)
def test_dates_match_truth(): assert (df.order_date.values == key.order_date.values).all()
def test_no_duplicates_left(): assert not df.order_id.duplicated().any()
def test_cities_match_truth(): assert (df.city.values == key.city.values).all()
def test_discount_rule(): assert (df.discount_pct.values == key.discount_pct.values).all()
def test_missing_amounts_flagged_not_filled(): assert len(issues) == int(key.amount.isna().sum()) and df.amount.isna().sum() == len(issues)
def test_almost_empty_column_dropped(): assert "landline" not in df.columns
