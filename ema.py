import pandas as pd


def calculate_ema(candles, period=20):
    """
    Calculate Exponential Moving Average (EMA)

    candles = [
        {"close": 100.5},
        {"close": 101.2},
        ...
    ]
    """

    if len(candles) < period:
        return None

    df = pd.DataFrame(candles)

    ema = df["close"].ewm(
        span=period,
        adjust=False
    ).mean()

    return round(float(ema.iloc[-1]), 4)


if __name__ == "__main__":

    candles = []

    price = 100

    for i in range(50):
        price += 0.5
        candles.append({"close": price})

    print("EMA 20:", calculate_ema(candles))
