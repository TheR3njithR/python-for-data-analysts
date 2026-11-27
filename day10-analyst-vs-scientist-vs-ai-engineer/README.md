# Day 10 — Data Analyst vs Data Scientist vs AI Engineer (India 2026): Skills, Tools and Which to Pick

Companion files for **[Data Analyst vs Data Scientist vs AI Engineer (India 2026): Skills, Tools and Which to Pick](https://youtu.be/7rBtZRWN5tU)** on **TheDataScientist | Renjith R** (Python for Data Analysts, Day 10).

`make_data.py` builds a seeded customer table for a made-up mobile company, Sabari Mobile: 6,000 customers, plan, tenure, bill, data use, support calls, late payments and churn (21.1%). The data analyst runs SQL on the SQLite copy. The data scientist trains a logistic regression with scikit-learn (AUC 0.782 on 1,500 test customers). The AI engineer serves the saved model behind a FastAPI `/predict` endpoint. Four tests in `tests/test_api.py` check health, a valid probability, that a risky customer scores higher than a loyal one, and that a bad plan is rejected.

All data is synthetic. Sabari Mobile, its customers and every figure are made up. No real company, person, account or credential. This is not career or salary advice; job titles vary by company, so read the job description.

| File | What it does |
|---|---|
| `make_data.py` | Writes `data/customers.csv` and `data/sabari.db` (seed 1001) |
| `analyst.sql` | The analyst queries from the video (churn by plan, churn by support calls) |
| `train.py` / `train_features.py` | Logistic regression, AUC and the riskiest-10% check; writes `output/churn_model.joblib` |
| `api.py` | FastAPI app (`/health`, `/predict`) from the video |
| `requests/*.json` | Sample payloads: risky, loyal, and a bad plan |
| `roles.md` | The three-role comparison table shown on screen |
| `tests/test_api.py` | 4 pytest checks |
| `run_all.sh` | Builds the data, trains the model and runs the tests |

The CSV, the SQLite database and the saved model are not stored in the repo. `./run_all.sh` rebuilds them.

## Run

```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
./run_all.sh                                           # or: PY=python3 ./run_all.sh
# optional: start the API, then try a request
# uvicorn api:app --port 8592
# curl -s localhost:8592/predict -H "Content-Type: application/json" -d @requests/risky.json
```
