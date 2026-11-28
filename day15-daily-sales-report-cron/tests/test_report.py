import sys; from datetime import date; from email import message_from_bytes
sys.path.insert(0, "src"); import pandas as pd, daily_report as r
D = date(2026, 10, 31)
def test_totals_match_raw_data():
    raw = pd.read_csv("data/sales.csv")
    assert r.build(D).today.sum() == raw[raw.date == str(D)].amount.sum()
def test_every_store_present():
    assert len(r.build(D)) == 8
def test_no_data_day_stops_before_sending():
    import pytest
    with pytest.raises(SystemExit, match="no sales found"): r.build(date(2026, 11, 1))
def test_email_has_csv_attachment(monkeypatch):
    sent = []
    class Fake:
        def __init__(self, *a): pass
        def __enter__(self): return self
        def __exit__(self, *a): pass
        def send_message(self, m): sent.append(m)
    monkeypatch.setattr(r.smtplib, "SMTP", Fake); r.send(r.build(D), D)
    assert [p.get_filename() for p in sent[0].iter_attachments()] == ["sales_2026-10-31.csv"]
