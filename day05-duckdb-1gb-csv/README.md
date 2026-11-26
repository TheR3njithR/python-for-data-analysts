# Day 5 — Query a 1 GB CSV in Seconds with SQL on Your Laptop (DuckDB, Free)

Companion files for **Query a 1 GB CSV in Seconds with SQL on Your Laptop (DuckDB, Free)** on **TheDataScientist | Renjith R** (Python for Data Analysts, Day 5).

You do not need a database server to use SQL on a big file. `make_big_csv.py` writes a seeded 16.5 million-row, 1.04 GB sales CSV for a made-up chain, Nilgiri Mart. `queries.py` runs four plain-SQL questions in DuckDB, capped at 4 threads and 2 GB of memory, then converts the file to Parquet. `pandas_check.py` recomputes the city totals in pandas chunks as a second check. Four tests confirm the answers.

All data is synthetic. Nilgiri Mart, its stores and every row are made up. No real people, accounts or credentials.

| File | What it does |
|---|---|
| `make_big_csv.py` | Writes `data/nilgiri_sales.csv` (seeded). `./run_all.sh` uses 16,500,000 rows, which matches the video. Calling the script with no argument defaults to 15,000,000 rows, so pass `16500000` if you run it directly |
| `queries.py` | Four SQL questions on the CSV, then `COPY` to Parquet and the same questions again. DuckDB is capped at 4 threads and 2 GB |
| `pandas_check.py` | Independent city-total check, reading the CSV in 1 million-row chunks |
| `tests/test_queries.py` | 4 pytest checks (row count, city totals, Parquet answers, Parquet file size) |
| `run_all.sh` | Builds the 16.5 million-row file, runs the queries, the pandas check and the tests |
| `output/` | Run logs and JSON from the build used in the video |

The 1.04 GB CSV and the 241 MB Parquet file are not stored in the repo. `./run_all.sh` rebuilds them. You need roughly 1.3 GB of free disk for both files. Building the CSV took about 46 seconds of work on the build machine; query times will differ on yours. Timings in the video are from one run with DuckDB capped at 4 threads and 2 GB of memory.

`gate.py` from the original demo folder is a box helper only and is not included. The scripts run fine without it.

## Run

```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
./run_all.sh                                           # or: PY=python3 ./run_all.sh
```

This uses 16,500,000 rows so the file matches the video. To try a smaller file first: `ROWS=500000 ./run_all.sh`.
