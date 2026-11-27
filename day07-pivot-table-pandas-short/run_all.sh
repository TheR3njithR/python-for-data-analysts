#!/bin/bash
# Needs: pip install pandas numpy openpyxl; LibreOffice for the Excel check
set -e; cd "$(dirname "$0")"; PY=${PY:-python3}; mkdir -p data output
$PY make_data.py | tee output/run_make.txt; $PY pivot_demo.py
