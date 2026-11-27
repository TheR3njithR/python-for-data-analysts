"""Clean the raw export with pandas, then load it into SQLite (data/kaveri.db)."""
import sqlite3, pandas as pd
o = pd.read_csv("data/orders.csv"); before = len(o)
o = o.drop_duplicates(); dups = before - len(o)
missing = int(o.unit_price.isna().sum()); o = o.dropna(subset=["unit_price"])
o["revenue"] = (o.qty * o.unit_price).round(2)
with sqlite3.connect("data/kaveri.db") as db:
    o.to_sql("orders", db, if_exists="replace", index=False)
    pd.read_csv("data/stores.csv").to_sql("stores", db, if_exists="replace", index=False)
print(f"removed {dups} duplicate lines and {missing} lines with no price")
print(f"loaded {len(o):,} clean lines into data/kaveri.db")
