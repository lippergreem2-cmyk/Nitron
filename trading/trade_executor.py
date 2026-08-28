from datetime import datetime


class TradeExecutor:

    def __init__(self):
        self.allowed_signals = ["BUY", "SELL"]

    def validate(self, trade):

        required = [
            "symbol",
            "signal",
            "entry",
            "stop_loss",
            "take_profit",
            "lot_size",
            "confidence"
        ]

        for field in required:
            if field not in trade:
                return False, f"Missing field: {field}"

        if trade["signal"] not in self.allowed_signals:
            return False, "Invalid signal"

        if trade["lot_size"] <= 0:
            return False, "Lot size must be greater than zero"

        if trade["confidence"] < 60:
            return False, "Confidence too low"

        return True, "Trade validated"

    def prepare(self, trade):

        valid, message = self.validate(trade)

        if not valid:
            return {
                "success": False,
                "message": message
            }

        return {
            "success": True,
            "message": "Trade ready",
            "trade": {
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "symbol": trade["symbol"],
                "signal": trade["signal"],
                "entry": trade["entry"],
                "stop_loss": trade["stop_loss"],
                "take_profit": trade["take_profit"],
                "lot_size": trade["lot_size"],
                "confidence": trade["confidence"]
            }
        }


if __name__ == "__main__":

    executor = TradeExecutor()

    trade = {
        "symbol": "BTCUSD",
        "signal": "BUY",
        "entry": 115000,
        "stop_loss": 114500,
        "take_profit": 116000,
        "lot_size": 0.01,
        "confidence": 86
    }

    result = executor.prepare(trade)

    print(result)
