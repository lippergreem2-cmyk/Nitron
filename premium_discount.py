# premium_discount.py

from swings import swing_highs, swing_lows


def premium_discount(candles):

    highs = swing_highs(candles)
    lows = swing_lows(candles)

    if not highs or not lows:
        return None

    swing_high = float(highs[-1]["price"])
    swing_low = float(lows[-1]["price"])

    high = max(swing_high, swing_low)
    low = min(swing_high, swing_low)

    equilibrium = (high + low) / 2

    current = float(candles[-1]["close"])

    if current > equilibrium:
        zone = "Premium"

    elif current < equilibrium:
        zone = "Discount"

    else:
        zone = "Equilibrium"

    return {
        "swing_high": swing_high,
        "swing_low": swing_low,
        "equilibrium": round(equilibrium, 5),
        "current_price": current,
        "zone": zone
    }


if __name__ == "__main__":

    from mt5_data import get_candles

    candles = get_candles("XAUUSD")

    print(premium_discount(candles))
