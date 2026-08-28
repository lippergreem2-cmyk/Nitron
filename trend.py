import pandas as pd


def detect_trend(candles, fast=20, slow=50):
    """
    Detect market trend using moving averages.
    """

    if len(candles) < slow:
        return {
            "trend": "UNKNOWN",
            "ema_fast": 0.0,
            "ema_slow": 0.0,
            "strength": "LOW"
        }

    df = pd.DataFrame(candles)

    close = df["close"]

    ema_fast = close.ewm(span=fast, adjust=False).mean().iloc[-1]
    ema_slow = close.ewm(span=slow, adjust=False).mean().iloc[-1]

    current_price = close.iloc[-1]

    if current_price > ema_fast > ema_slow:
        trend = "UPTREND"

    elif current_price < ema_fast < ema_slow:
        trend = "DOWNTREND"

    else:
        trend = "SIDEWAYS"

    distance = abs(ema_fast - ema_slow)

    if distance > current_price * 0.01:
        strength = "HIGH"
    elif distance > current_price * 0.005:
        strength = "MEDIUM"
    else:
        strength = "LOW"

    return {
        "trend": trend,
        "ema_fast": round(float(ema_fast), 4),
        "ema_slow": round(float(ema_slow), 4),
        "strength": strength
    }


if __name__ == "__main__":

    candles = []

    price = 100.0

    for i in range(60):
        candles.append({
            "close": price
        })
        price += 0.5

    result = detect_trend(candles)

    print(result)
