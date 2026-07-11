from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import joblib
import pandas as pd
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from features import engineer_features, STRUCTURED_FEATURE_COLS, STRUCTURED_CATEGORICAL_COLS

app = FastAPI(title="Support Ticket Triage API")

model = joblib.load(os.path.join(os.path.dirname(__file__), "..", "data", "lgb_model_tuned.pkl"))

class Ticket(BaseModel):
    product: str
    sub_product: str
    issue: str
    state: str
    date_received: str
    date_sent_to_company: str
    has_narrative: bool

@app.get("/")
def root():
    return {"status": "ok", "message": "Support Ticket Triage API is running"}

@app.post("/predict")
def predict(ticket: Ticket):
    df = pd.DataFrame([{
        "Product": ticket.product,
        "Sub-product": ticket.sub_product,
        "Issue": ticket.issue,
        "State": ticket.state,
        "Date received": pd.to_datetime(ticket.date_received),
        "Date sent to company": pd.to_datetime(ticket.date_sent_to_company),
        "Consumer complaint narrative": "placeholder" if ticket.has_narrative else None,
    }])

    df = engineer_features(df)

    for col in STRUCTURED_CATEGORICAL_COLS:
        df[col] = df[col].astype("category")

    X = df[STRUCTURED_FEATURE_COLS]
    proba = model.predict_proba(X)[:, 1][0]

    return {
        "late_probability": float(proba),
        "risk_level": "high" if proba > 0.657 else "medium" if proba > 0.528 else "low"
    }
