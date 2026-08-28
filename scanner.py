# scanner.py

from mt5_data import connect, disconnect, get_candles
from strategy import analyze_trade

# Symbols to scan
SYMBOLS = [
    "XAUUSD",
    "EURUSD",
    "GBPUSD",
    "USDJPY",
    "USDCHF",
    "AUDUSD",
    "NZDUSD",
    "USDCAD",
    "BTCUSD",
    "ETHUSD",
    "NAS100",
    "US30"
]


def scan_market():

    results = []

    for symbol in SYMBOLS:

        try:

            candles = get_candles(symbol, bars=200)

            if len(candles) < 50:
                continue

            report = analyze_trade(symbol, candles)

            results.append(report)

        except Exception as e:

            print(symbol, e)

    results.sort(
        key=lambda x: x["confidence"],
        reverse=True
    )

    return results


def print_results(results):

    print("=" * 75)
    print("                 NITRON MARKET SCANNER")
    print("=" * 75)

    for r in results:

        print(
            f"{r['symbol']:10}"
            f"{r['recommendation']:8}"
            f"{r['confidence']:>4}%"
            f"   Trend: {r['trend']}"
        )

    print("=" * 75)


def best_trade(results):

    if len(results) == 0:
        return None

    return results[0]


if __name__ == "__main__":

    if connect():

        reports = scan_market()

        print_results(reports)

        trade = best_trade(reports)

        if trade:

            print("\nBEST TRADE")

            print("---------------------------")

            print("Symbol :", trade["symbol"])
            print("Action :", trade["recommendation"])
            print("Trend  :", trade["trend"])
            print("Score  :", trade["confidence"])

            print("\nEntry")

            print(trade["risk"])

        disconnect()
