"""Make the messy Excel export for Day 4 (synthetic; seeded). 'Kaveri Electronics' is a made-up retailer; every customer is invented.
Planted problems (truth in _answer_key/ only):
  - order_date in THREE formats: real Excel dates, text 'DD/MM/YYYY', and Excel serial numbers stored as text (e.g. '46301')
  - 200 duplicate rows: 150 exact copies + 50 copies that differ only in case / extra spaces in customer name, email and city
  - missing values: blank cells plus fake blanks ('NA', 'n/a', '-', ' '), a 'landline' column that is almost all blank,
    some missing discounts (business rule: no discount = 0) and a few missing amounts (must be flagged, never guessed)"""
import numpy as np, pandas as pd, os, datetime as dt
rng = np.random.default_rng(401); H = os.path.dirname(os.path.abspath(__file__))
first = "Aarav Diya Kabir Meera Rohan Ananya Vihaan Isha Arjun Sara Kiran Nisha Dev Pooja Rahul Tara".split()
last = "Sharma Iyer Nair Reddy Gupta Menon Das Pillai Joshi Kulkarni Rao Bose".split()
cities = ["Kochi", "Chennai", "Bengaluru", "Hyderabad", "Pune", "Mumbai"]
products = {"LED TV 43in": 26990, "Mixer Grinder": 3499, "Air Fryer": 5999, "Smartwatch": 2799, "Bluetooth Speaker": 1899, "Ceiling Fan": 2650}
N = 2200; rows = []
for i in range(N):
    fn, ln = rng.choice(first), rng.choice(last); name = f"{fn} {ln}"
    email = f"{fn.lower()}.{ln.lower()}{rng.integers(1, 99)}@example.com"
    d = dt.date(2026, 10, 1) + dt.timedelta(days=int(rng.integers(0, 31)))
    p = rng.choice(list(products)); qty = int(rng.integers(1, 4))
    rows.append({"order_id": f"KE-{50001 + i}", "order_date": d, "customer": name, "email": email, "city": rng.choice(cities),
                 "product": p, "qty": qty, "amount": float(products[p] * qty),
                 "discount_pct": float(rng.choice([0, 5, 10, 15])), "landline": ""})
clean = pd.DataFrame(rows)
key = clean.copy()
m = clean.copy().astype(object)
# dates: 3 formats
fmt = rng.choice(["date", "dmy", "serial"], N, p=[0.55, 0.30, 0.15])
excel_epoch = dt.date(1899, 12, 30)
for i, f in enumerate(fmt):
    d = clean.at[i, "order_date"]
    if f == "dmy": m.at[i, "order_date"] = d.strftime("%d/%m/%Y")
    elif f == "serial": m.at[i, "order_date"] = str((d - excel_epoch).days)
# missing values
fake = ["NA", "n/a", "-", " ", ""]
city_blank = rng.choice(N, 140, replace=False); m.loc[city_blank, "city"] = rng.choice(fake, 140)
disc_blank = rng.choice(N, 90, replace=False); m.loc[disc_blank, "discount_pct"] = None
amt_blank = rng.choice(N, 7, replace=False); m.loc[amt_blank, "amount"] = None
ll = rng.choice(N, 22, replace=False); m.loc[ll, "landline"] = [f"0484 2{rng.integers(100000, 999999)}" for _ in ll]
# duplicates: 150 exact + 50 near
src = rng.choice(N, 200, replace=False); dups = m.loc[src].copy()
near = dups.index[:50]
dups.loc[near, "customer"] = ["  " + str(x).upper() + " " for x in dups.loc[near, "customer"]]
dups.loc[near, "email"] = [str(x).upper() for x in dups.loc[near, "email"]]
dups.loc[near, "city"] = [str(x).lower() + "  " for x in dups.loc[near, "city"]]
messy = pd.concat([m, dups]).sample(frac=1, random_state=4).reset_index(drop=True)
messy.to_excel(os.path.join(H, "input", "Kaveri_Orders_Oct2026.xlsx"), index=False, sheet_name="Orders")
key["order_date"] = pd.to_datetime(key.order_date); key.loc[disc_blank, "discount_pct"] = 0.0
key.loc[amt_blank, "amount"] = np.nan; key["city"] = key.city.where(~key.index.isin(city_blank), "Unknown")
key.to_csv(os.path.join(H, "_answer_key", "clean_truth.csv"), index=False)
open(os.path.join(H, "_answer_key", "planted.txt"), "w").write(
    f"rows: {N} real + 200 duplicates (150 exact, 50 case/space variants) = {len(messy)}\n"
    f"date formats: real dates {int((fmt == 'date').sum())}, DD/MM/YYYY text {int((fmt == 'dmy').sum())}, serial-as-text {int((fmt == 'serial').sum())}\n"
    f"city blanks or fake blanks: 140; discount blanks: 90 (rule: 0); amount blanks: 7 (flag); landline filled: 22 of {N}\n")
print(open(os.path.join(H, "_answer_key", "planted.txt")).read().strip())
