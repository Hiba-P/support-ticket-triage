import pandas as pd
import numpy as np

HIGH_RISK_ISSUES = [
    "Attempts to collect debt not owed",
    "Took or threatened to take negative or legal action"
]

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Apply the same feature engineering used in training to new data."""
    df = df.copy()
    
    df["days_to_send"] = (df["Date sent to company"] - df["Date received"]).dt.days
    df["days_to_send_capped"] = df["days_to_send"].clip(upper=42)
    
    df["has_narrative"] = df["Consumer complaint narrative"].notna().astype(int)
    df["narrative_length"] = df["Consumer complaint narrative"].fillna("").str.len()
    
    df["high_risk_issue"] = df["Issue"].isin(HIGH_RISK_ISSUES).astype(int)
    df["received_month"] = df["Date received"].dt.month
    
    return df

STRUCTURED_FEATURE_COLS = [
    "Product", "Sub-product", "Issue", "high_risk_issue",
    "days_to_send_capped", "has_narrative", "received_month", "State"
]

STRUCTURED_CATEGORICAL_COLS = ["Product", "Sub-product", "Issue", "State"]
