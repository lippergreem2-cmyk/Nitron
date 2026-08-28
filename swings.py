# swings.py

def f(x):
    return float(x)


def swing_highs(candles, lookback=3):

    highs = []

    if len(candles) < lookback * 2 + 1:
        return highs

    for i in range(lookback, len(candles) - lookback):

        current = f(candles[i]["high"])

        left = max(f(c["high"]) for c in candles[i-lookback:i])
        right = max(f(c["high"]) for c in candles[i+1:i+lookback+1])

        if current > left and current > right:

            highs.append({
                "index": i,
                "price": current
            })

    return highs


def swing_lows(candles, lookback=3):

    lows = []

    if len(candles) < lookback * 2 + 1:
        return lows

    for i in range(lookback, len(candles) - lookback):

        current = f(candles[i]["low"])

        left = min(f(c["low"]) for c in candles[i-lookback:i])
        right = min(f(c["low"]) for c in candles[i+1:i+lookback+1])

        if current < left and current < right:

            lows.append({
                "index": i,
                "price": current
            })

    return lows


def latest_swing_high(candles):

    highs = swing_highs(candles)

    if highs:
        return highs[-1]

    return None


def latest_swing_low(candles):

    lows = swing_lows(candles)

    if lows:
        return lows[-1]

    return None


if __name__ == "__main__":

    from mt5_data import get_candles

    candles = get_candles("XAUUSD")

    print("Swing Highs")
    print(swing_highs(candles)[-5:])

    print()

    print("Swing Lows")
    print(swing_lows(candles)[-5:])
