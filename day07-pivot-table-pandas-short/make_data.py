"""Day 7 Short data (synthetic, seeded): 3,000 sales rows for a made-up shop, plus an Excel file whose 'Summary' sheet is a grid of
SUMIFS formulas (the same totals a pivot table shows). Usage: python make_data.py"""
import os, numpy as np, pandas as pd
from openpyxl import Workbook
H = os.path.dirname(os.path.abspath(__file__)); rng = np.random.default_rng(701)
regions = ["North", "South", "East", "West", "Central", "North-East"]; months = [f"2026-{m:02d}" for m in range(1, 11)]
n = 3000
df = pd.DataFrame({"order_id": [f"PV-{70001 + i}" for i in range(n)], "region": rng.choice(regions, n), "month": rng.choice(months, n),
                   "amount": np.round(rng.gamma(2.0, 1800, n), 0)})
df.to_csv(os.path.join(H, "data", "sales.csv"), index=False)
wb = Workbook(); ws = wb.active; ws.title = "Sales"; ws.append(list(df.columns))
for r in df.itertuples(index=False): ws.append(list(r))
sm = wb.create_sheet("Summary"); sm.append(["region"] + months)
for i, rg in enumerate(regions, start=2):
    sm.cell(i, 1, rg)
    for j, mo in enumerate(months, start=2):
        col = sm.cell(1, j).column_letter
        sm.cell(i, j, f'=SUMIFS(Sales!$D$2:$D${n + 1},Sales!$B$2:$B${n + 1},$A{i},Sales!$C$2:$C${n + 1},{col}$1)')
wb.save(os.path.join(H, "data", "sales_with_sumifs.xlsx"))
print(f"{n:,} rows, {len(regions)} regions, {len(months)} months, {len(regions) * len(months)} SUMIFS formulas")
