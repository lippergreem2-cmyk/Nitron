# ==========================================================
# NITRON ASSET DETECTOR
# Detects market type
# ==========================================================


ASSET_TYPES = {

    "crypto": [
        "BTCUSD",
        "ETHUSD",
        "BNBUSD",
        "SOLUSD",
        "XRPUSD",
        "ADAUSD"
    ],


    "forex": [
        "EURUSD",
        "GBPUSD",
        "USDJPY",
        "AUDUSD",
        "NZDUSD",
        "USDCAD",
        "USDCHF",
        "EURGBP",
        "EURJPY",
        "GBPJPY"
    ],


    "metals": [
        "XAUUSD",
        "XAGUSD",
        "XPTUSD"
    ],


    "stocks": [
        "AAPL",
        "TSLA",
        "NVDA",
        "MSFT",
        "GOOGL",
        "AMZN",
        "META"
    ]

}



def normalize_symbol(symbol):

    return symbol.upper().replace(
        " ",
        ""
    )



def detect_asset(symbol):

    symbol = normalize_symbol(symbol)


    for category, symbols in ASSET_TYPES.items():

        if symbol in symbols:

            return category



    # Automatic detection

    if symbol.endswith("USD"):

        return "forex"


    return "unknown"



def market_profile(symbol):

    asset = detect_asset(symbol)


    profiles = {


        "crypto": {

            "name": "Cryptocurrency",

            "risk": "High",

            "strategy":
                "Momentum + Volatility + Volume"

        },


        "forex": {

            "name": "Forex",

            "risk": "Medium",

            "strategy":
                "Trend + Currency Strength"

        },


        "metals": {

            "name": "Metal",

            "risk": "Medium",

            "strategy":
                "Dollar Strength + Volatility"

        },


        "stocks": {

            "name": "Stock",

            "risk": "Medium",

            "strategy":
                "Trend + Volume + Market News"

        },


        "unknown": {

            "name": "Unknown",

            "risk": "Unknown",

            "strategy":
                "General Analysis"

        }

    }


    return profiles[asset]



if __name__ == "__main__":

    for symbol in [
        "XAUUSD",
        "BTCUSD",
        "ETHUSD",
        "AAPL",
        "TSLA",
        "EURUSD"
    ]:

        print(
            symbol,
            "=>",
            detect_asset(symbol),
            market_profile(symbol)
        )
