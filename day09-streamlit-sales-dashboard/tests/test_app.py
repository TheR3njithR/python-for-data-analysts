"""Run the real app headless with Streamlit's AppTest and check every KPI against plain pandas."""
from pathlib import Path
import pandas as pd
from streamlit.testing.v1 import AppTest

HERE = Path(__file__).resolve().parents[1]
DF = pd.read_csv(HERE / "data" / "sales.csv")


def run(**kw):
    import os
    os.chdir(HERE)
    at = AppTest.from_file(str(HERE / "app.py")).run()
    for label, value in kw.items():
        w = {"city": at.multiselect[0], "category": at.multiselect[1], "channel": at.radio[0]}[label]
        w.set_value(value)
    return at.run() if kw else at


def metrics(at):
    return {m.label: m.value for m in at.metric}


def test_totals_match_pandas():
    m = metrics(run())
    assert m["Revenue"] == f"₹{DF.revenue.sum() / 1e5:,.2f} lakh"
    assert m["Orders"] == f"{len(DF):,}"


def test_city_filter():
    v = DF[DF.city == "Pune"]
    m = metrics(run(city=["Pune"]))
    assert m["Revenue"] == f"₹{v.revenue.sum() / 1e5:,.2f} lakh"
    assert m["Orders"] == f"{len(v):,}"


def test_city_and_channel_filter():
    v = DF[(DF.city == "Pune") & (DF.channel == "Online")]
    m = metrics(run(city=["Pune"], channel="Online"))
    assert m["Average order value"] == f"₹{v.revenue.sum() / len(v):,.0f}"


def test_top_products_table():
    at = run()
    top = at.dataframe[0].value
    expect = DF.groupby("product").revenue.sum().nlargest(5)
    assert list(top["product"]) == list(expect.index)


def test_empty_filter_shows_warning():
    at = run(city=[])
    assert at.warning[0].value == "No orders match these filters."
    assert len(at.metric) == 0
