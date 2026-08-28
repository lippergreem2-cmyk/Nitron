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

    def statistics(self):

        trades = self.load_trades()

        total = len(trades)

        if total == 0:
            return {
                "total": 0,
                "wins": 0,
                "losses": 0,
                "win_rate": 0
            }

        wins = sum(
            1 for trade in trades
            if trade.get("result") == "WIN"
        )

        losses = sum(
            1 for trade in trades
            if trade.get("result") == "LOSS"
        )

        return {
            "total": total,
            "wins": wins,
            "losses": losses,
            "win_rate": round((wins / total) * 100, 2)
        }

    def best_symbol(self):

        trades = self.load_trades()

        scores = {}

        for trade in trades:

            symbol = trade.get("symbol")

            if symbol not in scores:
                scores[symbol] = 0

            if trade.get("result") == "WIN":
                scores[symbol] += 1
            else:
                scores[symbol] -= 1

        if not scores:
            return None

        return max(scores, key=scores.get)

    def recommendation(self):

        stats = self.statistics()

        if stats["win_rate"] >= 70:
            return "Trading performance is excellent."

        if stats["win_rate"] >= 50:
            return "Trading performance is acceptable."

        return "Trading performance needs improvement."


if __name__ == "__main__":

    ai = LearningEngine()

    print(ai.statistics())
    print("Best Symbol:", ai.best_symbol())
    print(ai.recommendation())
