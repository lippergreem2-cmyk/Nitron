# fair_value_gap.py

def f(x):
    return float(x)


def bullish_fvg(candles):

    gaps = []

    for i in range(2, len(candles)):

        c1 = candles[i - 2]
        c2 = candles[i - 1]
        c3 = candles[i]

        if (
            f(c3["low"]) > f(c1["high"])
            and f(c2["close"]) > f(c2["open"])
        ):

            gaps.append({
                "index": i,
                "type": "Bullish",
                "top": f(c3["low"]),
                "bottom": f(c1["high"])
            })

    return gaps


def bearish_fvg(candles):

    gaps = []

    for i in range(2, len(candles)):

        c1 = candles[i - 2]
        c2 = candles[i - 1]
        c3 = candles[i]

        if (
            f(c3["high"]) < f(c1["low"])
            and f(c2["close"]) < f(c2["open"])
        ):

            gaps.append({
                "index": i,
                "type": "Bearish",
                "top": f(c1["low"]),
                "bottom": f(c3["high"])
            })

    return gaps


def latest_fvg(candles):

    bulls = bullish_fvg(candles)
    bears = bearish_fvg(candles)

    if bulls and bears:

        if bulls[-1]["index"] > bears[-1]["index"]:
            return bulls[-1]

        return bears[-1]

    if bulls:
        return bulls[-1]

    if bears:
        return bears[-1]

    return None


def inside_fvg(price, gap):

    if gap is None:
        return False

    return gap["bottom"] <= price <= gap["top"]


if __name__ == "__main__":

    from mt5_data import get_candles

    candles = get_candles("XAUUSD")

    gap = latest_fvg(candles)

    print("Latest FVG")
    print(gap)

    if gap:

        price = float(candles[-1]["close"])

        print("Current Price:", price)
        print("Inside FVG:", inside_fvg(price, gap))
