# ==========================================================
# NITRON TRADE ADVISOR
# Multi Market Trading System
# ==========================================================


from strategy import analyze_trade
from confidence import confidence_level
from news_filter import can_trade
from mt5_data import get_candles
from market_parser import extract_symbol



def advise(command):

    # Convert human command to symbol

    symbol = extract_symbol(command)


    if symbol is None:

        symbol = command.strip().upper()


    if symbol == "":

        symbol = "XAUUSD"



    # News check

    news = can_trade()


    if not news["allowed"]:

        return {

            "symbol": symbol,

            "action": "WAIT",

            "reason": news["reason"]

        }




    # Get market candles

    candles = get_candles(symbol)



    if candles is None:

        return {

            "symbol": symbol,

            "action": "WAIT",

            "reason":
                "Unable to download market data."

        }



    if len(candles) == 0:

        return {

            "symbol": symbol,

            "action": "WAIT",

            "reason":
                "No market data returned."

        }



    if len(candles) < 20:

        return {

            "symbol": symbol,

            "action": "WAIT",

            "reason":
                f"Only {len(candles)} candles available."

        }




    # Run multi-market strategy

    report = analyze_trade(

        symbol,

        candles

    )



    return {


        "symbol":
            symbol,


        "action":
            report["recommendation"],


        "trend":
            report["trend"],


        "confidence":
            report["confidence"],


        "confidence_level":
            confidence_level(
                report["confidence"]
            ),


        "entry":
            report["risk"]["entry"],


        "stop_loss":
            report["risk"]["stop_loss"],


        "take_profit":
            report["risk"]["take_profit"],


        "lot_size":
            report["risk"]["lot_size"],


        "risk_reward":
            report["risk"]["risk_reward"],


        "message":
            report["message"],


        "reasons":
            report["reasons"]

    }





def print_advice(advice):


    print("=" * 60)

    print(
        "          NITRON TRADE ADVISOR"
    )

    print("=" * 60)



    print(
        "Symbol:",
        advice.get(
            "symbol",
            "N/A"
        )
    )


    print(
        "Action:",
        advice.get(
            "action",
            "WAIT"
        )
    )



    if "confidence" in advice:

        print(
            "Confidence:",
            advice["confidence"],
            "%"
        )


    if "entry" in advice:

        print(
            "Entry:",
            advice["entry"]
        )


        print(
            "Stop Loss:",
            advice["stop_loss"]
        )


        print(
            "Take Profit:",
            advice["take_profit"]
        )


    if "message" in advice:

        print(
            "Message:",
            advice["message"]
        )


    if "reason" in advice:

        print(
            "Reason:",
            advice["reason"]
        )


    if "reasons" in advice:

        print("\nReasons:")

        for reason in advice["reasons"]:

            print(
                "-",
                reason
            )


    print("=" * 60)





if __name__ == "__main__":


    command = input(

        "Enter market command: "

    )


    result = advise(command)


    print_advice(result)
