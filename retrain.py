"""
retrain.py
Reads closed trades logged by trade_logger.py, trains a model to predict
trade success probability from the indicator features, and saves it so
the live bot can score new setups before entering.

Usage:
    python retrain.py

Requires at least ~30-50 closed trades to produce a meaningful model.
Below that, it'll still run but the model won't be reliable -- treat early
runs as a pipeline test, not a real signal source.
"""

import json
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

from trade_logger import TradeLogger

MODEL_PATH = Path.home() / "Nitron" / "data" / "signal_model.joblib"
MIN_TRADES_TO_TRAIN = 30


def build_dataset() -> pd.DataFrame:
    logger = TradeLogger()
    trades = logger.get_closed_trades()

    if not trades:
        return pd.DataFrame()

    rows = []
    for t in trades:
        row = dict(t["features"])  # rsi, macd, adx, etc.
        row["outcome_win"] = 1 if t["outcome"] == "win" else 0
        rows.append(row)

    df = pd.DataFrame(rows)
    return df.dropna()  # drop rows with missing indicator values


def train(df: pd.DataFrame):
    feature_cols = [c for c in df.columns if c != "outcome_win"]
    X = df[feature_cols]
    y = df["outcome_win"]

    # order_block / liquidity_sweep may be bool -- convert to int for sklearn
    X = X.astype(float)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y if y.nunique() > 1 else None
    )

    model = GradientBoostingClassifier(
        n_estimators=100, max_depth=3, learning_rate=0.05, random_state=42
    )
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)

    print(f"\nTest accuracy: {acc:.3f}")
    print("\nClassification report:")
    print(classification_report(y_test, preds, zero_division=0))

    importances = dict(zip(feature_cols, model.feature_importances_))
    print("Feature importances:")
    for feat, imp in sorted(importances.items(), key=lambda x: -x[1]):
        print(f"  {feat}: {imp:.3f}")

    return model, feature_cols


def save_model(model, feature_cols):
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": model, "feature_cols": feature_cols}, MODEL_PATH)
    print(f"\nSaved model to {MODEL_PATH}")


def score_setup(features: dict) -> float:
    """
    Load the saved model and score a new setup's win probability.
    Use this at signal time, before deciding to enter a trade.
    """
    if not MODEL_PATH.exists():
        raise FileNotFoundError("No trained model yet -- run retrain.py first.")

    bundle = joblib.load(MODEL_PATH)
    model, feature_cols = bundle["model"], bundle["feature_cols"]

    row = pd.DataFrame([{c: features.get(c) for c in feature_cols}]).astype(float)
    prob_win = model.predict_proba(row)[0][1]
    return float(prob_win)


if __name__ == "__main__":
    df = build_dataset()

    if df.empty:
        print("No closed trades found yet -- nothing to train on.")
        print("Log some trades via trade_logger.py first, then rerun this.")
    elif len(df) < MIN_TRADES_TO_TRAIN:
        print(f"Only {len(df)} closed trades found (recommend >= {MIN_TRADES_TO_TRAIN}).")
        print("Training anyway as a pipeline test -- don't trust this model yet.\n")
        model, feature_cols = train(df)
        save_model(model, feature_cols)
    else:
        print(f"Training on {len(df)} closed trades...\n")
        model, feature_cols = train(df)
        save_model(model, feature_cols)
