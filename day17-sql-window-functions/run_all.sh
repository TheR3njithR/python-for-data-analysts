#!/bin/bash
# rebuild the data and run every query (SQLite via litecli), then the tests
set -e
python src/make_data.py
for f in sql/*.sql; do echo "== $f"; litecli data/kaveri.db -t -e "$(cat "$f")"; done
python -m pytest -q
