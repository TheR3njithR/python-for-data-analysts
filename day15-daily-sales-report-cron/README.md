# Daily sales report in Python, sent at 8 AM with cron

Companion files for **Automate a Daily Sales Report in Python and Send It at 8 AM (cron + pandas)** on **TheDataScientist | Renjith R** (Python for Data Analysts, Day 15). The YouTube URL will be added to this README after the video is scheduled.

One script totals yesterday's sales by store, puts the same day last week next to it, emails the table with a CSV attached, and cron runs it at 8 AM. The mail server comes from the environment, never the code. Cron is started with almost no settings, so the crontab uses the full path to the project's Python and the code builds file paths from its own folder.

Synthetic data: Kaveri Mart is a made-up chain (8 stores, Sep–Oct 2026, 21,730 sales lines, seed 1501). Emails go to a local test inbox (`localhost:8025`), not the internet. Nothing in this folder is a real company, person, mailbox or password.

| File | What it does |
|---|---|
| `src/make_data.py` | Writes `data/sales.csv` (seed 1501) |
| `src/daily_report.py` | Builds the daily table, writes the CSV and sends the email |
| `src/mail_catcher.py` | Local test inbox on port 8025 |
| `cron/daily_report.cron` | The 8 AM crontab line from the video (for your own machine) |
| `tests/test_report.py` | 4 pytest checks: totals match the raw data, all eight stores appear, an empty day stops before sending, and the email carries the CSV |
| `run_all.sh` | Builds the sales file and runs the tests |

The sales CSV, cron log, outbox `.eml` files and report CSVs are not stored in the repo. `./run_all.sh` rebuilds the sales file. The tests swap in a fake mail server, so they never send anything and do not need the test inbox.

## Run

```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
./run_all.sh                                           # or: PY=python3 ./run_all.sh

# optional: see a real email land in the local test inbox
# python src/mail_catcher.py &
# python src/daily_report.py --date 2026-10-31

# on your own machine, to run every day at 8 AM in that machine's time zone:
# crontab cron/daily_report.cron
```

Never put a mail password in the code or the crontab; read it from the environment.
