import json
import os


class PerformanceTracker:

    def __init__(self, journal_file="trade_journal.json"):
        self.journal_file = journal_file

    def load_trades(self):

        if not os.path.exists(self.journal_file):
            return []

        with open(self.journal_file, "r") as file:
            return json.load(file)

    def summary(self):

        trades = self.load_trades()

        total_profit = 0
        total_loss = 0
        wins = 0
        losses = 0

        for trade in trades:

            profit = trade.get("profit", 0)

            if profit >= 0:
                total_profit += profit
                wins += 1
            else:
                total_loss += abs(profit)
                losses += 1

        total = wins + losses

        if total == 0:
            win_rate = 0
        else:
            win_rate = round((wins / total) * 100, 2)

        profit_factor = (
            round(total_profit / total_loss, 2)
            if total_loss > 0 else 0
        )

        return {
            "total_trades": total,
            "wins": wins,
            "losses": losses,
            "win_rate": win_rate,
            "gross_profit": round(total_profit, 2),
            "gross_loss": round(total_loss, 2),
            "net_profit": round(total_profit - total_loss, 2),
            "profit_factor": profit_factor
        }


if __name__ == "__main__":

    tracker = PerformanceTracker()

    print(tracker.summary())
