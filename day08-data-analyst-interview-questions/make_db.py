"""Build the synthetic Kaveri Mart practice data for Day 8 (interview questions). Everything is made up. Seed 801.
Writes data/kaveri_mart.db (SQLite: customers, products, orders) and data/orders_export.csv (a messy export of the same orders:
missing values and re-sent duplicate rows, for the pandas questions). Usage: python make_db.py"""
import os, sqlite3, numpy as np, pandas as pd
H = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(H, "data"); os.makedirs(D, exist_ok=True)
rng = np.random.default_rng(801)
first = ["Aarav", "Diya", "Kabir", "Meera", "Rohan", "Isha", "Vihaan", "Ananya", "Arjun", "Saanvi", "Karthik", "Lakshmi", "Nikhil", "Pooja", "Rahul", "Sneha", "Tanvi", "Varun", "Zoya", "Farhan"]
last = ["Iyer", "Nair", "Sharma", "Reddy", "Menon", "Gupta", "Das", "Pillai", "Kapoor", "Joshi", "Rao", "Shah", "Khan", "Bose", "Patel"]
cities = ["Bengaluru", "Chennai", "Delhi", "Hyderabad", "Kochi", "Mumbai", "Pune"]
N = 800
names = [f"{rng.choice(first)} {rng.choice(last)}" for _ in range(N)]
emails = [f"{n.split()[0].lower()}.{n.split()[1].lower()}{i}@example.com" for i, n in enumerate(names, 1)]
dup_src = rng.choice(np.arange(N - 40), 12, replace=False)                 # 12 people who signed up twice
dup_dst = np.arange(N - 12, N)
for s, d in zip(dup_src, dup_dst): names[d] = names[s]; emails[d] = emails[s]
cust = pd.DataFrame({"customer_id": np.arange(1, N + 1), "name": names, "email": emails, "city": rng.choice(cities, N, p=[.2, .14, .18, .14, .08, .16, .10]),
                     "signup_date": (pd.Timestamp("2025-01-01") + pd.to_timedelta(rng.integers(0, 500, N), unit="D")).strftime("%Y-%m-%d")})
cats = {"Electronics": [("Bluetooth Speaker", 2499), ("Smartwatch", 3999), ("Power Bank", 1299), ("Earbuds", 1899), ("Wi-Fi Router", 2199)],
        "Home": [("Pressure Cooker", 1899), ("Mixer Grinder", 3299), ("Bedsheet Set", 999), ("Water Bottle", 449), ("Steel Tiffin", 699)],
        "Grocery": [("Basmati Rice 5kg", 649), ("Toor Dal 1kg", 179), ("Filter Coffee 500g", 389), ("Ghee 1L", 659), ("Masala Box", 299)],
        "Personal Care": [("Face Wash", 249), ("Shampoo", 349), ("Hair Oil", 199), ("Sunscreen", 449), ("Trimmer", 1499)]}
prod = pd.DataFrame([(c, n, p) for c, items in cats.items() for n, p in items], columns=["category", "product_name", "unit_price"])
prod.insert(0, "product_id", np.arange(101, 101 + len(prod)))
M = 6000
odate = pd.Timestamp("2026-01-01") + pd.to_timedelta(rng.integers(0, 181, M), unit="D")      # Jan..Jun 2026
w = rng.gamma(1.2, 1.0, N); w /= w.sum()
orders = pd.DataFrame({"order_id": np.arange(50001, 50001 + M), "customer_id": rng.choice(cust.customer_id, M, p=w),
                       "product_id": rng.choice(prod.product_id, M), "qty": rng.choice([1, 1, 1, 2, 2, 3, 4], M), "order_date": odate})
orders = orders.sort_values(["order_date", "order_id"]).reset_index(drop=True); orders["order_id"] = np.arange(50001, 50001 + M)
orders["order_date"] = orders.order_date.dt.strftime("%Y-%m-%d")
orders["status"] = rng.choice(["Delivered", "Returned", "Cancelled"], M, p=[.86, .08, .06])
ghost = rng.choice(M, 9, replace=False); orders.loc[ghost, "customer_id"] = rng.integers(900, 990, 9)   # 9 orders from customer ids not in customers
con = sqlite3.connect(os.path.join(D, "kaveri_mart.db"))
for t, df in (("customers", cust), ("products", prod), ("orders", orders)): df.to_sql(t, con, index=False, if_exists="replace")
con.commit()
# messy export of the orders (pandas questions): 2 percent missing city, 1.5 percent missing qty, 40 rows re-sent later with a newer exported_at
ex = orders.merge(cust[["customer_id", "city"]], on="customer_id", how="left")
ex["exported_at"] = "2026-07-01 09:00"
ex.loc[rng.choice(M, 120, replace=False), "city"] = np.nan
ex["qty"] = ex.qty.astype("float"); ex.loc[rng.choice(M, 90, replace=False), "qty"] = np.nan
re_sent = ex.sample(40, random_state=801).copy(); re_sent["exported_at"] = "2026-07-02 09:00"
re_sent.loc[re_sent.index[:15], "status"] = "Returned"                    # 15 of the re-sent rows changed status
ex = pd.concat([ex, re_sent]).sort_values(["order_id", "exported_at"]).reset_index(drop=True)
ex.to_csv(os.path.join(D, "orders_export.csv"), index=False)
print(f"customers {len(cust):,} (12 duplicate emails planted), products {len(prod)}, orders {len(orders):,} ({orders.order_date.min()} to {orders.order_date.max()}), "
      f"9 orders with unknown customer ids; orders_export.csv {len(ex):,} rows")
