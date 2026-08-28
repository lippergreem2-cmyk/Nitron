import json
import os


class LearningEngine:

    def __init__(self, journal_file="trade_journal.json"):
        self.journal_file = journal_file

    def load_trades(self):

        if not os.path.exists(self.journal_file):
            return []

        with open(self.journal_file, "r") as f:
            return json.load(f)

    def analyze(self):

        trades = self.load_trades()

        if not trades:
            return {
                "total": 0,
                "wins": 0,
                "losses": 0,
                "win_rate": 0,
                "net_profit": 0,
                "recommendation": "Not enough data."
            }

        wins = 0
        losses = 0
        profit = 0

        buy_wins = 0
        sell_wins = 0

        for trade in trades:

            profit += trade.get("profit", 0)

            if trade.get("result") == "WIN":
                wins += 1

                if trade.get("signal") == "BUY":
                    buy_wins += 1

                elif trade.get("signal") == "SELL":
                    sell_wins += 1

            elif trade.get("result") == "LOSS":
                losses += 1

        total = wins + losses

        if total == 0:
            win_rate = 0
        else:
            win_rate = round((wins / total) * 100, 2)

        if win_rate >= 70:
            recommendation = "Current strategy is performing well."

        elif win_rate >= 50:
            recommendation = "Strategy is acceptable but can be improved."

        else:
            recommendation = "Review strategy before opening new trades."

        return {
            "total": total,
            "wins": wins,
            "losses": losses,
            "win_rate": win_rate,
            "buy_wins": buy_wins,
            "sell_wins": sell_wins,
            "net_profit": round(profit, 2),
            "recommendation": recommendation
        }


if __name__ == "__main__":

    engine = LearningEngine()

    report = engine.analyze()

    print(report)
