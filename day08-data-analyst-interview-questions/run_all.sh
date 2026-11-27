#!/bin/bash
# Build the practice data, answer all 10 questions, check every answer. Needs: pip install numpy pandas pytest (sqlite3 ships with Python)
set -e; cd "$(dirname "$0")"; PY=${PY:-python3}; mkdir -p data output
$PY make_db.py | tee output/run_make.txt; $PY run_sql.py | tee output/run_sql.txt; $PY pandas_answers.py | tee output/run_pandas.txt; $PY -m pytest -q tests | tail -2 | tee output/run_tests.txt
