# Day 8 — Data Analyst Interview Questions 2026: 10 SQL and Python Answers, Solved Live

Companion files for **[Data Analyst Interview Questions 2026: 10 SQL and Python Answers, Solved Live](https://youtu.be/ndBcqnpU7RM)** on **TheDataScientist | Renjith R** (Python for Data Analysts, Day 8).

`make_db.py` builds a seeded SQLite database and a messy CSV export for a made-up shop, Kaveri Mart: 800 customers (12 duplicate emails planted), 20 products and 6,000 orders (January to June 2026), plus 9 orders with unknown customer ids. The export has 6,040 rows, with missing city and quantity values and 40 re-sent rows. `queries.sql` has the five SQL interview questions. `pandas_answers.py` has the five pandas questions. Ten tests in `tests/test_answers.py` check every answer a second way.

All data is synthetic. Kaveri Mart, its customers and every rupee are made up. No real people, accounts or credentials.

| File | What it does |
|---|---|
| `make_db.py` | Writes `data/kaveri_mart.db` and `data/orders_export.csv` (seed 801) |
| `queries.sql` | The five SQL questions from the video (Q1–Q5) |
| `run_sql.py` | Runs every query and writes `output/sql_answers.json` |
| `pandas_answers.py` | The five pandas questions (Q6–Q10) |
| `questions.md` | Short list of the ten questions |
| `tests/test_answers.py` | 10 pytest checks (each answer vs an independent calculation) |
| `run_all.sh` | Builds the data, runs the SQL, the pandas answers and the tests |
| `output/` | Run logs and JSON from the build used in the video |

The SQLite database and the messy export are not stored in the repo. `./run_all.sh` rebuilds them. SQLite ships with Python.

## Run

```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
./run_all.sh                                           # or: PY=python3 ./run_all.sh
```
