# Day 9 — Build a Sales Dashboard in Streamlit with Python (Interactive, No Tableau)

Companion files for **[Build a Sales Dashboard in Streamlit with Python (Interactive, No Tableau)](https://youtu.be/MIT8H0WpRnI)** on **TheDataScientist | Renjith R** (Python for Data Analysts, Day 9).

`make_data.py` builds a seeded sales file for a made-up shop, Godavari Traders: 9,000 orders, January to September 2026, 6 cities, 4 categories and 16 products. `app.py` is the 51-line Streamlit app from the video: sidebar filters, three KPI cards, a monthly line chart, a category bar chart, a top-5 products table and a CSV download. Five tests in `tests/test_app.py` run the real app headless with Streamlit's AppTest and check every card against plain pandas.

All data is synthetic. Godavari Traders, its customers and every rupee are made up. No real people, accounts or credentials.

| File | What it does |
|---|---|
| `make_data.py` | Writes `data/sales.csv` (seed 901) |
| `app.py` | The Streamlit dashboard from the video |
| `facts.py` | Recomputes every figure quoted in the narration (`output/facts.json`) |
| `tests/test_app.py` | 5 AppTest checks (each KPI vs pandas, plus the empty-filter guard) |
| `run_all.sh` | Builds the data, writes the facts file and runs the tests |
| `.streamlit/config.toml` | Headless local server settings used in the recording |
| `output/` | Facts JSON and run logs from the build used in the video |

The sales CSV is not stored in the repo. `./run_all.sh` rebuilds it.

## Run

```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
./run_all.sh                                           # or: PY=python3 ./run_all.sh
streamlit run app.py
```
