import pandas as pd


def calculate_bollinger(candles, period=20, deviation=2):
    """
    Calculate Bollinger Bands
    """

    if len(candles) < period:
        return {
            "upper": 0.0,
            "middle": 0.0,
            "lower": 0.0
        }

    df = pd.DataFrame(candles)

    close = df["close"]

    middle = close.rolling(period).mean()
    std = close.rolling(period).std()

    upper = middle + (std * deviation)
    lower = middle - (std * deviation)

    return {
        "upper": round(float(upper.iloc[-1]), 4),
        "middle": round(float(middle.iloc[-1]), 4),
        "lower": round(float(lower.iloc[-1]), 4)
    }


if __name__ == "__main__":

    candles = []

    price = 100.0

    for i in range(50):
        candles.append({"close": price})
        price += 0.5

    result = calculate_bollinger(candles)

    print(result)
