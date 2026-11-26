"""Clean a messy Excel export with pandas: dates, duplicates and missing values.
Usage: python clean_sales.py input/Kaveri_Orders_Oct2026.xlsx  ->  output/Kaveri_Orders_Oct2026_CLEAN.xlsx (+ printed report)"""
import sys, os, re, datetime as dt
import pandas as pd, numpy as np
FAKE_BLANKS = ["", " ", "NA", "N/A", "n/a", "na", "-", "--", "null", "None"]
EXCEL_EPOCH = pd.Timestamp("1899-12-30")
def date_kind(v):
    if isinstance(v, (dt.date, pd.Timestamp)): return "real Excel date"
    s = str(v).strip()
    if re.fullmatch(r"\d{2}/\d{2}/\d{4}", s): return "text DD/MM/YYYY"
    if re.fullmatch(r"\d{5}", s): return "serial number as text"
    return "other"
def fix_date(v):
    k = date_kind(v)
    if k == "real Excel date": return pd.Timestamp(v)
    if k == "text DD/MM/YYYY": return pd.to_datetime(str(v).strip(), format="%d/%m/%Y")
    if k == "serial number as text": return EXCEL_EPOCH + pd.Timedelta(days=int(str(v).strip()))
    return pd.NaT
def clean(path, log=print):
    raw = pd.read_excel(path, dtype=object)
    log(f"loaded {len(raw):,} rows x {raw.shape[1]} columns from {os.path.basename(path)}")
    # 1. dates
    kinds = raw.order_date.map(date_kind).value_counts()
    log("date formats found: " + ", ".join(f"{k} {v:,}" for k, v in kinds.items()))
    df = raw.copy(); df["order_date"] = df.order_date.map(fix_date)
    log(f"dates parsed: {df.order_date.notna().sum():,} of {len(df):,}; range {df.order_date.min().date()} to {df.order_date.max().date()}")
    # 2. missing values: fake blanks first
    fake_set = {b.strip().lower() for b in FAKE_BLANKS}
    df = df.replace({"": np.nan})
    for c in ["customer", "email", "city", "product"]:
        txt = df[c].astype("string").str.strip()
        is_fake = txt.str.lower().isin(fake_set) & df[c].notna()
        if c == "city": fake = int(is_fake.sum()); empty = int(df[c].isna().sum())
        df[c] = txt.mask(is_fake | (txt == ""), pd.NA)
    log(f"city: {empty} truly empty cells plus {fake} fake blanks ('NA', 'n/a', '-' or just spaces), now all real missing values")
    # 3. text normalisation (needed before duplicate check)
    df["customer"] = df.customer.str.split().str.join(" ").str.title()
    df["email"] = df.email.str.lower(); df["city"] = df.city.str.split().str.join(" ").str.title()
    # 4. duplicates
    exact = int(raw.astype(str).duplicated().sum())
    after = int(df.drop(columns=["landline"]).astype(str).duplicated().sum())
    log(f"duplicates: {exact} exact copies in the raw file; {after} once case and spaces are fixed")
    df = df[~df.drop(columns=["landline"]).astype(str).duplicated()].copy()
    # 5. missing values: decide column by column
    miss = (df.isna().mean() * 100).round(1)
    log("missing after de-duplication (%): " + ", ".join(f"{c} {v}" for c, v in miss.items() if v > 0))
    df = df.drop(columns=[c for c, v in miss.items() if v >= 95]); log("dropped columns >= 95% empty: " + ", ".join(c for c, v in miss.items() if v >= 95))
    n_disc = int(df.discount_pct.isna().sum()); df["discount_pct"] = df.discount_pct.fillna(0).astype(float)
    n_city = int(df.city.isna().sum()); df["city"] = df.city.fillna("Unknown")
    df["amount"] = pd.to_numeric(df.amount); df["qty"] = df.qty.astype(int)
    issues = df[df.amount.isna()].assign(issue="amount missing: check the invoice, do not guess")
    log(f"discount blanks set to 0 (business rule): {n_disc}; city blanks set to 'Unknown': {n_city}; rows with no amount flagged: {len(issues)}")
    df["net_amount"] = (df.amount * (1 - df.discount_pct / 100)).round(2)
    log(f"clean rows: {len(df):,}; net sales on rows with an amount: Rs {df.net_amount.sum():,.2f}")
    return df.sort_values("order_id").reset_index(drop=True), issues
if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "input", "Kaveri_Orders_Oct2026.xlsx")
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output", os.path.basename(src).replace(".xlsx", "_CLEAN.xlsx"))
    lines = []; log = lambda s: (lines.append(s), print(s))
    df, issues = clean(src, log)
    with pd.ExcelWriter(out) as xw:
        df.assign(order_date=df.order_date.dt.date).to_excel(xw, sheet_name="Clean", index=False)
        issues.assign(order_date=issues.order_date.dt.date).to_excel(xw, sheet_name="Issues", index=False)
        pd.DataFrame({"step": lines}).to_excel(xw, sheet_name="Report", index=False)
    log(f"wrote {out}")
