# trade_advisor.py

from strategy import analyze_trade
from confidence import confidence_level
from news_filter import can_trade
from mt5_data import get_candles


def advise(symbol):

    symbol = symbol.strip().upper()

    if symbol == "":
        symbol = "XAUUSD"

    news = can_trade()

    if not news["allowed"]:
        return {
            "symbol": symbol,
            "action": "WAIT",
            "reason": news["reason"]
        }

    candles = get_candles(symbol)

    if candles is None:
        return {
            "symbol": symbol,
            "action": "WAIT",
            "reason": "Unable to download market data."
        }

    if len(candles) == 0:
        return {
            "symbol": symbol,
            "action": "WAIT",
            "reason": "No market data returned."
        }

    if len(candles) < 20:
        return {
            "symbol": symbol,
            "action": "WAIT",
            "reason": f"Only {len(candles)} candles available."
        }

    report = analyze_trade(symbol, candles)

    return {
        "symbol": symbol,
        "action": report["recommendation"],
        "trend": report["trend"],
        "confidence": report["confidence"],
        "confidence_level": confidence_level(report["confidence"]),
        "entry": report["risk"]["entry"],
        "stop_loss": report["risk"]["stop_loss"],
        "take_profit": report["risk"]["take_profit"],
        "lot_size": report["risk"]["lot_size"],
        "risk_reward": report["risk"]["risk_reward"],
        "message": report["message"],
        "reasons": report["reasons"]
    }


def print_advice(advice):

    print("=" * 60)
    print("               NITRON TRADE ADVISOR")
    print("=" * 60)

    print(f"Symbol      : {advice.get('symbol', 'N/A')}")
    print(f"Action      : {advice.get('action', 'WAIT')}")

    if "trend" in advice:
        print(f"Trend       : {advice['trend']}")

    if "confidence" in advice:
        print(f"Confidence  : {advice['confidence']}%")
        print(f"Level       : {advice['confidence_level']}")

    if "entry" in advice:
        print(f"Entry       : {advice['entry']}")
        print(f"Stop Loss   : {advice['stop_loss']}")
        print(f"Take Profit : {advice['take_profit']}")
        print(f"Lot Size    : {advice['lot_size']}")
        print(f"R:R         : {advice['risk_reward']}")

    if "message" in advice:
        print(f"Message     : {advice['message']}")

    if "reason" in advice:
        print(f"Reason      : {advice['reason']}")

    if "reasons" in advice:
        print("\nReasons")
        print("-" * 60)
        for reason in advice["reasons"]:
            print("•", reason)

    print("=" * 60)


if __name__ == "__main__":

    symbol = input(
        "Enter Symbol (default XAUUSD): "
    ).strip().upper()

    if symbol == "":
        symbol = "XAUUSD"

    advice = advise(symbol)

    print_advice(advice)
