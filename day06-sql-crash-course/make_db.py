"""Make the Day 6 practice database (synthetic, seeded): 'Ganga Retail' is a made-up Indian retailer; every customer is invented.
Writes data/ganga_retail.db (SQLite, ships with Python) with three tables: customers, products, orders. Usage: python make_db.py"""
import os, sqlite3, datetime as dt
import numpy as np
H = os.path.dirname(os.path.abspath(__file__)); DB = os.path.join(H, "data", "ganga_retail.db")
rng = np.random.default_rng(601)
cities = ["Kochi", "Chennai", "Bengaluru", "Hyderabad", "Pune", "Mumbai", "Delhi", "Jaipur"]
first = "Aarav Diya Kabir Meera Rohan Ananya Vihaan Isha Arjun Sara Kiran Nisha Dev Pooja Rahul Tara Neel Riya".split()
last = "Sharma Iyer Nair Reddy Gupta Menon Das Pillai Joshi Kulkarni Rao Bose Khan Singh".split()
cats = {"Grocery": (40, 600), "Snacks": (20, 250), "Beverages": (30, 400), "Personal Care": (80, 900), "Home": (150, 3500), "Electronics": (800, 45000)}
if os.path.exists(DB): os.remove(DB)
con = sqlite3.connect(DB); c = con.cursor()
c.executescript("""CREATE TABLE customers (customer_id INTEGER PRIMARY KEY, name TEXT, city TEXT, segment TEXT, joined DATE);
CREATE TABLE products (product_id INTEGER PRIMARY KEY, product_name TEXT, category TEXT, unit_price REAL);
CREATE TABLE orders (order_id INTEGER PRIMARY KEY, order_date DATE, customer_id INTEGER, product_id INTEGER, qty INTEGER, discount_pct REAL, status TEXT);""")
NC, NP, NO = 1200, 60, 9000
for i in range(1, NC + 1):
    c.execute("INSERT INTO customers VALUES (?,?,?,?,?)", (i, f"{rng.choice(first)} {rng.choice(last)}", str(rng.choice(cities)),
              str(rng.choice(["Retail", "Retail", "Retail", "Business"])), str(dt.date(2024, 1, 1) + dt.timedelta(days=int(rng.integers(0, 900))))))
names = {"Grocery": ["Basmati Rice 5kg", "Toor Dal 1kg", "Atta 10kg", "Sunflower Oil 1L", "Tea 500g", "Sugar 1kg", "Ghee 500ml", "Spice Mix", "Poha 1kg", "Jaggery 1kg"],
         "Snacks": ["Banana Chips", "Murukku", "Bhujia", "Biscuits", "Chikki", "Mixture", "Peanuts", "Khakhra", "Mathri", "Namkeen"],
         "Beverages": ["Filter Coffee", "Mango Drink", "Coconut Water", "Lassi", "Green Tea", "Juice 1L", "Soda", "Buttermilk", "Energy Drink", "Rose Milk"],
         "Personal Care": ["Shampoo", "Soap Pack", "Toothpaste", "Hair Oil", "Face Wash", "Deodorant", "Sunscreen", "Lotion", "Razor", "Talc"],
         "Home": ["Pressure Cooker", "Steel Tiffin", "Bedsheet", "Mop Set", "Water Bottle", "Kadai", "Tawa", "Storage Jar", "Curtains", "Iron Box"],
         "Electronics": ["Mixer Grinder", "Ceiling Fan", "LED Bulb Pack", "Smartwatch", "Earbuds", "Power Bank", "Air Fryer", "Kettle", "Trimmer", "Smart TV 43in"]}
ELEC = {"Mixer Grinder": 3499.0, "Ceiling Fan": 2650.0, "LED Bulb Pack": 499.0, "Smartwatch": 2799.0, "Earbuds": 1499.0, "Power Bank": 1299.0,
        "Air Fryer": 5999.0, "Kettle": 1199.0, "Trimmer": 1099.0, "Smart TV 43in": 26990.0}
pid = 0
for cat, (lo, hi) in cats.items():
    for nm in names[cat]:
        pid += 1; price = ELEC[nm] if cat == "Electronics" else float(round(rng.uniform(lo, hi), 0))
        c.execute("INSERT INTO products VALUES (?,?,?,?)", (pid, nm, cat, price))
active = rng.choice(np.arange(1, NC + 1), 1100, replace=False)          # 100 customers never order
for i in range(1, NO + 1):
    d = dt.date(2026, 1, 1) + dt.timedelta(days=int(rng.integers(0, 304)))  # Jan to Oct 2026
    c.execute("INSERT INTO orders VALUES (?,?,?,?,?,?,?)", (i, str(d), int(rng.choice(active)), int(rng.integers(1, NP + 1)), int(rng.integers(1, 5)),
              float(rng.choice([0, 0, 5, 10])), str(rng.choice(["Delivered"] * 17 + ["Returned", "Cancelled", "Cancelled"]))))
con.commit()
for t in ("customers", "products", "orders"): print(t, c.execute(f"SELECT count(*) FROM {t}").fetchone()[0], "rows")
con.close(); print("wrote", os.path.relpath(DB, H), os.path.getsize(DB), "bytes")
