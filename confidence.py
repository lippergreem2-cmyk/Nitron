# confidence.py
# Nitron Confidence Engine v2.0


def confidence_level(score):

    if score >= 90:
        return "VERY HIGH"

    elif score >= 75:
        return "HIGH"

    elif score >= 60:
        return "MEDIUM"

    elif score >= 40:
        return "LOW"

    else:
        return "VERY LOW"



def calculate_confidence(signals):
    """
    Calculate trading confidence score.

    signals example:

    {
        "trend": True,
        "rsi": True,
        "macd": False,
        "support": True
    }

    Returns:

    {
        "score": 75,
        "confidence": "HIGH"
    }
    """


    if not signals:

        return {

            "score": 0,

            "confidence": "VERY LOW"

        }



    total = len(signals)


    positive = sum(

        1

        for value in signals.values()

        if value

    )


    score = round(

        (positive / total) * 100

    )


    return {

        "score": score,

        "confidence":
            confidence_level(score)

    }



def compare(buy_signals, sell_signals):

    buy = calculate_confidence(
        buy_signals
    )

    sell = calculate_confidence(
        sell_signals
    )


    if buy["score"] > sell["score"]:

        return {

            "signal": "BUY",

            "score": buy["score"],

            "confidence":
                buy["confidence"]

        }


    elif sell["score"] > buy["score"]:

        return {

            "signal": "SELL",

            "score": sell["score"],

            "confidence":
                sell["confidence"]

        }


    return {

        "signal": "WAIT",

        "score":
            max(
                buy["score"],
                sell["score"]
            ),

        "confidence":
            confidence_level(
                max(
                    buy["score"],
                    sell["score"]
                )
            )

    }



if __name__ == "__main__":


    signals = {

        "trend": True,

        "rsi": True,

        "macd": True,

        "support": True,

        "adx": True,

        "liquidity": True,

        "fvg": False,

        "order_block": True

    }


    result = calculate_confidence(
        signals
    )


    print(result)
