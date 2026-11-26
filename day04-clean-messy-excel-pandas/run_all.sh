#!/bin/bash
# Rebuild the messy file, clean it, show the traps and run the tests. Needs: pip install pandas openpyxl pytest
set -e; cd "$(dirname "$0")"; PY=${PY:-python3}
$PY make_messy.py; $PY clean_sales.py | tee output/run_clean.txt; $PY traps.py | tee output/run_traps.txt; $PY -m pytest -q tests | tail -2 | tee output/run_tests.txt
