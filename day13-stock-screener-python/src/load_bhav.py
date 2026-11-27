"""Load every bhavcopy file into one clean table.
Strip the spaces, keep EQ rows, and trust DATE1 inside the file, not the file name."""
import glob, pandas as pd
FILES = "data/bhav/sec_bhavdata_full_*.csv"

def load():
    parts = []
    for f in sorted(glob.glob(FILES)):
        df = pd.read_csv(f, dtype=str, skipinitialspace=True)   # read as text first
        df.columns = df.columns.str.strip()
        parts.append(df.apply(lambda c: c.str.strip()))
    raw = pd.concat(parts)
    eq = raw[raw.SERIES == "EQ"].copy()                         # drop BE and other series
    eq["DATE1"] = pd.to_datetime(eq.DATE1, format="%d-%b-%Y")
    for c in eq.columns[3:]:
        eq[c] = pd.to_numeric(eq[c], errors="coerce")           # "-" becomes NaN
    clean = eq.drop_duplicates(["SYMBOL", "DATE1"])             # a repeated file adds nothing
    return raw, clean.sort_values(["SYMBOL", "DATE1"])

if __name__ == "__main__":
    raw, clean = load(); eq = raw[raw.SERIES == "EQ"]
    print(f"{len(raw):,} raw rows from {len(glob.glob(FILES))} files")
    print(f"dropped {len(raw) - len(eq)} non-EQ rows and {len(eq) - len(clean)} repeated rows")
    print(f"clean: {len(clean):,} rows, {clean.DATE1.nunique()} sessions, "
          f"{clean.SYMBOL.nunique()} symbols, {int(clean.DELIV_PER.isna().sum())} missing delivery")
