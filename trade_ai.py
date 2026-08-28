import pandas as pd


class TradeAI:
    def __init__(self):
        self.fast_ma = 20
        self.slow_ma = 50

    def analyze(self, candles):
        """
        candles = list of dictionaries:
        [
            {"close": 1.1020},
            {"close": 1.1032},
            ...
        ]
        """

        if len(candles) < self.slow_ma:
            return {
                "signal": "WAIT",
                "reason": "Not enough candle data."
            }

        df = pd.DataFrame(candles)

        df["ma20"] = df["close"].rolling(self.fast_ma).mean()
        df["ma50"] = df["close"].rolling(self.slow_ma).mean()

        latest = df.iloc[-1]

        if latest["ma20"] > latest["ma50"]:
            signal = "BUY"

        elif latest["ma20"] < latest["ma50"]:
            signal = "SELL"

        else:
            signal = "WAIT"

        return {
            "signal": signal,
            "price": latest["close"],
            "ma20": latest["ma20"],
            "ma50": latest["ma50"]
        }


if __name__ == "__main__":

    candles = []

    price = 100

    for i in range(60):
        candles.append({"close": price})
        price += 0.5

    ai = TradeAI()

    print(ai.analyze(candles))
