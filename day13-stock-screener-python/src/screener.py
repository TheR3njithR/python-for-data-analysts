"""Screen the clean table with four rules. The output is a shortlist to study, not a list to buy."""
from load_bhav import load

def screen(clean, min_ret=5, min_turnover=2500, min_deliv=40):
    g = clean.groupby("SYMBOL")
    clean = clean.assign(
        sma50=g.CLOSE_PRICE.transform(lambda s: s.rolling(50).mean()),
        ret20=g.CLOSE_PRICE.transform(lambda s: s.pct_change(20) * 100),
        turn20=g.TURNOVER_LACS.transform(lambda s: s.rolling(20).mean()),
        deliv20=g.DELIV_PER.transform(lambda s: s.rolling(20).mean()))
    last = clean[clean.DATE1 == clean.DATE1.max()].copy()
    last["trend"] = last.CLOSE_PRICE > last.sma50          # 1. close above its 50-day average
    last["momentum"] = last.ret20 > min_ret                # 2. up more than 5% in 20 sessions
    last["liquid"] = last.turn20 >= min_turnover           # 3. turnover >= 2,500 lakh a day
    last["delivery"] = last.deliv20 >= min_deliv           # 4. delivery >= 40% (NaN fails)
    last["passes"] = last[["trend", "momentum", "liquid", "delivery"]].all(axis=1)
    return last

if __name__ == "__main__":
    last = screen(load()[1])
    print(f"as of {last.DATE1.max():%d %b %Y}: {len(last)} symbols checked")
    for r in ["trend", "momentum", "liquid", "delivery", "passes"]:
        print(f"  {r:9s} {int(last[r].sum()):3d}")
    cols = ["SYMBOL", "CLOSE_PRICE", "sma50", "ret20", "turn20", "deliv20"]
    out = last[last.passes][cols].sort_values("ret20", ascending=False).round(1)
    out.to_csv("output/shortlist.csv", index=False); print(out.to_string(index=False))
