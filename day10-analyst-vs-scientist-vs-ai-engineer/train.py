"""Data scientist: which customers are likely to leave next?"""
import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split

from train_features import FEATURES

def prepare(df):
    return df.assign(is_basic=(df.plan == "Basic").astype(int), is_premium=(df.plan == "Premium").astype(int))[FEATURES]

df = pd.read_csv("data/customers.csv")
X, y = prepare(df), df["churned"]
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, random_state=7, stratify=y)
model = LogisticRegression(max_iter=1000).fit(X_tr, y_tr)

p = model.predict_proba(X_te)[:, 1]
top = pd.Series(p).rank(ascending=False) <= len(p) * 0.1
print(f"test customers: {len(y_te)}, AUC: {roc_auc_score(y_te, p):.3f}")
print(f"churn in the riskiest 10%: {y_te[top.values].mean():.1%} (overall {y_te.mean():.1%})")
joblib.dump(model, "output/churn_model.joblib")
print("saved output/churn_model.joblib")
