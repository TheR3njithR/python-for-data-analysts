"""Run every query in queries.sql against data/kaveri_mart.db and save the answers to output/sql_answers.json. Usage: python run_sql.py"""
import os, re, json, sqlite3
H = os.path.dirname(os.path.abspath(__file__)); con = sqlite3.connect(os.path.join(H, "data", "kaveri_mart.db"))
blocks = re.split(r"^-- name: (\w+)\n", open(os.path.join(H, "queries.sql")).read(), flags=re.M)[1:]
out = {}
for name, sql in zip(blocks[::2], blocks[1::2]):
    cur = con.execute(sql); rows = cur.fetchall(); out[name] = {"cols": [d[0] for d in cur.description], "rows": rows}
    print(f"\n== {name}\n" + " | ".join(out[name]["cols"])); [print(" | ".join(map(str, r))) for r in rows]
json.dump(out, open(os.path.join(H, "output", "sql_answers.json"), "w"), indent=1)
