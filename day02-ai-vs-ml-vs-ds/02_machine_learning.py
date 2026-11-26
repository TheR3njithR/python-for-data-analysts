"""STEP 2 - MACHINE LEARNING: let a model LEARN what a normal order looks like, then score every order.
Isolation Forest (scikit-learn), unsupervised: it never sees the answer key. Trained on August + September, tested on October.
The answer key (_answer_key/abuse_truth.csv) is opened only afterwards, to grade the model."""
import pandas as pd, numpy as np, os, pickle
from sklearn.ensemble import IsolationForest
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "outputs")
FEATURES = ["order_value", "discount_pct", "account_age_days", "night_order", "items", "address_orders_30d"]
def features(df):
    df = df.copy(); df["discount_pct"] = (df.discount / df.order_value * 100).round(1)
    df["night_order"] = ((df.hour >= 22) | (df.hour <= 3)).astype(int); return df
if __name__ == "__main__":
    df = features(pd.read_csv(os.path.join(HERE, "data", "orders_aug_oct.csv"), parse_dates=["date"]))
    train, test = df[df.date < "2026-10-01"], df[df.date >= "2026-10-01"].copy()
    model = IsolationForest(n_estimators=300, random_state=42).fit(train[FEATURES])
    cut = float(np.quantile(-model.score_samples(train[FEATURES]), 0.99))      # flag anything stranger than 99% of training orders
    test["anomaly_score"] = -model.score_samples(test[FEATURES]); test["flag"] = test.anomaly_score > cut
    truth = pd.read_csv(os.path.join(HERE, "_answer_key", "abuse_truth.csv")); test = test.merge(truth, on="order_id")
    tp = int((test.flag & test.is_abuse).sum()); fp = int((test.flag & ~test.is_abuse).sum()); fn = int((~test.flag & test.is_abuse).sum())
    L = [f"trained on {len(train):,} orders (Aug-Sep), no labels; features: {', '.join(FEATURES)}",
         f"threshold = top 1% of training scores ({cut:.3f})",
         f"October: {len(test):,} orders scored, {int(test.flag.sum())} flagged as unusual",
         f"graded with the answer key: {tp} of {tp + fn} planted abuse orders caught (recall {tp / (tp + fn):.0%}), "
         f"{fp} genuine orders flagged (precision {tp / max(1, tp + fp):.0%}), {fn} missed", "",
         "five most unusual October orders:"]
    top = test.sort_values("anomaly_score", ascending=False).head(5)
    L += [top[["order_id", "date", "hour", "city", "order_value", "coupon", "account_age_days", "address_orders_30d", "anomaly_score", "is_abuse"]]
          .assign(date=lambda x: x.date.dt.date, anomaly_score=lambda x: x.anomaly_score.round(3)).to_string(index=False)]
    open(os.path.join(OUT, "02_machine_learning.txt"), "w").write("\n".join(L) + "\n"); print("\n".join(L))
    pickle.dump({"model": model, "cut": cut, "features": FEATURES}, open(os.path.join(OUT, "order_model.pkl"), "wb"))
