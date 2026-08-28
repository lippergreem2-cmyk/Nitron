import json
import os
from datetime import datetime


class TradeJournal:

    def __init__(self, filename="trade_journal.json"):
        self.filename = filename

        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                json.dump([], f, indent=4)

    def load(self):

        with open(self.filename, "r") as f:
            return json.load(f)

    def save_trade(self, trade):

        trades = self.load()

        trade["saved_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        trades.append(trade)

        with open(self.filename, "w") as f:
            json.dump(trades, f, indent=4)

        return True

    def total_trades(self):

        return len(self.load())

    def wins(self):

        trades = self.load()
        return sum(
            1 for trade in trades
            if trade.get("result") == "WIN"
        )

    def losses(self):

        trades = self.load()
        return sum(
            1 for trade in trades
            if trade.get("result") == "LOSS"
        )

    def statistics(self):

        total = self.total_trades()
        wins = self.wins()
        losses = self.losses()

        if total == 0:
            win_rate = 0
        else:
            win_rate = round((wins / total) * 100, 2)

        return {
            "total_trades": total,
            "wins": wins,
            "losses": losses,
            "win_rate": win_rate
        }


if __name__ == "__main__":

    journal = TradeJournal()

    journal.save_trade({
        "symbol": "BTCUSD",
        "signal": "BUY",
        "entry": 115000,
        "exit": 116000,
        "profit": 100,
        "result": "WIN"
    })

    print(journal.statistics())
