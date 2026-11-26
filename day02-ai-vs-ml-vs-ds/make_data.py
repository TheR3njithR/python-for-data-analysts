"""Make the synthetic order data for 'Masala Mart', a made-up online grocery and snacks shop in four Indian cities.
Everything is invented and seeded (same file every run). Two problems are planted, and their truth is written ONLY to _answer_key/:
  1. a coupon-abuse ring: from mid-September, one group makes brand-new accounts to use the FIRST100 welcome coupon
     (Rs 100 off a first order of Rs 299 or more), mostly late at night, many accounts sharing a few delivery addresses (Pune);
  2. a courier change in Kochi on 1 Oct raises delivery cost per order from Rs 45 to Rs 72.
data/orders_aug_oct.csv = history (1 Aug - 31 Oct 2026); data/orders_nov_live.csv = 1-14 Nov 2026, used as 'new orders arriving'."""
import numpy as np, pandas as pd, os
rng = np.random.default_rng(29)
HERE = os.path.dirname(os.path.abspath(__file__))
CITIES = {"Pune": 0.32, "Jaipur": 0.24, "Kochi": 0.22, "Lucknow": 0.22}
DELIV = {"Pune": 40, "Jaipur": 38, "Kochi": 45, "Lucknow": 36}
days = pd.date_range("2026-08-01", "2026-11-14")
rows, cust_seq, addr_seq = [], 0, 0
regulars = {c: [] for c in CITIES}          # (customer_id, address_id, signup_day)
def new_id(prefix, n): return f"{prefix}{n:06d}"
for d in days:
    dn = (d - days[0]).days
    base = int(rng.normal(150 + dn * 0.25, 12))
    for _ in range(base):
        city = rng.choice(list(CITIES), p=list(CITIES.values()))
        is_new = rng.random() < 0.18 or len(regulars[city]) < 50
        if is_new:
            cust_seq += 1; addr_seq += 1; cid, aid, signup = new_id("C", cust_seq), new_id("A", addr_seq), d
            regulars[city].append((cid, aid, d))
        else:
            cid, aid, signup = regulars[city][rng.integers(len(regulars[city]))]
        hour = int(np.clip(rng.normal(15, 3.6), 7, 23))
        value = float(np.round(np.clip(rng.lognormal(6.35, 0.45), 120, 4500), 2))
        items = int(np.clip(round(value / rng.uniform(90, 160)), 1, 30))
        coupon, disc = "", 0.0
        if is_new and value >= 299 and rng.random() < 0.7: coupon, disc = "FIRST100", 100.0
        elif rng.random() < 0.08: coupon, disc = "FESTIVE10", round(value * 0.10, 2)
        dc = DELIV[city] + (27 if city == "Kochi" and d >= pd.Timestamp("2026-10-01") else 0) + rng.integers(-5, 6)
        refund = round(value * rng.uniform(0.2, 1.0), 2) if rng.random() < 0.03 else 0.0
        rows.append([d, hour, city, cid, aid, (d - signup).days, items, value, coupon, disc, float(dc), refund, False])
    # abuse ring: starts 15 Sep, grows; Pune; 6 shared drop addresses; new account per order
    if d >= pd.Timestamp("2026-09-15"):
        n_abuse = rng.poisson(2 + 0.12 * (d - pd.Timestamp("2026-09-15")).days)
        for _ in range(n_abuse):
            cust_seq += 1
            if rng.random() < 0.25: addr_seq += 1; ad = new_id("A", addr_seq)      # some orders go to a fresh address
            else: ad = f"R{rng.integers(1, 7):05d}"                                   # most go to one of 6 drop addresses
            hr = int(rng.choice([22, 23, 0, 1, 2, 3])) if rng.random() < 0.7 else int(rng.integers(17, 22))
            rows.append([d, hr, "Pune", new_id("C", cust_seq), ad, 0,
                         int(rng.integers(1, 3)), float(np.round(rng.uniform(299, 335), 2)), "FIRST100", 100.0,
                         float(DELIV["Pune"] + rng.integers(-5, 6)), 0.0, True])
df = pd.DataFrame(rows, columns=["date", "hour", "city", "customer_id", "address_id", "account_age_days", "items", "order_value",
                                 "coupon", "discount", "delivery_cost", "refund", "is_abuse"])
df = df.sample(frac=1, random_state=7).sort_values(["date", "hour"], kind="stable").reset_index(drop=True)
df.insert(0, "order_id", [f"MM{100001 + i}" for i in range(len(df))])
df["cost_of_goods"] = (df.order_value * 0.74).round(2)
df["profit"] = (df.order_value - df.discount - df.cost_of_goods - df.delivery_cost - df.refund).round(2)
# each address's number of orders in the previous 30 days (a normal feature any shop database can compute)
df["address_orders_30d"] = 0
for aid, g in df.groupby("address_id"):
    t = g.date.values; df.loc[g.index, "address_orders_30d"] = [int(((t > x - np.timedelta64(30, "D")) & (t <= x)).sum()) for x in t]
df.address_id = df.address_id.str.replace("R", "A9")  # ring addresses look like any other address in the shared data
key = df[["order_id", "is_abuse"]]; key.to_csv(os.path.join(HERE, "_answer_key", "abuse_truth.csv"), index=False)
open(os.path.join(HERE, "_answer_key", "planted.txt"), "w").write(
    "Planted problem 1: coupon-abuse ring from 2026-09-15, Pune, new account every order, FIRST100, Rs 299-335, mostly 22:00-03:59 (30% at 17:00-21:59), 6 shared drop addresses (25% of orders to a fresh address).\n"
    "Planted problem 2: Kochi courier change 2026-10-01, delivery cost Rs 45 -> Rs 72 per order (+/- 5).\n")
pub = df.drop(columns=["is_abuse"]); pub.date = pub.date.dt.date
live = pub.date >= pd.Timestamp("2026-11-01").date()
pub[~live].to_csv(os.path.join(HERE, "data", "orders_aug_oct.csv"), index=False); pub[live].to_csv(os.path.join(HERE, "data", "orders_nov_live.csv"), index=False)
print(f"history: {int((~live).sum())} orders (1 Aug - 31 Oct 2026); live: {int(live.sum())} orders (1-14 Nov 2026); "
      f"planted abuse orders: {int(df.is_abuse[~live].sum())} in history, {int(df.is_abuse[live].sum())} in live")
