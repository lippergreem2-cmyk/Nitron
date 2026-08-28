class Portfolio:

    def __init__(self):
        self.positions = []

    def add_position(
        self,
        symbol,
        signal,
        entry,
        lot_size,
        stop_loss,
        take_profit
    ):

        position = {
            "symbol": symbol,
            "signal": signal,
            "entry": entry,
            "lot_size": lot_size,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "status": "OPEN"
        }

        self.positions.append(position)

        return position

    def close_position(self, symbol, exit_price):

        for position in self.positions:

            if (
                position["symbol"] == symbol and
                position["status"] == "OPEN"
            ):

                position["status"] = "CLOSED"
                position["exit"] = exit_price

                if position["signal"] == "BUY":
                    profit = (
                        exit_price - position["entry"]
                    ) * position["lot_size"]

                else:
                    profit = (
                        position["entry"] - exit_price
                    ) * position["lot_size"]

                position["profit"] = round(profit, 2)

                return position

        return None

    def get_open_positions(self):

        return [
            p for p in self.positions
            if p["status"] == "OPEN"
        ]

    def total_profit(self):

        total = 0

        for position in self.positions:
            total += position.get("profit", 0)

        return round(total, 2)


if __name__ == "__main__":

    portfolio = Portfolio()

    portfolio.add_position(
        "BTCUSD",
        "BUY",
        115000,
        0.02,
        114500,
        116000
    )

    portfolio.add_position(
        "XAUUSD",
        "SELL",
        3400,
        0.10,
        3410,
        3380
    )

    portfolio.close_position(
        "BTCUSD",
        116200
    )

    print("Open Positions:")
    print(portfolio.get_open_positions())

    print()

    print("Total Profit:")
    print(portfolio.total_profit())
