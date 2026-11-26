#!/bin/bash
# Make the ~1 GB CSV, query it with DuckDB, check the totals with pandas, run the tests. Needs: pip install duckdb pandas pytest
set -e; cd "$(dirname "$0")"; PY=${PY:-python3}; mkdir -p data output
$PY make_big_csv.py ${ROWS:-16500000} | tee output/run_make.txt; $PY queries.py | tee output/run_queries.txt
$PY pandas_check.py | tee output/run_pandas.txt; $PY -m pytest -q tests | tail -2 | tee output/run_tests.txt
