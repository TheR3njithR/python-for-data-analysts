"""STEP 3 - AI: a system that takes a DECISION by itself, order by order, with no person in the loop.
Two versions run on the same 'live' orders (1-14 Nov 2026), one at a time, as they arrive:
  A) a hand-written rule  -> AI without machine learning (a person wrote the logic; nothing was learned)
  B) the same decision step driven by the Isolation Forest from step 2 -> AI powered by machine learning
Action: HOLD the welcome coupon for a quick human check, or APPROVE. The answer key is opened only to grade the result."""
import pandas as pd, os, pickle, time
import importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "outputs")
spec = importlib.util.spec_from_file_location("ml", os.path.join(HERE, "02_machine_learning.py")); ml = importlib.util.module_from_spec(spec); spec.loader.exec_module(ml)
M = pickle.load(open(os.path.join(OUT, "order_model.pkl"), "rb"))
def rule_bot(o):                        # A) written by a person, from the data-science finding
    return "HOLD" if o.coupon == "FIRST100" and (o.hour >= 22 or o.hour <= 3) else "APPROVE"
def ml_bot(o):                          # B) the model decides what is unusual
    s = -M["model"].score_samples(pd.DataFrame([o[M["features"]]]))[0]
    return "HOLD" if o.coupon == "FIRST100" and s > M["cut"] else "APPROVE"
live = ml.features(pd.read_csv(os.path.join(HERE, "data", "orders_nov_live.csv")))
truth = pd.read_csv(os.path.join(HERE, "_answer_key", "abuse_truth.csv"))
log = []; t0 = time.perf_counter()
for _, o in live.iterrows():            # one order at a time, like a live checkout
    log.append({"order_id": o.order_id, "date": o.date, "hour": o.hour, "city": o.city, "coupon": o.coupon, "order_value": o.order_value,
                "rule_bot": rule_bot(o), "ml_bot": ml_bot(o)})
secs = time.perf_counter() - t0
log = pd.DataFrame(log).merge(truth, on="order_id"); log.to_csv(os.path.join(OUT, "03_live_decisions.csv"), index=False)
L = [f"live orders 1-14 Nov 2026: {len(log):,} (FIRST100 coupon on {int((log.coupon == 'FIRST100').sum())}); planted abuse orders: {int(log.is_abuse.sum())}",
     f"both bots decided every order one by one in {secs:.1f} s ({secs / len(log) * 1000:.0f} ms per order)", ""]
for b, name in (("rule_bot", "A) rule-based AI (hand-written rule, no learning)"), ("ml_bot", "B) ML-powered AI (Isolation Forest decides)")):
    h = log[b] == "HOLD"; tp = int((h & log.is_abuse).sum()); fp = int((h & ~log.is_abuse).sum()); fn = int((~h & log.is_abuse).sum())
    L += [name, f"   held {int(h.sum())}: abuse caught {tp} of {tp + fn}, genuine customers held {fp}, abuse missed {fn}",
          f"   coupon money protected: Rs {tp * 100:,}   genuine new customers made to wait: {fp}", ""]
L += ["first FIRST100 orders as they arrived:", log[log.coupon == "FIRST100"].head(8).to_string(index=False)]
open(os.path.join(OUT, "03_ai_system.txt"), "w").write("\n".join(L) + "\n"); print("\n".join(L))
