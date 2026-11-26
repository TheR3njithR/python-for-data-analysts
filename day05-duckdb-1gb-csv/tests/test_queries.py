import os, json
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = json.load(open(os.path.join(H, "output", "query_results.json"))); P = json.load(open(os.path.join(H, "output", "pandas_check.json")))
def test_row_count_matches_pandas(): assert R["q1_count"]["rows"][0]["orders"] == P["rows"]
def test_city_totals_match_pandas():
    for r in R["q2_city_revenue"]["rows"]:
        assert abs(r["net_revenue_crore"] - P["city"][r["city"]]["net_revenue_crore"]) <= 0.01 and r["orders"] == P["city"][r["city"]]["orders"]
def test_parquet_gives_same_answer(): assert R["q2_city_revenue"]["rows"] == R["q2_city_revenue_parquet"]["rows"] and R["q4_top_products"]["rows"] == R["q4_top_products_parquet"]["rows"]
def test_parquet_is_smaller(): assert R["parquet_bytes"] < R["csv_bytes"]
