def analyze_market_structure(candles, lookback=10):
    """
    Analyze basic market structure.

    candles = [
        {
            "high": 101.2,
            "low": 99.5,
            "close": 100.8
        }
    ]
    """

    if len(candles) < lookback + 2:
        return {
            "trend": "UNKNOWN",
            "signal": "WAIT",
            "last_high": 0.0,
            "last_low": 0.0
        }

    recent = candles[-lookback:]

    last_high = max(c["high"] for c in recent[:-1])
    last_low = min(c["low"] for c in recent[:-1])

    current = recent[-1]

    if current["high"] > last_high:
        trend = "BULLISH"
        signal = "BOS"

    elif current["low"] < last_low:
        trend = "BEARISH"
        signal = "CHOCH"

    else:
        trend = "RANGING"
        signal = "WAIT"

    return {
        "trend": trend,
        "signal": signal,
        "last_high": round(last_high, 4),
        "last_low": round(last_low, 4)
    }


if __name__ == "__main__":

    candles = []

    price = 100.0

    for i in range(20):
        candles.append({
            "high": price + 1,
            "low": price - 1,
            "close": price
        })
        price += 0.5

    result = analyze_market_structure(candles)

    print(result)
