# Day 13 — Build a Stock Screener in Python with pandas (NSE Bhavcopy Format, Tested)

Companion files for **[Build a Stock Screener in Python with pandas (NSE Bhavcopy Format, Tested)](https://youtu.be/TsaijHDtLfI)** on **TheDataScientist | Renjith R** (Python for Data Analysts, Day 13).

Educational demo. Not financial advice. All symbols (DEMO...) and prices are synthetic.

`src/make_data.py` writes 66 end-of-day files in the layout of NSE's free `sec_bhavdata_full_DDMMYYYY.csv` (15 columns, a space after every comma, "-" when a delivery figure is missing). Sessions are business days from 1 Jul to 30 Sep 2026, except 14 Sep; the file named for 14 Sep repeats 11 Sep's rows. `src/load_bhav.py` strips the spaces, keeps only EQ rows, turns the dash into a missing value and drops repeated symbol-and-date rows. `src/screener.py` applies four rules and writes a shortlist. `src/plot.py` charts one shortlisted symbol against its 50-day average. Five tests in `tests/test_screener.py` guard the traps.

Rules (a shortlist to study, not a list to buy):
1. close above its 50-day average
2. up more than 5% over the last 20 sessions
3. average turnover at least 2,500 lakh rupees a day (20 sessions)
4. average delivery at least 40% (20 sessions); a missing figure fails

On 30 Sep 2026, 5 of 24 demo symbols pass all four. Findings in the video are from the seeded generator (seed 1301).

All data is synthetic. Every symbol starts with DEMO. No real company, price, account or credential.

| File | What it does |
|---|---|
| `src/make_data.py` | Writes the synthetic bhavcopy CSVs in `data/bhav/` (seed 1301) |
| `src/load_bhav.py` | Loads and cleans every file into one table |
| `src/screener.py` | Applies the four rules and writes `output/shortlist.csv` |
| `src/plot.py` | Charts one symbol vs its 50-day average (`output/DEMOAGRI17.png` by default) |
| `tests/test_screener.py` | 5 pytest checks |
| `run_all.sh` | Builds the data, runs the screener, draws the chart and runs the tests |
| `.gitignore` | Keeps generated data, output, caches and the virtualenv out of git |

The synthetic bhavcopy files, the shortlist CSV and the chart are not stored in the repo. `./run_all.sh` rebuilds them.

## Run

```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
./run_all.sh                                           # or: PY=python3 ./run_all.sh
```
