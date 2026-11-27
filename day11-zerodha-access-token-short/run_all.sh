#!/bin/bash
# Run the access-token expiry checks (synthetic session file, no real credentials).
set -e; cd "$(dirname "$0")"; PY=${PY:-python3}
$PY token_check.py "2026-12-08 23:00"
$PY token_check.py "2026-12-09 09:15"
$PY -m pytest -q tests
