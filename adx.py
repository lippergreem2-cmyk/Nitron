import pandas as pd


def calculate_adx(candles, period=14):
    """
    Calculate Average Directional Index (ADX)
    """

    if len(candles) < period + 1:
        return {
            "adx": 0.0,
            "plus_di": 0.0,
            "minus_di": 0.0
        }

    df = pd.DataFrame(candles)

    high = df["high"]
    low = df["low"]
    close = df["close"]

    up_move = high.diff()
    down_move = -low.diff()

    plus_dm = up_move.where((up_move > down_move) & (up_move > 0), 0.0)
    minus_dm = down_move.where((down_move > up_move) & (down_move > 0), 0.0)

    tr1 = high - low
    tr2 = (high - close.shift()).abs()
    tr3 = (low - close.shift()).abs()

    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

    atr = tr.rolling(period).mean()

    plus_di = 100 * (plus_dm.rolling(period).mean() / atr)
    minus_di = 100 * (minus_dm.rolling(period).mean() / atr)

    dx = (
        (plus_di - minus_di).abs()
        /
        (plus_di + minus_di)
    ) * 100

    adx = dx.rolling(period).mean()

    return {
        "adx": round(float(adx.iloc[-1]), 2),
        "plus_di": round(float(plus_di.iloc[-1]), 2),
        "minus_di": round(float(minus_di.iloc[-1]), 2)
    }


if __name__ == "__main__":

    candles = []

    price = 100.0

    for i in range(40):
        candles.append({
            "high": price + 1,
            "low": price - 1,
            "close": price
        })
        price += 0.5

    result = calculate_adx(candles)

    print(result)
