#!/bin/bash
# rebuild everything from scratch: data -> clean + load -> SQL + chart -> tests
set -e
python src/make_data.py && python src/clean_load.py && python src/analysis.py && python -m pytest -q
