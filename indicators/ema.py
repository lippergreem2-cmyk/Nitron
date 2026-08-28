# indicators/ema.py

def calculate_ema(prices, period=14):

    if len(prices) < period:
        return None

    multiplier = 2 / (period + 1)

    ema = sum(prices[:period]) / period

    for price in prices[period:]:
        ema = (price - ema) * multiplier + ema

    return round(ema, 5)


if __name__ == "__main__":

    prices = [
        100,101,102,103,104,
        105,106,107,108,109,
        110,111,112,113,114
    ]

    print("EMA:", calculate_ema(prices))
