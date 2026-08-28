# ==========================================================
# NITRON MULTI MARKET STRATEGY ENGINE
# ==========================================================

from confidence import calculate_confidence
from asset_detector import detect_asset, market_profile



class Strategy:


    def __init__(self, minimum_confidence=75):

        self.minimum_confidence = minimum_confidence



    def decide(self, analysis):

        buy_score = calculate_confidence(
            analysis["buy_signals"]
        )


        sell_score = calculate_confidence(
            analysis["sell_signals"]
        )


        if (
            buy_score["score"] >= self.minimum_confidence
            and buy_score["score"] > sell_score["score"]
        ):

            return {
                "signal": "BUY",
                "confidence": buy_score["score"]
            }



        if (
            sell_score["score"] >= self.minimum_confidence
            and sell_score["score"] > buy_score["score"]
        ):

            return {
                "signal": "SELL",
                "confidence": sell_score["score"]
            }



        return {

            "signal": "WAIT",

            "confidence":
                max(
                    buy_score["score"],
                    sell_score["score"]
                )

        }





def create_analysis(asset):


    # -------------------------
    # METALS
    # -------------------------

    if asset == "metals":

        return {

            "buy_signals": {

                "trend": True,
                "dollar_weak": True,
                "support": True,
                "volatility": True

            },


            "sell_signals": {

                "trend": False,
                "dollar_strong": False,
                "resistance": False,
                "volatility": False

            }

        }




    # -------------------------
    # CRYPTO
    # -------------------------

    if asset == "crypto":

        return {

            "buy_signals": {

                "momentum": True,
                "volume": True,
                "trend": True,
                "breakout": True

            },


            "sell_signals": {

                "momentum": False,
                "volume": False,
                "trend": False,
                "breakdown": False

            }

        }




    # -------------------------
    # STOCKS
    # -------------------------

    if asset == "stocks":

        return {

            "buy_signals": {

                "trend": True,
                "volume": True,
                "market_news": True

            },


            "sell_signals": {

                "trend": False,
                "volume": False,
                "market_news": False

            }

        }




    # -------------------------
    # FOREX
    # -------------------------

    if asset == "forex":

        return {

            "buy_signals": {

                "trend": True,
                "currency_strength": True,
                "support": True

            },


            "sell_signals": {

                "trend": False,
                "currency_strength": False,
                "resistance": False

            }

        }



    return {

        "buy_signals": {},

        "sell_signals": {}

    }





def analyze_trade(symbol, candles):


    asset = detect_asset(symbol)

    profile = market_profile(symbol)


    analysis = create_analysis(asset)


    strategy = Strategy()


    decision = strategy.decide(
        analysis
    )


    entry = candles[-1]["close"]



    if decision["signal"] == "BUY":

        stop_loss = entry * 0.98

        take_profit = entry * 1.04



    elif decision["signal"] == "SELL":

        stop_loss = entry * 1.02

        take_profit = entry * 0.96



    else:

        stop_loss = entry

        take_profit = entry




    return {


        "recommendation":
            decision["signal"],


        "confidence":
            decision["confidence"],


        "trend":
            profile["strategy"],


        "risk": {


            "entry":
                entry,


            "stop_loss":
                stop_loss,


            "take_profit":
                take_profit,


            "lot_size":
                0.01,


            "risk_reward":
                "1:2"

        },


        "message":
            f"{symbol} {profile['name']} analysis complete",


        "reasons": [

            profile["strategy"],

            "Asset-specific strategy",

            "Market type detection"

        ]

    }
