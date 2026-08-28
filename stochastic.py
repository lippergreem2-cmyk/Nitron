import pandas as pd


def calculate_stochastic(candles, period=14, smooth=3):
    """
    Calculate Stochastic Oscillator

    candles = [
        {
            "high": 101.5,
            "low": 99.8,
            "close": 100.7
        }
    ]
    """

    if len(candles) < period:
        return {
            "k": 0.0,
            "d": 0.0
        }

    df = pd.DataFrame(candles)

    lowest_low = df["low"].rolling(period).min()
    highest_high = df["high"].rolling(period).max()

    k = (
        (df["close"] - lowest_low)
        /
        (highest_high - lowest_low)
    ) * 100

    d = k.rolling(smooth).mean()

    return {
        "k": round(float(k.iloc[-1]), 2),
        "d": round(float(d.iloc[-1]), 2)
    }


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

    result = calculate_stochastic(candles)

    print(result)
