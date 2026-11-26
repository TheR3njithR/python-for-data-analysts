"""Charts used in the video, drawn from the real outputs (matplotlib)."""
import pandas as pd, os, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "outputs"); os.makedirs(os.path.join(OUT, "charts"), exist_ok=True)
plt.rcParams.update({"figure.facecolor": "#0a1222", "axes.facecolor": "#0a1222", "axes.edgecolor": "#8da2c0", "text.color": "#e6edf7",
                     "axes.labelcolor": "#e6edf7", "xtick.color": "#e6edf7", "ytick.color": "#e6edf7", "font.size": 15})
df = pd.read_csv(os.path.join(HERE, "data", "orders_aug_oct.csv"), parse_dates=["date"]); df["month"] = df.date.dt.strftime("%b")
m = df.groupby("month", sort=False)[["order_value", "profit"]].sum() / 1e5
fig, ax = plt.subplots(figsize=(12, 6)); x = range(len(m))
ax.bar([i - 0.2 for i in x], m.order_value, 0.4, label="sales (Rs lakh)", color="#38bdf8"); ax.bar([i + 0.2 for i in x], m.profit, 0.4, label="profit (Rs lakh)", color="#4ade80")
for i, (s, p) in enumerate(zip(m.order_value, m.profit)): ax.text(i - 0.2, s + 0.3, f"{s:.1f}", ha="center"); ax.text(i + 0.2, p + 0.3, f"{p:.2f}", ha="center")
ax.set_xticks(list(x), m.index); ax.set_ylim(0, m.order_value.max() * 1.25); ax.legend(frameon=False, loc="upper left", ncol=2); ax.set_title("Masala Mart (synthetic): sales up 9%, profit up 2%"); [ax.spines[k].set_visible(False) for k in ("top", "right")]
fig.tight_layout(); fig.savefig(os.path.join(OUT, "charts", "sales_vs_profit.png"), dpi=120); plt.close(fig)
d = df[df.month.isin(["Aug", "Sep", "Oct"])].pivot_table(index="month", columns="city", values="delivery_cost", aggfunc="mean").loc[["Aug", "Sep", "Oct"]]
fig, ax = plt.subplots(figsize=(12, 6)); d.plot(ax=ax, marker="o", lw=3); ax.set_ylabel("avg delivery cost per order (Rs)"); ax.set_xlabel("")
ax.set_title("Delivery cost per order by city"); ax.legend(frameon=False); [ax.spines[k].set_visible(False) for k in ("top", "right")]
fig.tight_layout(); fig.savefig(os.path.join(OUT, "charts", "delivery_cost.png"), dpi=120); plt.close(fig)
f = df[(df.coupon == "FIRST100") & (df.city == "Pune")]; f = f.assign(wk=f.date.dt.to_period("W").dt.start_time, night=(f.hour >= 22) | (f.hour <= 3))
w = f.pivot_table(index="wk", columns="night", values="order_id", aggfunc="size", fill_value=0).rename(columns={False: "daytime", True: "10pm-4am"})
fig, ax = plt.subplots(figsize=(12, 6)); w.plot(ax=ax, lw=3, color=["#38bdf8", "#f87171"]); ax.set_ylabel("FIRST100 orders per week, Pune"); ax.set_xlabel("")
ax.set_title("Welcome-coupon orders in Pune, by time of day"); ax.legend(frameon=False); [ax.spines[k].set_visible(False) for k in ("top", "right")]
fig.tight_layout(); fig.savefig(os.path.join(OUT, "charts", "pune_coupon_nights.png"), dpi=120); plt.close(fig)
print("charts -> outputs/charts/ (sales_vs_profit, delivery_cost, pune_coupon_nights)")
