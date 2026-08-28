class Backtester:

    def __init__(self):
        self.balance = 1000.0
        self.start_balance = 1000.0
        self.trades = []

    def execute_trade(
        self,
        symbol,
        signal,
        entry,
        exit_price,
        lot_size
    ):

        if signal == "BUY":
            profit = (exit_price - entry) * lot_size

        elif signal == "SELL":
            profit = (entry - exit_price) * lot_size

        else:
            profit = 0

        self.balance += profit

        trade = {
            "symbol": symbol,
            "signal": signal,
            "entry": entry,
            "exit": exit_price,
            "lot_size": lot_size,
            "profit": round(profit, 2)
        }

        self.trades.append(trade)

        return trade

    def statistics(self):

        wins = sum(
            1 for trade in self.trades
            if trade["profit"] > 0
        )

        losses = sum(
            1 for trade in self.trades
            if trade["profit"] <= 0
        )

        total = len(self.trades)

        win_rate = 0

        if total:
            win_rate = round((wins / total) * 100, 2)

        return {
            "starting_balance": self.start_balance,
            "ending_balance": round(self.balance, 2),
            "profit": round(
                self.balance - self.start_balance,
                2
            ),
            "total_trades": total,
            "wins": wins,
            "losses": losses,
            "win_rate": win_rate
        }


if __name__ == "__main__":

    tester = Backtester()

    tester.execute_trade(
        "BTCUSD",
        "BUY",
        115000,
        116500,
        0.02
    )

    tester.execute_trade(
        "XAUUSD",
        "SELL",
        3400,
        3380,
        0.10
    )

    print(tester.statistics())
