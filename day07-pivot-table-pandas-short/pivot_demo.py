"""The whole Short in code: one pandas pivot_table line vs Excel SUMIFS (recalculated by LibreOffice, headless)."""
import os, subprocess, shutil, tempfile, time, pandas as pd
H = os.path.dirname(os.path.abspath(__file__)); df = pd.read_csv(f"{H}/data/sales.csv")
t = time.perf_counter()
pivot = df.pivot_table(index="region", columns="month", values="amount", aggfunc="sum", margins=True, margins_name="Total")   # the one line
ms = (time.perf_counter() - t) * 1000
tmp = tempfile.mkdtemp(); shutil.copy(f"{H}/data/sales_with_sumifs.xlsx", tmp)
subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", f"{tmp}/out", f"{tmp}/sales_with_sumifs.xlsx"], check=True, capture_output=True)
xl = pd.read_excel(f"{tmp}/out/sales_with_sumifs.xlsx", sheet_name="Summary", index_col=0)
shutil.copy(f"{tmp}/out/sales_with_sumifs.xlsx", f"{H}/output/sales_with_sumifs_recalculated_by_libreoffice.xlsx")
core = pivot.drop(index="Total", columns="Total")
match = int((core.loc[xl.index, xl.columns].round(2).values == xl.round(2).values).sum())
ver = subprocess.run(["soffice", "--version"], capture_output=True, text=True).stdout.split()[1]
pivot.to_csv(f"{H}/output/pivot.csv")
L = [f"rows {len(df):,}, regions {df.region.nunique()}, months {df.month.nunique()}",
     "pandas: df.pivot_table(index='region', columns='month', values='amount', aggfunc='sum', margins=True)",
     f"  pivot shape with totals: {pivot.shape[0]} x {pivot.shape[1]}; took {ms:.1f} ms",
     f"Excel: {xl.size} SUMIFS formulas, recalculated by LibreOffice {ver}",
     f"  cells where SUMIFS == pandas: {match} of {xl.size}",
     f"  grand total: {pivot.loc['Total', 'Total']:,.0f}; largest region total: {pivot['Total'].drop('Total').idxmax()} {pivot['Total'].drop('Total').max():,.0f}"]
open(f"{H}/output/run_pivot_demo.txt", "w").write("\n".join(L) + "\n"); print("\n".join(L))
