"""Synthetic end-of-day files in the layout of NSE's free sec_bhavdata_full CSV (15 columns, a space after every comma,
"-" for a missing delivery figure). Every symbol is made up (DEMO...), every price is random. Sessions: Jul-Sep 2026."""
import numpy as np, pandas as pd
rng = np.random.default_rng(1301)
syms = ["DEMOAUTO1", "DEMOBANK2", "DEMOCEM3", "DEMOFMCG4", "DEMOIT5", "DEMOPHAR6", "DEMOPOWR7", "DEMOSTL8",
        "DEMOTEL9", "DEMOCHEM10", "DEMORETL11", "DEMOINFR12", "DEMOMETL13", "DEMOMEDI14", "DEMOTXTL15", "DEMOLOGI16",
        "DEMOAGRI17", "DEMOFIN18", "DEMOENGY19", "DEMOREAL20", "DEMOPAPR21", "DEMOGLAS22", "DEMOFOOD23", "DEMOTYRE24"]
days = [d for d in pd.bdate_range("2026-07-01", "2026-09-30") if d != pd.Timestamp("2026-09-14")]   # no session on 14 Sep in this demo
drift = rng.normal(0.0004, 0.0012, len(syms)); vol = rng.uniform(0.010, 0.025, len(syms))
price = rng.uniform(80, 2500, len(syms)); base_qty = rng.integers(20_000, 2_000_000, len(syms))
prev = price.copy(); frames = {}
for d in days:
    close = prev * np.exp(drift + vol * rng.standard_normal(len(syms)))
    op = prev * np.exp(vol / 3 * rng.standard_normal(len(syms)))
    hi = np.maximum(op, close) * (1 + rng.uniform(0, vol)); lo = np.minimum(op, close) * (1 - rng.uniform(0, vol))
    qty = (base_qty * rng.lognormal(0, 0.35, len(syms))).astype(int); avg = (op + close + hi + lo) / 4
    deliv = (qty * rng.uniform(0.2, 0.7, len(syms))).astype(int)
    df = pd.DataFrame({"SYMBOL": syms, "SERIES": "EQ", "DATE1": d.strftime("%d-%b-%Y"), "PREV_CLOSE": prev.round(2),
        "OPEN_PRICE": op.round(2), "HIGH_PRICE": hi.round(2), "LOW_PRICE": lo.round(2), "LAST_PRICE": (close * 1.0005).round(2),
        "CLOSE_PRICE": close.round(2), "AVG_PRICE": avg.round(2), "TTL_TRD_QNTY": qty, "TURNOVER_LACS": (qty * avg / 1e5).round(2),
        "NO_OF_TRADES": (qty / rng.uniform(40, 120, len(syms))).astype(int), "DELIV_QTY": deliv.astype(str),
        "DELIV_PER": (100 * deliv / qty).round(2).astype(str)})
    be = df.iloc[[3]].assign(SERIES="BE")                       # a trade-for-trade row, not a normal equity row
    df = pd.concat([df, be]); df.loc[df.index[5], ["DELIV_QTY", "DELIV_PER"]] = "-"   # a missing delivery figure
    frames[d] = df; prev = close
def write(df, d):
    lines = [", ".join(df.columns)] + [", ".join(map(str, r)) for r in df.itertuples(index=False)]
    open(f"data/bhav/sec_bhavdata_full_{d:%d%m%Y}.csv", "w").write("\n".join(lines) + "\n")
for d, df in frames.items(): write(df, d)
write(frames[pd.Timestamp("2026-09-11")], pd.Timestamp("2026-09-14"))   # file named for 14 Sep, holding 11 Sep's data
print(f"wrote {len(days) + 1} files ({len(days)} sessions + 1 repeated file), {len(syms)} made-up symbols")
