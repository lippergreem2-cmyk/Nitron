# ==========================================================
# NITRON TRADING CONVERSATION PARSER
# Converts human speech into trading symbols
# ==========================================================

from market_parser import extract_symbol


TRADING_WORDS = [
    "analyze",
    "analyse",
    "check",
    "look",
    "watch",
    "trade",
    "buy",
    "sell",
    "should i",
    "what about",
    "how is"
]


def is_trading_command(message):

    message = message.lower()

    return any(
        word in message
        for word in TRADING_WORDS
    )



def parse_trade_command(message):

    symbol = extract_symbol(message)

    if symbol:

        return {
            "type": "trade_analysis",
            "symbol": symbol
        }


    return None



def convert_to_command(message):

    result = parse_trade_command(message)

    if result:

        return (
            f"analyze {result['symbol']}"
        )

    return message
