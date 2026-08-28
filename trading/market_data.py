from datetime import datetime
import random


class MarketData:

    def __init__(self):
        self.supported_symbols = [
            "BTCUSD",
            "XAUUSD",
            "EURUSD",
            "GBPUSD",
            "USDJPY"
        ]

    def get_price(self, symbol):

        if symbol not in self.supported_symbols:
            return None

        prices = {
            "BTCUSD": 115000.0,
            "XAUUSD": 3400.0,
            "EURUSD": 1.1650,
            "GBPUSD": 1.3450,
            "USDJPY": 151.80
        }

        return prices.get(symbol)

    def get_candle(self, symbol):

        price = self.get_price(symbol)

        if price is None:
            return None

        open_price = price
        close_price = price + random.uniform(-50, 50)
        high = max(open_price, close_price) + random.uniform(5, 20)
        low = min(open_price, close_price) - random.uniform(5, 20)

        return {
            "symbol": symbol,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "open": round(open_price, 2),
            "high": round(high, 2),
            "low": round(low, 2),
            "close": round(close_price, 2)
        }

    def get_market(self, symbol):

        candle = self.get_candle(symbol)

        if candle is None:
            return {
                "success": False,
                "message": "Unsupported symbol."
            }

        return {
            "success": True,
            "data": candle
        }


if __name__ == "__main__":

    market = MarketData()

    result = market.get_market("BTCUSD")

    print(result)
