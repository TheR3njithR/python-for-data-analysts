# Day 4 — Clean Messy Excel Data with pandas: Dates, Duplicates and Missing Values

Companion files for **Clean Messy Excel Data with pandas: Dates, Duplicates and Missing Values** on **TheDataScientist | Renjith R** (Python for Data Analysts, Day 4).

A messy October sales export from a made-up shop, Kaveri Electronics, has three date formats, 200 duplicate rows and a column that is 99% blank. The script cleans it in pandas, step by step, writes a Clean / Issues / Report workbook, and checks the result against an answer key with 7 tests.

All data is synthetic. Kaveri Electronics, its customers and every rupee are made up. Emails use example.com. No real people, accounts or credentials.

| File | What it does |
|---|---|
| `make_messy.py` | Builds the messy export `input/Kaveri_Orders_Oct2026.xlsx` from a clean answer key (seeded) |
| `clean_sales.py` | Parses dates format by format, cleans text, drops hidden duplicates, decides missing values column by column, writes `output/Kaveri_Orders_Oct2026_CLEAN.xlsx` |
| `traps.py` | Measures the three beginner traps on the same file (naive `to_datetime`, plain `drop_duplicates()`, plain `dropna()`) |
| `tests/test_clean.py` | 7 pytest checks against `_answer_key/clean_truth.csv` |
| `_answer_key/` | The planted truth (`clean_truth.csv`, `planted.txt`). Cleaning code does not read this until the tests run |
| `run_all.sh` | Rebuilds the messy file, cleans it, shows the traps and runs the tests |
| `output/` | Run logs from the build used in the video |

## Run

```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
./run_all.sh                                           # or: PY=python3 ./run_all.sh
```

The pre-built `.xlsx` workbooks are not stored in the repo (input export and the Clean / Issues / Report workbook). `./run_all.sh` rebuilds them. The generator is seeded, so the data matches the video.

The earlier Excel-to-Python walkthrough is Day 1: https://youtu.be/L3rOE91lP8o
