def detect_order_block(candles, lookback=20):
    """
    Detect Bullish and Bearish Order Blocks

    candles = [
        {
            "open": 100,
            "high": 102,
            "low": 99,
            "close": 101
        }
    ]
    """

    if len(candles) < lookback:
        return {
            "found": False,
            "type": "NONE",
            "high": 0.0,
            "low": 0.0
        }

    recent = candles[-lookback:]

    # Bullish Order Block
    for i in range(len(recent) - 2):
        candle = recent[i]
        next_candle = recent[i + 1]

        if (
            candle["close"] < candle["open"] and
            next_candle["close"] > candle["high"]
        ):
            return {
                "found": True,
                "type": "BULLISH",
                "high": round(candle["high"], 4),
                "low": round(candle["low"], 4)
            }

    # Bearish Order Block
    for i in range(len(recent) - 2):
        candle = recent[i]
        next_candle = recent[i + 1]

        if (
            candle["close"] > candle["open"] and
            next_candle["close"] < candle["low"]
        ):
            return {
                "found": True,
                "type": "BEARISH",
                "high": round(candle["high"], 4),
                "low": round(candle["low"], 4)
            }

    return {
        "found": False,
        "type": "NONE",
        "high": 0.0,
        "low": 0.0
    }


if __name__ == "__main__":

    candles = [
        {
            "open": 105,
            "high": 106,
            "low": 103,
            "close": 104
        },
        {
            "open": 104,
            "high": 108,
            "low": 104,
            "close": 109
        }
    ] * 10

    result = detect_order_block(candles)

    print(result)
