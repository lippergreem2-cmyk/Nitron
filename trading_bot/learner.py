import json
import os
import numpy as np

MODEL_FILE = "learner_state.json"
FEATURE_NAMES = ["ema_gap_pct", "rsi", "volatility_pct", "hour_of_day_norm"]
LEARNING_RATE = 0.05


class OnlineLearner:
    def __init__(self):
        self.n_features = len(FEATURE_NAMES)
        self.weights, self.bias = self._load()

    def _load(self):
        if os.path.exists(MODEL_FILE):
            with open(MODEL_FILE, "r") as f:
                state = json.load(f)
            return np.array(state["weights"]), state["bias"]
        return np.zeros(self.n_features), 0.0

    def _save(self):
        with open(MODEL_FILE, "w") as f:
            json.dump({"weights": self.weights.tolist(), "bias": self.bias}, f, indent=2)

    @staticmethod
    def _sigmoid(z):
        return 1 / (1 + np.exp(-z))

    def predict_confidence(self, features: dict) -> float:
        x = np.array([features[name] for name in FEATURE_NAMES])
        z = np.dot(self.weights, x) + self.bias
        return float(self._sigmoid(z))

    def learn(self, features: dict, won: bool):
        x = np.array([features[name] for name in FEATURE_NAMES])
        y = 1.0 if won else 0.0
        z = np.dot(self.weights, x) + self.bias
        pred = self._sigmoid(z)
        error = pred - y
        self.weights -= LEARNING_RATE * error * x
        self.bias -= LEARNING_RATE * error
        self._save()

    def feature_importance(self):
        return dict(sorted(
            zip(FEATURE_NAMES, self.weights.tolist()),
            key=lambda kv: abs(kv[1]),
            reverse=True,
        ))


def featurize(df, current_index=-1):
    row = df.iloc[current_index]
    ema_gap_pct = ((row["ema_fast"] - row["ema_slow"]) / row["close"]) * 100
    volatility_pct = ((df["high"].tail(14).max() - df["low"].tail(14).min())
                       / row["close"]) * 100
    hour_of_day_norm = row["timestamp"].hour / 24.0
    rsi = row.get("rsi", 50)
    return {
        "ema_gap_pct": float(ema_gap_pct),
        "rsi": float(rsi),
        "volatility_pct": float(volatility_pct),
        "hour_of_day_norm": float(hour_of_day_norm),
    }
