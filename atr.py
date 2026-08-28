import pandas as pd


def calculate_atr(candles, period=14):
    """
    Calculate Average True Range (ATR)

    candles = [
        {
            "high": 101.5,
            "low": 99.8,
            "close": 100.7
        }
    ]
    """

    if len(candles) < period + 1:
        return 0.0

    df = pd.DataFrame(candles)

    high = df["high"]
    low = df["low"]
    close = df["close"]

    tr1 = high - low
    tr2 = (high - close.shift()).abs()
    tr3 = (low - close.shift()).abs()

    true_range = pd.concat(
        [tr1, tr2, tr3],
        axis=1
    ).max(axis=1)

    atr = true_range.rolling(period).mean()

    return round(float(atr.iloc[-1]), 4)


if __name__ == "__main__":

    candles = []

    price = 100.0

    for i in range(30):
        candles.append({
            "high": price + 1,
            "low": price - 1,
            "close": price
        })
        price += 0.5

    print("ATR:", calculate_atr(candles))
