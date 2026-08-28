import random
from datetime import datetime


class LiveData:

    def __init__(self):
        self.prices = {
            "BTCUSD": 115000.0,
            "XAUUSD": 3400.0,
            "EURUSD": 1.1700,
            "GBPUSD": 1.3600
        }

    def get_price(self, symbol):

        if symbol not in self.prices:
            return None

        change = random.uniform(-1.0, 1.0)

        self.prices[symbol] += change

        return {
            "symbol": symbol,
            "price": round(self.prices[symbol], 5),
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def get_prices(self):

        data = []

        for symbol in self.prices:
            data.append(self.get_price(symbol))

        return data


if __name__ == "__main__":

    live = LiveData()

    while True:

        prices = live.get_prices()

        for item in prices:
            print(item)

        print("-" * 50)

        import time
        time.sleep(5)
