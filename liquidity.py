def detect_liquidity_sweep(candles, lookback=20):
    """
    Detect simple liquidity sweeps.

    candles = [
        {
            "high": 101.5,
            "low": 99.8,
            "close": 100.7
        }
    ]
    """

    if len(candles) < lookback + 1:
        return {
            "type": "NONE",
            "level": 0.0,
            "signal": "WAIT"
        }

    recent = candles[-(lookback + 1):-1]

    highest = max(c["high"] for c in recent)
    lowest = min(c["low"] for c in recent)

    current = candles[-1]

    # Buy-side liquidity sweep
    if current["high"] > highest and current["close"] < highest:
        return {
            "type": "BUY_SIDE_SWEEP",
            "level": round(highest, 4),
            "signal": "SELL"
        }

    # Sell-side liquidity sweep
    if current["low"] < lowest and current["close"] > lowest:
        return {
            "type": "SELL_SIDE_SWEEP",
            "level": round(lowest, 4),
            "signal": "BUY"
        }

    return {
        "type": "NONE",
        "level": 0.0,
        "signal": "WAIT"
    }


if __name__ == "__main__":

    candles = []

    price = 100.0

    for i in range(25):
        candles.append({
            "high": price + 1,
            "low": price - 1,
            "close": price
        })
        price += 0.5

    result = detect_liquidity_sweep(candles)

    print(result)
