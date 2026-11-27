#!/bin/bash
# Build the practice data, recompute the narrated figures, and run the AppTest checks.
# Needs: pip install numpy pandas streamlit pytest
set -e; cd "$(dirname "$0")"; PY=${PY:-python3}; mkdir -p data output
$PY make_data.py | tee output/run_make.txt
$PY facts.py > /dev/null
$PY -m pytest -q tests | tail -2 | tee output/run_tests.txt
