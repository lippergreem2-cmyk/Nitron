# indicators/macd.py

from indicators.ema import calculate_ema


def calculate_macd(prices):

    ema_fast = calculate_ema(prices, 12)
    ema_slow = calculate_ema(prices, 26)

    if ema_fast is None or ema_slow is None:
        return None

    macd = ema_fast - ema_slow

    if macd > 0:
        signal = "BULLISH"
    elif macd < 0:
        signal = "BEARISH"
    else:
        signal = "NEUTRAL"

    return {
        "macd": round(macd, 5),
        "signal": signal
    }


if __name__ == "__main__":

    prices = list(range(100, 140))

    print(calculate_macd(prices))
