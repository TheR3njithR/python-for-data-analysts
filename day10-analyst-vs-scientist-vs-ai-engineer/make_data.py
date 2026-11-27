"""Sabari Mobile: a fully synthetic telecom customer table for Day 10 (seed 1001). No real company or person.
Writes data/customers.csv and data/sabari.db (SQLite, table customers)."""
import sqlite3
import numpy as np, pandas as pd
rng = np.random.default_rng(1001)
n = 6000
plan = rng.choice(["Basic", "Standard", "Premium"], n, p=[0.45, 0.35, 0.20])
city = rng.choice(["Bengaluru", "Chennai", "Hyderabad", "Kochi", "Mumbai", "Pune"], n)
tenure = rng.integers(1, 61, n)
bill = np.round(np.select([plan == "Basic", plan == "Standard"], [199, 399], 699) + rng.normal(0, 40, n)).astype(int)
data_gb = np.round(rng.gamma(2.0, 6.0, n) * np.select([plan == "Basic", plan == "Standard"], [0.7, 1.0], 1.5), 1)
calls = rng.poisson(1.2, n)
late = rng.poisson(0.4, n)
z = -1.2 - 0.045 * tenure + 0.55 * calls + 0.6 * late + np.select([plan == "Basic", plan == "Standard"], [0.5, 0.0], -0.4) - 0.01 * data_gb
churned = (rng.random(n) < 1 / (1 + np.exp(-z))).astype(int)
df = pd.DataFrame(dict(customer_id=[f"SM{50001 + i}" for i in range(n)], city=city, plan=plan, tenure_months=tenure, monthly_bill=bill,
                       data_gb=data_gb, support_calls=calls, late_payments=late, churned=churned))
df.to_csv("data/customers.csv", index=False)
with sqlite3.connect("data/sabari.db") as con:
    df.to_sql("customers", con, if_exists="replace", index=False)
print(f"wrote {len(df):,} customers; churn rate {df.churned.mean():.1%}")
