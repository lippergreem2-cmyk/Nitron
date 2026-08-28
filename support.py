import pandas as pd


def find_support(candles, lookback=20):
    """
    Find the nearest support level.
    """

    if len(candles) < lookback:
        return 0.0

    df = pd.DataFrame(candles)

    recent = df.tail(lookback)

    support = recent["low"].min()

    return round(float(support), 4)


def is_near_support(price, support, tolerance=0.003):
    """
    Check if price is close to support.
    """

    return abs(price - support) <= (support * tolerance)


if __name__ == "__main__":

    candles = [
        {"high": 101, "low": 98, "close": 100},
        {"high": 102, "low": 99, "close": 101},
        {"high": 103, "low": 97, "close": 102},
        {"high": 104, "low": 100, "close": 103},
        {"high": 105, "low": 101, "close": 104},
        {"high": 106, "low": 102, "close": 105},
        {"high": 107, "low": 103, "close": 106},
        {"high": 108, "low": 104, "close": 107},
        {"high": 109, "low": 105, "close": 108},
        {"high": 110, "low": 106, "close": 109},
        {"high": 111, "low": 107, "close": 110},
        {"high": 112, "low": 108, "close": 111},
        {"high": 113, "low": 109, "close": 112},
        {"high": 114, "low": 110, "close": 113},
        {"high": 115, "low": 111, "close": 114},
        {"high": 116, "low": 112, "close": 115},
        {"high": 117, "low": 113, "close": 116},
        {"high": 118, "low": 114, "close": 117},
        {"high": 119, "low": 115, "close": 118},
        {"high": 120, "low": 116, "close": 119},
    ]

    current_price = candles[-1]["close"]

    support = find_support(candles)

    print("Support:", support)
    print("Current Price:", current_price)
    print("Near Support:", is_near_support(current_price, support))
