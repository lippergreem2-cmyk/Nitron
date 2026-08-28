import pandas as pd


def calculate_macd(candles, fast=12, slow=26, signal=9):
    """
    Calculate MACD.

    candles = [
        {"close": 100.5},
        {"close": 101.0},
        ...
    ]
    """

    if len(candles) < slow:
        return {
            "macd": 0.0,
            "signal": 0.0,
            "histogram": 0.0
        }

    df = pd.DataFrame(candles)

    close = df["close"]

    ema_fast = close.ewm(span=fast, adjust=False).mean()
    ema_slow = close.ewm(span=slow, adjust=False).mean()

    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()

    histogram = macd_line - signal_line

    return {
        "macd": round(float(macd_line.iloc[-1]), 4),
        "signal": round(float(signal_line.iloc[-1]), 4),
        "histogram": round(float(histogram.iloc[-1]), 4)
    }


if __name__ == "__main__":
    candles = []

    price = 100.0

    for i in range(60):
        price += 0.5
        candles.append({"close": price})

    result = calculate_macd(candles)

    print(result)
