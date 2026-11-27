#!/bin/bash
# Build the practice database, run every query, check them with pandas. Needs: pip install numpy pandas pytest (sqlite3 ships with Python)
set -e; cd "$(dirname "$0")"; PY=${PY:-python3}; mkdir -p data output
$PY make_db.py | tee output/run_make.txt; $PY run_queries.py | tee output/run_queries.txt; $PY -m pytest -q tests | tail -2 | tee output/run_tests.txt
