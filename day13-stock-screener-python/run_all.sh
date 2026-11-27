#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
PY="${PY:-python3}"
mkdir -p data/bhav output
"$PY" src/make_data.py
"$PY" src/screener.py
"$PY" src/plot.py
"$PY" -m pytest -q tests
