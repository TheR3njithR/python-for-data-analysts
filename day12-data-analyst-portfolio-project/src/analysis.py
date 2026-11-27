"""Run the three SQL questions from Python, save the answers and the chart for the README."""
import sqlite3, pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt

db = sqlite3.connect("data/kaveri.db")
def ask(f): return pd.read_sql(open(f"sql/{f}").read(), db)
city, month = ask("01_revenue_by_city.sql"), ask("02_monthly_revenue.sql")
rep = ask("03_repeat_customers.sql")
for name, df in [("revenue_by_city", city), ("monthly_revenue", month), ("repeat_customers", rep)]:
    df.to_csv(f"output/{name}.csv", index=False)

ax = month.plot(x="month", y="revenue_lakh", marker="o", legend=False, figsize=(9, 4.2))
ax.set_title("Kaveri Mart revenue by month, 2025 (synthetic data)")
ax.set_ylabel("Revenue (lakh rupees)"); ax.set_xlabel(""); ax.set_ylim(0, 35); ax.grid(alpha=0.3)
ax.set_xticks(range(12)); ax.set_xticklabels([m[5:] for m in month.month])
plt.tight_layout(); plt.savefig("output/monthly_revenue.png", dpi=110)

peak = month[month.revenue_lakh == month.revenue_lakh.max()]
print(f"top city: {city.city[0]} ({city.revenue_lakh[0]} lakh)")
print(f"peak: {', '.join(peak.month)} ({peak.revenue_lakh.iloc[0]} lakh each)")
print(f"repeat customers: {rep.repeat_pct_of_customers[0]}% of customers, "
      f"{rep.repeat_pct_of_revenue[0]}% of revenue")
print("saved output/*.csv and output/monthly_revenue.png")
