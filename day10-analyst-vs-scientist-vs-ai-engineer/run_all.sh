#!/bin/bash
# Build the Sabari Mobile data, train the model, and run the API tests.
# Needs: pip install -r requirements.txt
set -e; cd "$(dirname "$0")"; PY=${PY:-python3}; mkdir -p data output
$PY make_data.py | tee output/run_make.txt
$PY train.py | tee output/run_train.txt
$PY -m pytest -q tests | tee output/run_tests.txt
