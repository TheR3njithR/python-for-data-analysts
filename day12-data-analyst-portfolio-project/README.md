# Day 12 — Data Analyst Portfolio Project: SQL + Python End to End (Indian Retail Data, GitHub Ready)

Companion files for **[Data Analyst Portfolio Project: SQL + Python End to End (Indian Retail Data, GitHub Ready)](https://youtu.be/zAc1mGFbamE)** on **TheDataScientist | Renjith R** (Python for Data Analysts, Day 12).

`src/make_data.py` builds a seeded sales export for a made-up retail chain, Kaveri Mart: 8 stores in 6 cities, 19,448 sales lines (120 exact duplicates and 40 missing prices, like a real export). `src/clean_load.py` drops those rows, computes revenue and loads SQLite. Three SQL files answer one business question each. `src/analysis.py` reruns those queries from Python, saves the answers as CSVs and draws the monthly chart. Four tests in `tests/test_totals.py` check that no duplicates or missing prices remain, that the SQL total matches pandas, and that the city totals add up.

Findings from the video (synthetic data):
1. Bengaluru (75.3 lakh) and Chennai (72.2 lakh) lead, but they have two stores each. Per store, all six cities sit between 35.5 and 37.7 lakh.
2. October and November are the peak months (31.3 lakh each), about 50% above February.
3. Repeat customers are 66.1% of customers but bring 87.2% of revenue.

All data is synthetic. Kaveri Mart, its customers and every rupee are made up. No real company, person, account or credential.

| File | What it does |
|---|---|
| `src/make_data.py` | Writes `data/orders.csv` and `data/stores.csv` (seed 1201) |
| `src/clean_load.py` | Drops duplicates and missing prices, loads `data/kaveri.db` |
| `sql/01_revenue_by_city.sql` | Revenue by city, with a per-store column |
| `sql/02_monthly_revenue.sql` | Revenue by month |
| `sql/03_repeat_customers.sql` | Repeat vs one-time customers (SQL CTE) |
| `src/analysis.py` | Runs the three SQL files, writes CSVs and `output/monthly_revenue.png` |
| `tests/test_totals.py` | 4 pytest checks |
| `run_all.sh` | Builds the data, loads SQLite, draws the chart and runs the tests |
| `.gitignore` | Keeps the database, caches and virtualenv out of git |

The orders CSV, the stores CSV, the SQLite database and the output chart are not stored in the repo. `./run_all.sh` rebuilds them.

## Run

```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
./run_all.sh                                           # or: PY=python3 ./run_all.sh
```
