#!/bin/bash
# Reproduce every number in the Day 3 Short. Needs Python 3.10+, pandas, openpyxl, and LibreOffice (for the Excel recalculation).
set -eo pipefail; cd "$(dirname "$0")"; PY=${PY:-python3}
$PY make_data.py | tee output/run_make_data.txt
$PY merge_demo.py
