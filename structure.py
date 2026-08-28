# structure.py

from swings import swing_highs, swing_lows


def analyze_structure(candles):

    result = {
        "trend": "Neutral",
        "higher_high": False,
        "higher_low": False,
        "lower_high": False,
        "lower_low": False,
        "bos": False,
        "choch": False,
        "mss": False,
        "last_high": None,
        "last_low": None,
        "previous_high": None,
        "previous_low": None
    }

    if len(candles) < 20:
        return result

    highs = swing_highs(candles)
    lows = swing_lows(candles)

    if len(highs) < 2 or len(lows) < 2:
        return result

    previous_high = float(highs[-2]["price"])
    last_high = float(highs[-1]["price"])

    previous_low = float(lows[-2]["price"])
    last_low = float(lows[-1]["price"])

    result["previous_high"] = previous_high
    result["previous_low"] = previous_low
    result["last_high"] = last_high
    result["last_low"] = last_low

    # Higher High
    if last_high > previous_high:
        result["higher_high"] = True

    # Higher Low
    if last_low > previous_low:
        result["higher_low"] = True

    # Lower High
    if last_high < previous_high:
        result["lower_high"] = True

    # Lower Low
    if last_low < previous_low:
        result["lower_low"] = True

    # Trend Detection
    if result["higher_high"] and result["higher_low"]:
        result["trend"] = "Bullish"

    elif result["lower_high"] and result["lower_low"]:
        result["trend"] = "Bearish"

    else:
        result["trend"] = "Neutral"

    current_close = float(candles[-1]["close"])

    # Break Of Structure
    if current_close > last_high:
        result["bos"] = True

    elif current_close < last_low:
        result["bos"] = True

    # Change Of Character
    if result["trend"] == "Bullish":

        if current_close < last_low:
            result["choch"] = True

    elif result["trend"] == "Bearish":

        if current_close > last_high:
            result["choch"] = True

    # Market Structure Shift
    if result["bos"] and result["choch"]:
        result["mss"] = True

    return result


if __name__ == "__main__":

    from mt5_data import get_candles

    symbols = [
        "XAUUSD",
        "EURUSD",
        "GBPUSD",
        "BTCUSD"
    ]

    for symbol in symbols:

        candles = get_candles(symbol)

        print("=" * 60)
        print(symbol)
        print("=" * 60)

        structure = analyze_structure(candles)

        for key, value in structure.items():
            print(f"{key:15}: {value}")

        print()
