# Day 1 — Excel to Python: automate your monthly report

Companion files for **Automate Excel with Python: Your Monthly Report in One Command (Beginner)** on **TheDataScientist | Renjith R** (Python for Data Analysts, Day 1).

A messy monthly sales export goes in, and a formatted Excel report with two native charts comes out, built by one Python command.

All data is synthetic: "Monsoon Home Goods", its customers, sales reps and prices are invented. No real people, accounts or credentials.

| File | What it does |
|---|---|
| `make_messy_export.py` | Generates messy exports `input/Sales_Export_2026-09.xlsx` and `input/Sales_Export_2026-10.xlsx` + answer key (seeded) |
| `monthly_report.py` | Step 1 clean, step 2 pivot summaries, step 3 formatted xlsx with two native Excel charts → `output/Monthly_Report_<month>.xlsx` |
| `tests/test_monthly_report.py` | 7 pytest checks against the answer key, plus "the file really has 2 charts and 8 sheets" |
| `fingerprint.py` | Hashes every input cell value, to prove the data is the same on every run |
| `run_all.sh` | Runs everything and saves outputs as `run_*.txt` |

## Run

```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
./run_all.sh                                           # or: PYTHON=python3 ./run_all.sh
```

`./run_all.sh` writes the messy exports to `input/` and the finished reports to `output/`. The generator is seeded, so the data matches the video. The pre-built `.xlsx` workbooks are not stored in the repo; running the script rebuilds them in a third of a second.

Your own export: copy it into `input/` and edit the `COLS` and `REGION` dictionaries at the top of `monthly_report.py`.
