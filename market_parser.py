# ==========================================================
# NITRON MARKET COMMAND PARSER
# Converts human words into trading symbols
# ==========================================================


MARKET_WORDS = {

    "bitcoin": "BTCUSD",
    "btc": "BTCUSD",

    "ethereum": "ETHUSD",
    "eth": "ETHUSD",

    "gold": "XAUUSD",
    "xau": "XAUUSD",

    "silver": "XAGUSD",

    "apple": "AAPL",
    "aapl": "AAPL",

    "tesla": "TSLA",
    "tsla": "TSLA",

    "nvidia": "NVDA",
    "nvda": "NVDA",

    "euro": "EURUSD",
    "eurusd": "EURUSD",

    "pound": "GBPUSD",
    "gbpusd": "GBPUSD"

}



def extract_symbol(message):

    message = message.lower()


    for word, symbol in MARKET_WORDS.items():

        if word in message:

            return symbol


    return None
