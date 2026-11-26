"""Monthly sales report: messy Excel export in, formatted Excel report out. Plain pandas + openpyxl.
  Step 1  clean   : find the header, tidy names, parse dates / money / percentages, drop junk, duplicates and other months
  Step 2  pivot   : region x product, weekly trend, sales reps, actual vs target, change vs last month
  Step 3  write   : formatted xlsx with KPI block, native Excel charts, number formats, frozen headers and filters
Usage: python monthly_report.py --month 2026-10 [--input input/Sales_Export_2026-10.xlsx] [--prev input/Sales_Export_2026-09.xlsx] [--out output/]"""
import argparse, os, re, time, datetime as dt
import pandas as pd
from openpyxl import load_workbook
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

COLS = {"invoice no": "invoice", "invoice date": "date", "customer": "customer", "region": "region", "sales rep": "rep",
        "product": "product", "qty": "qty", "unit price": "unit_price", "discount": "discount", "net amount": "net"}
REGION = {"north": "North", "n. zone": "North", "south": "South", "s. zone": "South",
          "east": "East", "e. zone": "East", "west": "West", "w. zone": "West"}

# ---------- Step 1: clean ----------
def to_number(v):
    if v is None or (isinstance(v, float) and pd.isna(v)): return None
    if isinstance(v, (int, float)): return float(v)
    s = re.sub(r"[₹,\s]", "", str(v)); return float(s) if s else None

def to_pct(v):
    if isinstance(v, str) and v.strip().endswith("%"): return float(v.strip()[:-1]) / 100
    return to_number(v)

def to_date(v):
    if isinstance(v, (dt.datetime, pd.Timestamp)): return pd.Timestamp(v).normalize()
    if isinstance(v, str):
        for f in ("%d/%m/%Y", "%Y-%m-%d"):
            try: return pd.Timestamp(dt.datetime.strptime(v.strip(), f))
            except ValueError: pass
    return pd.NaT

def load_export(path):
    raw = pd.read_excel(path, sheet_name="Export", header=None, dtype=object)
    hdr = raw.index[raw.iloc[:, 0].astype(str).str.strip().str.lower().eq("invoice no")][0]      # header is not on row 1
    df = raw.iloc[hdr + 1:].copy()
    df.columns = [COLS[str(c).strip().lower()] for c in raw.iloc[hdr]]
    targets = pd.read_excel(path, sheet_name="Targets").rename(columns={"Region": "region", "Target (INR)": "target"})
    return df, targets

def clean(df, month):
    log, issues = {}, []
    log["rows in export"] = len(df)
    df = df.dropna(how="all"); log["blank rows dropped"] = log["rows in export"] - len(df)
    is_line = df["invoice"].astype(str).str.match(r"^(INV|CN)-\d+$")
    log["total/footer rows dropped"] = int((~is_line).sum()); df = df[is_line].copy()
    df["date"] = df["date"].map(to_date)
    df["region"] = df["region"].map(lambda r: REGION.get(str(r).strip().lower()))
    df["rep"] = df["rep"].map(lambda r: " ".join(str(r).split()).title())
    for c in ("qty", "unit_price", "net"): df[c] = df[c].map(to_number)
    df["discount"] = df["discount"].map(to_pct)
    n = len(df); df = df.drop_duplicates(); log["exact duplicate rows dropped"] = n - len(df)
    other = df[df["date"].dt.strftime("%Y-%m") != month]
    issues.append(other.assign(issue=f"dated outside {month} (late entry)")); df = df.drop(other.index)
    bad = df[df[["date", "region", "qty", "unit_price", "net"]].isna().any(axis=1)]
    issues.append(bad.assign(issue="missing or unreadable value")); df = df.drop(bad.index)
    check = (df["qty"] * df["unit_price"] * (1 - df["discount"])).round(2)
    wrong = df[(check - df["net"]).abs() > 0.01]
    issues.append(wrong.assign(issue="net amount does not match qty x price x (1 - discount)")); df = df.drop(wrong.index)
    df["type"] = df["qty"].map(lambda q: "Return" if q < 0 else "Sale")
    monday = df["date"] - pd.to_timedelta(df["date"].dt.day_of_week, unit="D")                # week starting Monday,
    df["week"] = monday.where(monday >= pd.Timestamp(month + "-01"), pd.Timestamp(month + "-01")).dt.date   # first week starts on the 1st
    log["late entries moved to Issues"] = len(other); log["rows with missing values moved to Issues"] = len(bad)
    log["rows failing the net-amount check"] = len(wrong); log["clean lines"] = len(df)
    return df.sort_values(["date", "invoice"]).reset_index(drop=True), pd.concat(issues), log

# ---------- Step 2: pivot ----------
def summaries(df, targets, prev=None):
    pv_rp = pd.pivot_table(df, index="region", columns="product", values="net", aggfunc="sum", fill_value=0, margins=True, margins_name="Total")
    weekly = df.groupby("week").agg(lines=("invoice", "count"), net_revenue=("net", "sum")).reset_index()
    reps = (df.groupby(["rep", "region"]).agg(invoices=("invoice", "nunique"), units=("qty", "sum"), net_revenue=("net", "sum"))
              .reset_index().astype({"units": int}).sort_values("net_revenue", ascending=False))
    reg = df.groupby("region")["net"].sum().rename("actual").reset_index().merge(targets, on="region")
    reg["vs_target"] = reg["actual"] / reg["target"]
    if prev is not None:
        reg = reg.merge(prev.groupby("region")["net"].sum().rename("last_month").reset_index(), on="region")
        reg["change_vs_last_month"] = reg["actual"] / reg["last_month"] - 1
    sales, rets = df[df.type == "Sale"], df[df.type == "Return"]
    kpi = {"Net revenue": df["net"].sum(), "Invoices": sales["invoice"].nunique(), "Units sold": int(sales["qty"].sum()),
           "Average invoice": sales["net"].sum() / sales["invoice"].nunique(), "Returns": rets["net"].sum(),
           "Target achieved": reg["actual"].sum() / reg["target"].sum()}
    if prev is not None: kpi["Change vs last month"] = df["net"].sum() / prev["net"].sum() - 1
    return kpi, pv_rp, weekly, reps, reg

# ---------- Step 3: write ----------
HEAD = PatternFill("solid", fgColor="1F3A5F"); WHITE = Font(bold=True, color="FFFFFF"); BOLD = Font(bold=True)
INR = '"₹"#,##0'; PCT = "0.0%"; THIN = Border(bottom=Side(style="thin", color="BBBBBB"))

def style_header(ws, row=1):
    for c in ws[row]:
        if c.value is not None: c.fill, c.font, c.alignment = HEAD, WHITE, Alignment(horizontal="center", wrap_text=True)

def widths(ws, w=14):
    for i, col in enumerate(ws.iter_cols(min_row=1, max_row=min(ws.max_row, 60)), 1):
        n = max(len(str(c.value)) if c.value is not None else 0 for c in col)
        ws.column_dimensions[get_column_letter(i)].width = max(w, min(40, n + 3))

def write_report(path, month, df, issues, log, kpi, pv_rp, weekly, reps, reg):
    with pd.ExcelWriter(path, engine="openpyxl") as xw:
        pd.DataFrame({"x": []}).to_excel(xw, sheet_name="Summary", index=False)
        pv_rp.to_excel(xw, sheet_name="Region_x_Product")
        reg.to_excel(xw, sheet_name="Regions", index=False)
        weekly.to_excel(xw, sheet_name="Weekly", index=False)
        reps.to_excel(xw, sheet_name="Sales_Reps", index=False)
        df.drop(columns="week").to_excel(xw, sheet_name="Clean_Data", index=False)
        issues.drop(columns=[c for c in ("week", "type") if c in issues]).to_excel(xw, sheet_name="Issues", index=False)
        pd.DataFrame(list(log.items()), columns=["step", "rows"]).to_excel(xw, sheet_name="Cleaning_Log", index=False)
    wb = load_workbook(path)
    s = wb["Summary"]; s.delete_rows(1, s.max_row)
    s["A1"] = f"Monthly Sales Report - {pd.Timestamp(month + '-01'):%B %Y}"; s["A1"].font = Font(bold=True, size=18, color="1F3A5F")
    s["A2"] = "Monsoon Home Goods (synthetic demo data) - built by monthly_report.py"; s["A2"].font = Font(italic=True, color="666666")
    for i, (k, v) in enumerate(kpi.items()):
        r = 4 + i; s.cell(r, 1, k).font = BOLD; c = s.cell(r, 2, float(v) if not isinstance(v, int) else v)
        c.number_format = PCT if k in ("Target achieved", "Change vs last month") else INR if k not in ("Invoices", "Units sold") else "#,##0"
        s.cell(r, 1).border = s.cell(r, 2).border = THIN
    s.column_dimensions["A"].width = 26; s.column_dimensions["B"].width = 18
    rg = wb["Regions"]; style_header(rg); widths(rg)
    for row in rg.iter_rows(min_row=2):
        for c in row:
            h = rg.cell(1, c.column).value
            c.number_format = PCT if h in ("vs_target", "change_vs_last_month") else INR if h in ("actual", "target", "last_month") else c.number_format
    bar = BarChart(); bar.type = "col"; bar.title = "Net revenue vs target by region"; bar.y_axis.title = "INR"; bar.y_axis.numFmt = '#,##0'
    bar.add_data(Reference(rg, min_col=2, max_col=3, min_row=1, max_row=rg.max_row), titles_from_data=True)
    bar.set_categories(Reference(rg, min_col=1, min_row=2, max_row=rg.max_row)); bar.height, bar.width = 8, 16
    s.add_chart(bar, "D4")
    wk = wb["Weekly"]; style_header(wk); widths(wk)
    for row in wk.iter_rows(min_row=2): row[2].number_format = INR; row[0].number_format = "DD-MMM"
    line = LineChart(); line.title = "Net revenue by week"; line.y_axis.numFmt = '#,##0'
    line.add_data(Reference(wk, min_col=3, min_row=1, max_row=wk.max_row), titles_from_data=True)
    line.set_categories(Reference(wk, min_col=1, min_row=2, max_row=wk.max_row)); line.height, line.width = 8, 16
    line.series[0].smooth = False
    s.add_chart(line, "D21")
    p = wb["Region_x_Product"]; style_header(p); widths(p)
    for row in p.iter_rows(min_row=2, min_col=2):
        for c in row: c.number_format = INR
    for c in p[p.max_row]: c.font = BOLD
    for ws in wb.worksheets:                                   # print/PDF: landscape, one page wide
        ws.page_setup.orientation = "landscape"; ws.sheet_properties.pageSetUpPr.fitToPage = True
        ws.page_setup.fitToWidth, ws.page_setup.fitToHeight = 1, 0
    s.page_setup.fitToHeight = 1
    for name in ("Sales_Reps", "Clean_Data", "Issues", "Cleaning_Log"):
        ws = wb[name]; style_header(ws); widths(ws); ws.freeze_panes = "A2"
        for row in ws.iter_rows(min_row=2):
            for c in row:
                h = ws.cell(1, c.column).value
                if h in ("net", "unit_price", "net_revenue"): c.number_format = INR
                elif h == "discount": c.number_format = "0%"
                elif h == "date": c.number_format = "DD-MMM-YYYY"
    cd = wb["Clean_Data"]
    cd.add_table(Table(displayName="CleanData", ref=f"A1:{get_column_letter(cd.max_column)}{cd.max_row}",
                       tableStyleInfo=TableStyleInfo(name="TableStyleMedium2", showRowStripes=True)))
    wb["Issues"].auto_filter.ref = wb["Issues"].dimensions
    wb.save(path)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--month", required=True); ap.add_argument("--input"); ap.add_argument("--prev"); ap.add_argument("--out", default="output")
    a = ap.parse_args(); t0 = time.perf_counter()
    src = a.input or f"input/Sales_Export_{a.month}.xlsx"
    prev_month = (pd.Timestamp(a.month + "-01") - pd.DateOffset(months=1)).strftime("%Y-%m")
    prev_src = a.prev or f"input/Sales_Export_{prev_month}.xlsx"
    raw, targets = load_export(src); df, issues, log = clean(raw, a.month)
    prev = clean(load_export(prev_src)[0], prev_month)[0] if os.path.exists(prev_src) else None
    kpi, pv_rp, weekly, reps, reg = summaries(df, targets, prev)
    os.makedirs(a.out, exist_ok=True); out = os.path.join(a.out, f"Monthly_Report_{a.month}.xlsx")
    write_report(out, a.month, df, issues, log, kpi, pv_rp, weekly, reps, reg)
    print(f"== Monthly report {a.month}  ({src})")
    for k, v in log.items(): print(f"  {k:42s} {v}")
    print("== KPIs")
    for k, v in kpi.items(): print(f"  {k:42s} {v:.1%}" if k in ("Target achieved", "Change vs last month") else f"  {k:42s} {v:,.2f}" if isinstance(v, float) else f"  {k:42s} {v:,}")
    print("== Regions\n" + reg.to_string(index=False, float_format=lambda x: f"{x:,.3f}" if abs(x) < 5 else f"{x:,.0f}"))
    print("== Top 3 reps\n" + reps.head(3).to_string(index=False))
    print("== Weekly\n" + weekly.to_string(index=False))
    print(f"wrote {out} in {time.perf_counter() - t0:.2f} s")

if __name__ == "__main__":
    main()
