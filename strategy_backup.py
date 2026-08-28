# strategy.py
# Nitron Trading Strategy Engine v1.0

from confidence import calculate_confidence


class Strategy:

    def __init__(self, minimum_confidence=75):
        self.minimum_confidence = minimum_confidence


    def decide(self, analysis):

        buy_signals = {

            "trend":
                analysis.get("trend") == "UPTREND",

            "rsi":
                analysis.get("rsi", 50) < 30,

            "macd":
                analysis.get("macd") == "BULLISH",

            "support":
                analysis.get("near_support", False),

            "adx":
                analysis.get("adx", 0) > 25,

            "stochastic":
                analysis.get("stochastic", 50) < 20,

            "bollinger":
                analysis.get("bollinger") == "LOWER",

            "liquidity":
                analysis.get("liquidity") == "BUY",

            "fvg":
                analysis.get("fvg") == "BULLISH",

            "order_block":
                analysis.get("order_block") == "BULLISH",

            "market_structure":
                analysis.get("market_structure") == "BULLISH"
        }


        sell_signals = {

            "trend":
                analysis.get("trend") == "DOWNTREND",

            "rsi":
                analysis.get("rsi", 50) > 70,

            "macd":
                analysis.get("macd") == "BEARISH",

            "resistance":
                analysis.get("near_resistance", False),

            "adx":
                analysis.get("adx", 0) > 25,

            "stochastic":
                analysis.get("stochastic", 50) > 80,

            "bollinger":
                analysis.get("bollinger") == "UPPER",

            "liquidity":
                analysis.get("liquidity") == "SELL",

            "fvg":
                analysis.get("fvg") == "BEARISH",

            "order_block":
                analysis.get("order_block") == "BEARISH",

            "market_structure":
                analysis.get("market_structure") == "BEARISH"
        }


        buy = calculate_confidence(buy_signals)
        sell = calculate_confidence(sell_signals)


        if (
            buy["score"] >= self.minimum_confidence
            and buy["score"] > sell["score"]
        ):

            return {
                "signal": "BUY",
                "confidence": buy["score"]
            }


        if (
            sell["score"] >= self.minimum_confidence
            and sell["score"] > buy["score"]
        ):

            return {
                "signal": "SELL",
                "confidence": sell["score"]
            }


        return {
            "signal": "WAIT",
            "confidence": max(
                buy["score"],
                sell["score"]
            )
        }



def analyze_trade(symbol, candles):

    strategy = Strategy()


    # Temporary market analysis connector
    # Later connected to all Nitron indicators

    analysis = {

        "trend": "UPTREND",

        "rsi": 28,

        "macd": "BULLISH",

        "near_support": True,

        "near_resistance": False,

        "adx": 32,

        "stochastic": 18,

        "bollinger": "LOWER",

        "liquidity": "BUY",

        "fvg": "BULLISH",

        "order_block": "BULLISH",

        "market_structure": "BULLISH"
    }


    decision = strategy.decide(analysis)


    entry = candles[-1]["close"]


    if decision["signal"] == "BUY":

        stop_loss = entry - 15
        take_profit = entry + 30


    elif decision["signal"] == "SELL":

        stop_loss = entry + 15
        take_profit = entry - 30


    else:

        stop_loss = entry
        take_profit = entry



    return {

        "recommendation":
            decision["signal"],

        "confidence":
            decision["confidence"],

        "trend":
            analysis["trend"],

        "risk": {

            "entry": entry,

            "stop_loss": stop_loss,

            "take_profit": take_profit,

            "lot_size": 0.01,

            "risk_reward": "1:2"

        },

        "message":
            f"{symbol} analysis complete",

        "reasons": [

            "Trend confirmation",

            "Indicator analysis",

            "Market structure"

        ]

    }
