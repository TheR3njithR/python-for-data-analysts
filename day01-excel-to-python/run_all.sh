#!/bin/bash
# Reproduce every number in the video. Synthetic data only. Needs pandas, openpyxl and pytest (see requirements.txt).
set -e; cd "$(dirname "$0")"; P=${PYTHON:-python3}
$P make_messy_export.py                    | tee run_make_export.txt
$P monthly_report.py --month 2026-10       | tee run_report_2026-10.txt
$P monthly_report.py --month 2026-09       | tee run_report_2026-09.txt
$P -m pytest -q tests/ 2>&1                | tee run_tests.txt
$P fingerprint.py > DATA_FINGERPRINTS.txt
echo "ALL RUNS COMPLETE $(date -u '+%F %T UTC')"
