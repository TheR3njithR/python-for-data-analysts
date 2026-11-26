"""The whole Short in code: pandas merge vs Excel VLOOKUP, on the same data.
Excel side: LibreOffice (headless) recalculates the 5,000 real VLOOKUP formulas; we read its computed values back and compare."""
import pandas as pd, os, subprocess, time, shutil, tempfile
H = os.path.dirname(os.path.abspath(__file__))
orders = pd.read_csv(f"{H}/data/orders.csv"); products = pd.read_csv(f"{H}/data/products.csv")
t0 = time.perf_counter()
merged = orders.merge(products, on="product_id", how="left", indicator=True)          # the one line
secs = time.perf_counter() - t0
missing = merged[merged["_merge"] == "left_only"]
tmp = tempfile.mkdtemp(); shutil.copy(f"{H}/data/orders_with_vlookup.xlsx", tmp)
subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", f"{tmp}/out", f"{tmp}/orders_with_vlookup.xlsx"],
               check=True, capture_output=True)
xl = pd.read_excel(f"{tmp}/out/orders_with_vlookup.xlsx", sheet_name="Orders")
shutil.copy(f"{tmp}/out/orders_with_vlookup.xlsx", f"{H}/output/orders_with_vlookup_recalculated_by_libreoffice.xlsx")
na = xl["unit_price"].isna() | xl["unit_price"].astype(str).str.contains("#N/A")
same = (pd.to_numeric(xl["unit_price"], errors="coerce").round(2).fillna(-1).values == merged["unit_price"].round(2).fillna(-1).values).sum()
L = [f"orders {len(orders):,}, products {len(products)}",
     "pandas: orders.merge(products, on='product_id', how='left', indicator=True)",
     f"  merged rows {len(merged):,} (row count unchanged: {len(merged) == len(orders)}), took {secs * 1000:.1f} ms",
     f"  orders with no matching product (_merge == 'left_only'): {len(missing)} -> {', '.join(missing.order_id.head(4))}, ...",
     f"Excel: 5,000 x =VLOOKUP(B2,Products!$A$2:$D$201,4,FALSE), recalculated by LibreOffice {subprocess.run(['soffice', '--version'], capture_output=True, text=True).stdout.split()[1]}",
     f"  #N/A results: {int(na.sum())}",
     f"  #N/A rows are exactly the merge left_only rows: {set(xl.order_id[na]) == set(missing.order_id)}",
     f"  rows where VLOOKUP price == merge price (both missing counted equal): {same:,} of {len(orders):,}"]
merged.drop(columns="_merge").to_csv(f"{H}/output/orders_merged.csv", index=False); missing.to_csv(f"{H}/output/orders_missing_product.csv", index=False)
open(f"{H}/output/run_merge_demo.txt", "w").write("\n".join(L) + "\n"); print("\n".join(L))
