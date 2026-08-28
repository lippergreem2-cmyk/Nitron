# mt5_data.py

import requests
from config import TWELVEDATA_API_KEY

BASE_URL = "https://api.twelvedata.com"

# Convert MT5 symbols to Twelve Data symbols
SYMBOLS = {
    "XAUUSD": "XAU/USD",
    "BTCUSD": "BTC/USD",
    "ETHUSD": "ETH/USD",
    "EURUSD": "EUR/USD",
    "GBPUSD": "GBP/USD",
    "USDJPY": "USD/JPY",
    "AUDUSD": "AUD/USD",
    "NZDUSD": "NZD/USD",
    "USDCAD": "USD/CAD",
    "USDCHF": "USD/CHF",
    "EURGBP": "EUR/GBP",
    "EURJPY": "EUR/JPY",
    "GBPJPY": "GBP/JPY",
    "AAPL": "AAPL",
    "TSLA": "TSLA",
    "NVDA": "NVDA"
}


def convert_symbol(symbol):
    symbol = symbol.upper().replace(" ", "")
    return SYMBOLS.get(symbol, symbol)


def connect():
    print("Connected to Twelve Data")
    return True


def disconnect():
    print("Disconnected")
    return True


def get_current_price(symbol):

    symbol = convert_symbol(symbol)

    url = f"{BASE_URL}/price"

    params = {
        "symbol": symbol,
        "apikey": TWELVEDATA_API_KEY
    }

    try:

        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if "price" not in data:
            print(data)
            return None

        price = float(data["price"])

        return {
            "bid": price,
            "ask": price
        }

    except Exception as e:

        print("Price Error:", e)
        return None


def get_candles(symbol, timeframe="15min", bars=200):

    symbol = convert_symbol(symbol)

    url = f"{BASE_URL}/time_series"

    params = {
        "symbol": symbol,
        "interval": timeframe,
        "outputsize": bars,
        "apikey": TWELVEDATA_API_KEY
    }

    try:

        response = requests.get(url, params=params, timeout=15)

        data = response.json()

        if "values" not in data:
            print(data)
            return []

        candles = []

        for c in reversed(data["values"]):

            candles.append({

                "time": c["datetime"],
                "open": float(c["open"]),
                "high": float(c["high"]),
                "low": float(c["low"]),
                "close": float(c["close"]),
                "volume": float(c.get("volume", 0))

            })

        return candles

    except Exception as e:

        print("Candles Error:", e)
        return []


def account_information():

    return {
        "balance": 0.0,
        "equity": 0.0,
        "margin": 0.0,
        "free_margin": 0.0,
        "profit": 0.0
    }


if __name__ == "__main__":

    connect()

    for symbol in [
        "XAUUSD",
        "EURUSD",
        "GBPUSD",
        "BTCUSD"
    ]:

        candles = get_candles(symbol)

        print(symbol, len(candles))

        if candles:
            print(candles[-1])

    disconnect()
