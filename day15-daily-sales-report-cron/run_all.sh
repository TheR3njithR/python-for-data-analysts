#!/bin/bash
# write the synthetic sales file and rerun the tests
set -e
mkdir -p data logs outbox reports
python src/make_data.py
python -m pytest -v --no-header -p no:cacheprovider
