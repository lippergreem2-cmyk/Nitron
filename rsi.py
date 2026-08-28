import pandas as pd


def calculate_rsi(candles, period=14):
    """
    Calculate the Relative Strength Index (RSI).

    candles should be a list like:
    [
        {"close": 100.5},
        {"close": 101.2},
        ...
    ]
    """

    if len(candles) < period + 1:
        return 50.0

    df = pd.DataFrame(candles)

    delta = df["close"].diff()

    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    last_gain = avg_gain.iloc[-1]
    last_loss = avg_loss.iloc[-1]

    if pd.isna(last_gain) or pd.isna(last_loss):
        return 50.0

    if last_loss == 0:
        return 100.0

    rs = last_gain / last_loss
    rsi = 100 - (100 / (1 + rs))

    return round(float(rsi), 2)


if __name__ == "__main__":
    candles = []

    price = 100.0

    for i in range(30):
        price += 0.5
        candles.append({"close": price})

    print("RSI:", calculate_rsi(candles))
