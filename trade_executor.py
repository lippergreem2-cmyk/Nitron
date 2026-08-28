# trade_executor.py
# Nitron Trade Executor v2.0

import time


AUTO_TRADE = False
DEMO_MODE = True


open_trades = []



def market_order(
        symbol,
        action,
        lot,
        stop_loss,
        take_profit,
        entry
):

    if not AUTO_TRADE and not DEMO_MODE:

        return {
            "success": False,
            "message": "Trading disabled"
        }


    trade = {

        "ticket":
            int(time.time()),

        "symbol":
            symbol,

        "action":
            action,

        "lot":
            lot,

        "entry":
            entry,

        "stop_loss":
            stop_loss,

        "take_profit":
            take_profit,

        "status":
            "OPEN",

        "mode":
            "DEMO" if DEMO_MODE else "REAL"

    }


    open_trades.append(trade)


    return {

        "success": True,

        "message":
            "Trade opened",

        "trade":
            trade

    }



def get_trades():

    return open_trades



def close_trade(ticket):

    for trade in open_trades:

        if trade["ticket"] == ticket:

            trade["status"] = "CLOSED"

            return {

                "success": True,

                "message":
                    "Trade closed",

                "trade":
                    trade

            }


    return {

        "success": False,

        "message":
            "Trade not found"

    }



if __name__ == "__main__":


    result = market_order(

        "XAUUSD",

        "BUY",

        0.01,

        3330,

        3370,

        3345

    )


    print(result)

    print(get_trades())
