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

    def save(self, trades):
        with open(self.filename, "w") as f:
            json.dump(trades, f, indent=4)

    def add_trade(
        self,
        symbol,
        signal,
        entry,
        stop_loss,
        take_profit,
        lot_size,
        confidence,
        result="OPEN",
        profit=0.0
    ):

        trades = self.load()

        trade = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "symbol": symbol,
            "signal": signal,
            "entry": entry,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "lot_size": lot_size,
            "confidence": confidence,
            "result": result,
            "profit": profit
        }

        trades.append(trade)

        self.save(trades)

        return trade

    def statistics(self):

        trades = self.load()

        total = len(trades)

        wins = sum(1 for t in trades if t["result"] == "WIN")
        losses = sum(1 for t in trades if t["result"] == "LOSS")

        profit = sum(t["profit"] for t in trades)

        if total == 0:
            win_rate = 0
        else:
            win_rate = round((wins / total) * 100, 2)

        return {
            "total_trades": total,
            "wins": wins,
            "losses": losses,
            "win_rate": win_rate,
            "profit": round(profit, 2)
        }


if __name__ == "__main__":

    journal = TradeJournal()

    journal.add_trade(
        symbol="BTCUSD",
        signal="BUY",
        entry=115000,
        stop_loss=114500,
        take_profit=116000,
        lot_size=0.02,
        confidence=88
    )

    print(journal.statistics())
