# SQL window functions for data analysts (SQLite)

Companion files for **[SQL Window Functions for Data Analysts: RANK, LAG and Running Totals Explained](https://youtu.be/g01NXJ1yiyg)** on **TheDataScientist | Renjith R** (Python for Data Analysts, Day 17).

Rank stores, compare each month with the one before, and keep a running total — in one line of SQL each. Every result is checked against pandas.

Synthetic data: Kaveri Mart is a made-up chain (8 stores, Jan–Jun 2026, 48 monthly rows, seed 1701). June has one deliberate tie so you can see RANK vs DENSE_RANK vs ROW_NUMBER. No real company, person or figure.

| File | Window function | Question |
|---|---|---|
| `sql/01_rank.sql` | RANK, DENSE_RANK, ROW_NUMBER | rank the stores in June |
| `sql/02_lag.sql` | LAG | change from last month |
| `sql/03_running_total.sql` | SUM OVER, AVG OVER ROWS | running total, 3-month average |
| `sql/04_best_month.sql` | ROW_NUMBER in a CTE | best month for every store |
| `src/make_data.py` | — | writes `data/kaveri.db` (seed 1701) |
| `tests/test_windows.py` | — | 5 pytest checks against pandas rank, diff and cumsum |
| `run_all.sh` | — | builds the database, runs every query, reruns the tests |

The SQLite database is not stored in the repo. `./run_all.sh` rebuilds it.

Works in SQLite, PostgreSQL, MySQL 8 and most data warehouses (the demo runs in SQLite via litecli).

## Run

```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
./run_all.sh                                           # or: PY=python3 ./run_all.sh
```
