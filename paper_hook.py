from tradelog import open_trade, check_open, open_trades

def make_logged(fn):
    def wrapper(symbol, candles):
        report = fn(symbol, candles)
        try:
            check_open(symbol, candles[-1]["close"])
            action = report.get("recommendation")
            already_open = any(t["symbol"] == symbol for t in open_trades())
            if action in ("BUY", "SELL") and not already_open:
                r = report["risk"]
                open_trade(
                    symbol,
                    "long" if action == "BUY" else "short",
                    str(report.get("trend", "unknown")),
                    r["entry"], r["stop_loss"], r["take_profit"],
                    indicators={"confidence": report.get("confidence"),
                                "reasons": report.get("reasons")},
                    mode="paper",
                )
        except Exception as e:
            print(f"[paper log] skipped: {e}")
        return report
    return wrapper
