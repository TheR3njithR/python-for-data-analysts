# Day 11 — Why Your Zerodha API Stops Working Every Morning (Access Token) #Shorts

Companion files for **[Why Your Zerodha API Stops Working Every Morning (Access Token) #Shorts](https://youtu.be/BZvfQH7RjEI)** on **TheDataScientist | Renjith R** (Zerodha API + Google Sheets Algo Trading Series, Day 11 Short).

`token_check.py` reads a saved login time from `session.json` and flags the access token as expired after the next 6 AM cutoff (Kite Connect docs). The session file is synthetic (`DEMO-NOT-A-REAL-TOKEN`). Three tests in `tests/test_expiry.py` check an evening login, a pre-6 AM login, and a login at exactly 6 AM.

All data is synthetic. No real token, API key, API secret or account. Not trading advice.

| File | What it does |
|---|---|
| `token_check.py` | Prints whether the saved token is still valid at a given time |
| `session.json` | Synthetic demo session (not a real token) |
| `tests/test_expiry.py` | 3 pytest checks for the 6 AM expiry rule |
| `run_all.sh` | Runs two demo checks from the video, then the tests |

## Run

```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
./run_all.sh                                           # or: PY=python3 ./run_all.sh
python token_check.py "2026-12-09 09:15"
```
