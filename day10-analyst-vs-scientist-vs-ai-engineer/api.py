"""AI engineer: put the model behind an API that an app can call."""
import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field

from train_features import FEATURES

app = FastAPI(title="Churn scorer")
model = joblib.load("output/churn_model.joblib")


class Customer(BaseModel):
    plan: str = Field(pattern="^(Basic|Standard|Premium)$")
    tenure_months: int = Field(ge=0)
    monthly_bill: float = Field(ge=0)
    data_gb: float = Field(ge=0)
    support_calls: int = Field(ge=0)
    late_payments: int = Field(ge=0)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(c: Customer):
    row = c.model_dump() | {"is_basic": int(c.plan == "Basic"), "is_premium": int(c.plan == "Premium")}
    prob = model.predict_proba(pd.DataFrame([row])[FEATURES])[0, 1]
    return {"churn_probability": round(float(prob), 3)}
