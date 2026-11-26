"""Synthetic data for the Day 3 Short: 5,000 orders and a 200-product price list for a made-up shop.
12 orders use product IDs that are NOT in the price list (discontinued codes), so the lookup has real misses. Seeded: same files every run."""
import numpy as np, pandas as pd, os
rng = np.random.default_rng(30); H = os.path.dirname(os.path.abspath(__file__))
cats = ["Snacks", "Spices", "Tea", "Rice", "Oil"]
products = pd.DataFrame({"product_id": [f"P{100 + i}" for i in range(200)],
                         "product_name": [f"{cats[i % 5]} item {i + 1:03d}" for i in range(200)],
                         "category": [cats[i % 5] for i in range(200)],
                         "unit_price": np.round(rng.uniform(20, 900, 200), 2)})
ids = rng.choice(products.product_id, 5000)
miss = rng.choice(5000, 12, replace=False); ids[miss] = [f"P{900 + k}" for k in range(12)]
orders = pd.DataFrame({"order_id": [f"O{10001 + i}" for i in range(5000)], "product_id": ids, "qty": rng.integers(1, 6, 5000)})
orders.to_csv(f"{H}/data/orders.csv", index=False); products.to_csv(f"{H}/data/products.csv", index=False)
with pd.ExcelWriter(f"{H}/data/orders_with_vlookup.xlsx") as xw:
    orders.to_excel(xw, sheet_name="Orders", index=False); products.to_excel(xw, sheet_name="Products", index=False)
import openpyxl
wb = openpyxl.load_workbook(f"{H}/data/orders_with_vlookup.xlsx"); ws = wb["Orders"]; ws["D1"] = "unit_price"
for r in range(2, 5002): ws[f"D{r}"] = f"=VLOOKUP(B{r},Products!$A$2:$D$201,4,FALSE)"
wb.save(f"{H}/data/orders_with_vlookup.xlsx")
print(f"orders: {len(orders):,}  products: {len(products)}  orders with unknown product_id: {len(miss)}  VLOOKUP formulas written: 5,000")
