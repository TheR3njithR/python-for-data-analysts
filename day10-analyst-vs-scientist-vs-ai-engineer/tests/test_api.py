"""The AI engineer's safety net: the API answers, rejects bad input, and agrees with the trained model."""
import os, sys
from pathlib import Path
HERE = Path(__file__).resolve().parents[1]; os.chdir(HERE); sys.path.insert(0, str(HERE))
from fastapi.testclient import TestClient
import api

client = TestClient(api.app)
RISKY = dict(plan="Basic", tenure_months=3, monthly_bill=210, data_gb=4.0, support_calls=4, late_payments=2)
LOYAL = dict(plan="Premium", tenure_months=48, monthly_bill=700, data_gb=20.0, support_calls=0, late_payments=0)


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_probability_is_between_0_and_1():
    p = client.post("/predict", json=RISKY).json()["churn_probability"]
    assert 0 <= p <= 1


def test_risky_customer_scores_higher_than_loyal():
    hi = client.post("/predict", json=RISKY).json()["churn_probability"]
    lo = client.post("/predict", json=LOYAL).json()["churn_probability"]
    assert hi > lo


def test_bad_plan_is_rejected():
    assert client.post("/predict", json=RISKY | {"plan": "Gold"}).status_code == 422
