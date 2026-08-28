import requests

from config import TWELVEDATA_API_KEY

BASE_URL = "https://api.twelvedata.com"


def get_price(symbol):
    try:
        url = f"{BASE_URL}/price"

        params = {
            "symbol": symbol,
            "apikey": TWELVEDATA_API_KEY
        }

        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if "price" in data:
            return float(data["price"])

        print("API Error:", data)
        return None

    except Exception as e:
        print("Connection Error:", e)
        return None


def analyze(symbol):

    symbol = symbol.upper()

    price = get_price(symbol)

    if price is None:
        return (
            f"{symbol}\n"
            "Status : No live data\n"
            "Signal : WAIT\n"
            "Risk   : 1%"
        )

    if symbol == "XAUUSD":
        signal = "BUY" if price > 4000 else "SELL"

    elif symbol == "BTCUSD":
        signal = "BUY" if price > 50000 else "SELL"

    elif symbol == "AAPL":
        signal = "BUY" if price > 200 else "SELL"

    else:
        signal = "WAIT"

    return (
        f"Asset   : {symbol}\n"
        f"Price   : {price}\n"
        f"Signal  : {signal}\n"
        "Risk    : 1%\n"
        "Source  : Twelve Data"
    )


def buy(symbol):

    symbol = symbol.upper()

    return (
        f"BUY request received.\n"
        f"Asset : {symbol}\n"
        "Automatic trading is disabled."
    )


def sell(symbol):

    symbol = symbol.upper()

    return (
        f"SELL request received.\n"
        f"Asset : {symbol}\n"
        "Automatic trading is disabled."
    )


def account():

    return (
        "========== NITRON ACCOUNT ==========\n"
        "Trading Mode : Manual\n"
        "Market Data  : Twelve Data API\n"
        "Status       : Connected\n"
        "===================================="
    )
