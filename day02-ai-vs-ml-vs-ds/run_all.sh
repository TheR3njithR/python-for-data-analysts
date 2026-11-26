#!/bin/bash
# Reproduce every number in the Day 2 video. Needs Python 3.10+ with pandas, scikit-learn, matplotlib, pytest (requirements.txt).
set -e; cd "$(dirname "$0")"; PY=${PY:-python3}
$PY make_data.py | tee run_make_data.txt
$PY 01_data_science.py > /dev/null; $PY 02_machine_learning.py > /dev/null; $PY 03_ai_system.py > /dev/null; $PY 04_charts.py
$PY -m pytest -q tests 2>&1 | tail -2 | tee run_tests.txt
