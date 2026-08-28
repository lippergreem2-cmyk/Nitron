# ==========================================================
# trade_controller.py
# Nitron Trading Controller v3.0
# ==========================================================


from trade_advisor import advise


from trade_executor import (
    market_order,
    get_trades,
    close_trade
)


try:
    from trade_display import (
        show_analysis,
        show_open_trade
    )

except Exception:

    show_analysis = None
    show_open_trade = None



last_trade_plan = None



# ==========================================================
# ANALYZE TRADE
# ==========================================================

def analyze_trade(symbol="XAUUSD"):

    global last_trade_plan


    report = advise(symbol)


    if report.get("action") == "WAIT":

        return {

            "status": "WAIT",

            "symbol": symbol,

            "message":
                report.get(
                    "reason",
                    "No trade setup."
                )

        }


    last_trade_plan = report



    result = {


        "status":
            "ANALYSIS_COMPLETE",


        "symbol":
            report.get(
                "symbol",
                symbol
            ),


        "action":
            report.get(
                "action",
                "WAIT"
            ),


        "confidence":
            report.get(
                "confidence",
                0
            ),


        "entry":
            report.get(
                "entry",
                0
            ),


        "stop_loss":
            report.get(
                "stop_loss",
                0
            ),


        "take_profit":
            report.get(
                "take_profit",
                0
            ),


        "lot_size":
            report.get(
                "lot_size",
                0
            ),


        "risk_reward":
            report.get(
                "risk_reward",
                "N/A"
            ),


        "message":

            "Waiting for confirmation: Place trade?"

    }



    if show_analysis:

        show_analysis(result)



    return result




# ==========================================================
# PLACE TRADE
# ==========================================================

def place_trade():


    global last_trade_plan



    if last_trade_plan is None:

        return {

            "success": False,

            "message":
                "No trade analysis available. Run analyze first."

        }



    result = market_order(


        last_trade_plan["symbol"],


        last_trade_plan["action"],


        last_trade_plan["lot_size"],


        last_trade_plan["stop_loss"],


        last_trade_plan["take_profit"],


        last_trade_plan["entry"]

    )



    if (
        result.get("success")
        and show_open_trade
    ):

        show_open_trade(
            result["trade"]
        )



    return result




# ==========================================================
# SHOW ACTIVE TRADES
# ==========================================================

def show_trades():

    return {

        "active_trades":
            get_trades()

    }




# ==========================================================
# CLOSE TRADE
# ==========================================================

def close_trade_by_ticket(ticket):

    return close_trade(ticket)




# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":


    print(
        analyze_trade(
            "XAUUSD"
        )
    )


    print(
        place_trade()
    )


    print(
        show_trades()
    )
