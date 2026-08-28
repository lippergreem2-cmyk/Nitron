import MetaTrader5 as mt5
import pandas as pd


class TradeAnalyzer:

    def __init__(self):
        if not mt5.initialize():
            raise Exception("Failed to connect to MT5")

    def candles(self, symbol, timeframe=mt5.TIMEFRAME_M15, count=100):
        rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)

        if rates is None:
            return None

        df = pd.DataFrame(rates)
        return df

    def moving_average(self, df, period=20):
        return df["close"].rolling(period).mean()

    def analyze(self, symbol):

        df = self.candles(symbol)

        if df is None:
            return {
                "signal": "NONE",
                "reason": "No market data."
            }

        df["MA20"] = self.moving_average(df, 20)
        df["MA50"] = self.moving_average(df, 50)

        last = df.iloc[-1]

        if last["MA20"] > last["MA50"]:
            signal = "BUY"

        elif last["MA20"] < last["MA50"]:
            signal = "SELL"

        else:
            signal = "WAIT"

        return {
            "symbol": symbol,
            "price": last["close"],
            "signal": signal,
            "ma20": round(last["MA20"], 5),
            "ma50": round(last["MA50"], 5)
        }

    def close(self):
        mt5.shutdown()


if __name__ == "__main__":

    analyzer = TradeAnalyzer()

    print(analyzer.analyze("XAUUSD"))

    analyzer.close()
