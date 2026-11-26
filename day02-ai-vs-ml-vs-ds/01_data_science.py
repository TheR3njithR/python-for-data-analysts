"""STEP 1 - DATA SCIENCE: answer a business question with analysis. No model, no learning: just group, compare, explain.
Question from the owner: 'October sales went up, so why did profit not?'"""
import pandas as pd, os
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "outputs")
df = pd.read_csv(os.path.join(HERE, "data", "orders_aug_oct.csv"), parse_dates=["date"]); df["month"] = df.date.dt.strftime("%b")
L = []; P = lambda s="": L.append(s)
m = df.groupby("month", sort=False).agg(orders=("order_id", "size"), sales=("order_value", "sum"), profit=("profit", "sum"))
m["margin_%"] = (m.profit / m.sales * 100).round(1)
P("1. Month by month"); P(m.round(0).astype({"margin_%": float}).to_string()); P()
sep, oct_ = m.loc["Sep"], m.loc["Oct"]
P(f"   Oct vs Sep: sales {100 * (oct_.sales / sep.sales - 1):+.1f}%, profit {100 * (oct_.profit / sep.profit - 1):+.1f}% (Rs {oct_.profit - sep.profit:+,.0f})"); P()
c = df[df.month.isin(["Sep", "Oct"])].pivot_table(index="city", columns="month", values="profit", aggfunc="sum")[["Sep", "Oct"]]
c["change"] = c.Oct - c.Sep; P("2. Profit by city (Sep -> Oct)"); P(c.round(0).sort_values("change").to_string()); P()
dc = df[df.month.isin(["Sep", "Oct"])].pivot_table(index="city", columns="month", values="delivery_cost", aggfunc="mean")[["Sep", "Oct"]]
P("3. Average delivery cost per order (Rs)"); P(dc.round(1).to_string()); P()
f = df[df.coupon == "FIRST100"]; fm = f.groupby("month", sort=False).agg(uses=("order_id", "size"), coupon_cost=("discount", "sum"))
P("4. FIRST100 welcome coupon (Rs 100 off a first order)"); P(fm.to_string()); P()
fn = f[f.month.isin(["Sep", "Oct"])].assign(night=lambda x: (x.hour <= 3) | (x.hour >= 22))
nt = fn.pivot_table(index="city", columns="night", values="order_id", aggfunc="size", fill_value=0).rename(columns={False: "day", True: "night_10pm_4am"})
P("5. FIRST100 uses in Sep+Oct by city and time"); P(nt.to_string()); P()
acc = f.groupby("address_id").customer_id.nunique(); shared = acc[acc >= 5]
sh = f[f.address_id.isin(shared.index)]
P(f"6. Delivery addresses used by 5 or more different 'new' accounts with FIRST100: {len(shared)} addresses, "
  f"{sh.customer_id.nunique()} accounts, {len(sh)} orders, all in {', '.join(sorted(sh.city.unique()))}")
P(f"   first seen {sh.date.min().date()}; by month: " + ", ".join(f"{k} {v}" for k, v in sh.groupby('month', sort=False).size().items()))
P(f"   these orders: average Rs {sh.order_value.mean():.0f}, {100 * ((sh.hour >= 22) | (sh.hour <= 3)).mean():.0f}% placed 10pm-4am, "
  f"average profit per order Rs {sh.profit.mean():.0f} (all other orders: Rs {df[~df.order_id.isin(sh.order_id)].profit.mean():.0f})")
kochi = (dc.loc["Kochi", "Oct"] - dc.loc["Kochi", "Sep"]) * (df[(df.month == "Oct") & (df.city == "Kochi")].shape[0])
P(f"   Extra Kochi delivery cost in Oct: about Rs {kochi:,.0f}; October coupon cost on the shared addresses: Rs {sh[sh.month == 'Oct'].discount.sum():,.0f}")
P(); P("Conclusion (data science): sales grew but profit stood still for two reasons we can SEE in the data - a courier cost jump in Kochi and a burst of "
       "late-night welcome-coupon orders in Pune from a handful of addresses. Analysis explains the past; it does not watch new orders.")
open(os.path.join(OUT, "01_data_science.txt"), "w").write("\n".join(L) + "\n"); print("\n".join(L))
