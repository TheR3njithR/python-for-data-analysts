# Day 6 — SQL for Data Analysis: Beginner Crash Course on an Indian Sales Dataset (Part 1)

Companion files for **SQL for Data Analysis: Beginner Crash Course on an Indian Sales Dataset (Part 1)** on **TheDataScientist | Renjith R** (Python for Data Analysts, Day 6).

`make_db.py` builds a seeded SQLite database for a made-up shop, Ganga Retail: 1,200 customers, 60 products and 9,000 orders (January to October 2026). `queries.sql` has the five kinds of query analysts use most — WHERE, ORDER BY + LIMIT, GROUP BY, HAVING and JOIN — plus a LEFT JOIN that finds 100 customers who never ordered. `run_queries.py` runs them. Six tests in `tests/test_sql_vs_pandas.py` recompute every answer with pandas.

All data is synthetic. Ganga Retail, its customers and every rupee are made up. No real people, accounts or credentials.

| File | What it does |
|---|---|
| `make_db.py` | Writes `data/ganga_retail.db` (seeded SQLite) |
| `queries.sql` | The queries from the video |
| `run_queries.py` | Runs every query and writes `output/query_results.json` |
| `tests/test_sql_vs_pandas.py` | 6 pytest checks (each SQL answer vs pandas) |
| `run_all.sh` | Builds the database, runs the queries and the tests |
| `output/` | Run logs and JSON from the build used in the video |

The SQLite database is not stored in the repo. `./run_all.sh` rebuilds it. SQLite ships with Python.

## Run

```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
./run_all.sh                                           # or: PY=python3 ./run_all.sh
```
