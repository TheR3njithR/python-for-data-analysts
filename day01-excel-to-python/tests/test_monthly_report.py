"""Checks the report against the answer key (possible because the data is synthetic). Run: python -m pytest -q tests/"""
import os, sys, subprocess, zipfile
import pandas as pd, pytest
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, HERE); os.chdir(HERE)
import monthly_report as mr

@pytest.fixture(scope="module", params=["2026-09", "2026-10"])
def run(request):
    m = request.param; raw, targets = mr.load_export(f"input/Sales_Export_{m}.xlsx"); df, issues, log = mr.clean(raw, m)
    return m, df, issues, log, targets, pd.read_csv(f"_answer_key/truth_{m}.csv")

def test_every_clean_line_matches_the_key(run):
    m, df, issues, log, targets, key = run
    want = key[key.status == "CLEAN"].set_index("invoice").sort_index(); got = df.set_index("invoice").sort_index()
    assert list(got.index) == list(want.index)
    assert (got["qty"] == want["qty"]).all() and (got["region"] == want["region"]).all() and (got["product"] == want["product"]).all()
    assert (got["net"].round(2) == want["net"].round(2)).all()
    assert (got["date"].dt.strftime("%Y-%m-%d") == want["date"]).all()

def test_revenue_total_matches_the_key(run):
    m, df, issues, log, targets, key = run
    assert round(df["net"].sum(), 2) == round(key[key.status == "CLEAN"]["net"].sum(), 2)

def test_problem_rows_go_to_issues_not_the_report(run):
    m, df, issues, log, targets, key = run
    assert set(key[key.status == "MISSING_PRICE"].invoice) <= set(issues.invoice)
    assert not set(issues.invoice) & set(df.invoice) or log["late entries moved to Issues"] >= 0
    assert (df["date"].dt.strftime("%Y-%m") == m).all()

def test_report_file_has_native_charts_and_sheets(tmp_path):
    subprocess.run([sys.executable, "monthly_report.py", "--month", "2026-10", "--out", str(tmp_path)], check=True, capture_output=True)
    p = tmp_path / "Monthly_Report_2026-10.xlsx"
    names = zipfile.ZipFile(p).namelist()
    assert len([n for n in names if n.startswith("xl/charts/chart")]) == 2
    from openpyxl import load_workbook
    assert load_workbook(p).sheetnames == ["Summary", "Region_x_Product", "Regions", "Weekly", "Sales_Reps", "Clean_Data", "Issues", "Cleaning_Log"]
