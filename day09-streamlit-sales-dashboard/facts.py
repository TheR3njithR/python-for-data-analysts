"""Every figure the Day 9 narration quotes, computed from data/sales.csv (same logic as app.py)."""
import json, pandas as pd
df = pd.read_csv("data/sales.csv", parse_dates=["order_date"]); df["month"] = df.order_date.dt.strftime("%Y-%m")
def kpi(v): return dict(revenue=int(v.revenue.sum()), revenue_lakh=f"{v.revenue.sum()/1e5:,.2f}", orders=len(v), aov=round(v.revenue.sum()/len(v)))
F = dict(rows=len(df), columns=list(df.columns[:9]), first=str(df.order_date.min().date()), last=str(df.order_date.max().date()),
         cities=sorted(df.city.unique()), categories=sorted(df.category.unique()), products=df["product"].nunique(),
         all=kpi(df), pune=kpi(df[df.city == "Pune"]), pune_online=kpi(df[(df.city == "Pune") & (df.channel == "Online")]),
         month=df.groupby("month").revenue.sum().to_dict(), category=df.groupby("category").revenue.sum().sort_values(ascending=False).to_dict(),
         top5=df.groupby("product").revenue.sum().nlargest(5).to_dict(),
         pune_online_month=df[(df.city == "Pune") & (df.channel == "Online")].groupby("month").revenue.sum().to_dict(),
         pune_online_top5=df[(df.city == "Pune") & (df.channel == "Online")].groupby("product").revenue.sum().nlargest(5).to_dict(),
         grocery_all=kpi(df[df.category=="Grocery"]))
json.dump(F, open("output/facts.json", "w"), indent=1, default=int); print(json.dumps(F, indent=1, default=int))
