"""
Nitron Paper Portfolio.

Tracks simulated positions and calculates P/L using
Nitron instrument specifications.

No broker connection.
No real-money execution.
"""

try:
    from .instrument_specs import get_instrument
except ImportError:
    from instrument_specs import get_instrument


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
        symbol = str(symbol).upper().strip()
        signal = str(signal).upper().strip()

        if get_instrument(symbol) is None:
            raise ValueError(f"Unsupported instrument: {symbol}")

        position = {
            "symbol": symbol,
            "signal": signal,
            "entry": float(entry),
            "lot_size": float(lot_size),
            "stop_loss": float(stop_loss),
            "take_profit": float(take_profit),
            "status": "OPEN"
        }

        self.positions.append(position)

        return position

    def calculate_profit(self, position, exit_price):
        """
        Calculate simulated gross P/L.

        P/L = price movement × contract size × lot size
        """

        spec = get_instrument(position["symbol"])

        if spec is None:
            raise ValueError(
                f"Unsupported instrument: {position['symbol']}"
            )

        entry = float(position["entry"])
        exit_price = float(exit_price)
        lot_size = float(position["lot_size"])
        contract_size = float(spec["contract_size"])

        if position["signal"] == "BUY":
            price_difference = exit_price - entry

        elif position["signal"] == "SELL":
            price_difference = entry - exit_price

        else:
            raise ValueError(
                f"Unsupported signal: {position['signal']}"
            )

        profit = (
            price_difference
            * contract_size
            * lot_size
        )

        return round(profit, 2)

    def close_position(self, symbol, exit_price):

        symbol = str(symbol).upper().strip()
        exit_price = float(exit_price)

        for position in self.positions:

            if (
                position["symbol"] == symbol
                and position["status"] == "OPEN"
            ):

                profit = self.calculate_profit(
                    position,
                    exit_price
                )

                position["status"] = "CLOSED"
                position["exit"] = exit_price
                position["profit"] = profit

                return position

        return None

    def get_open_positions(self):
        return [
            position
            for position in self.positions
            if position["status"] == "OPEN"
        ]

    def total_profit(self):
        total = sum(
            position.get("profit", 0.0)
            for position in self.positions
        )

        return round(total, 2)


if __name__ == "__main__":

    print("===== NITRON PORTFOLIO V2 TEST =====")

    portfolio = Portfolio()

    # XAUUSD:
    # $40 movement × 100 contract size × 0.10 lot
    # = $400 simulated profit
    portfolio.add_position(
        "XAUUSD",
        "BUY",
        4000,
        0.10,
        3980,
        4040
    )

    result = portfolio.close_position(
        "XAUUSD",
        4040
    )

    print()
    print("Closed XAUUSD position:")
    print(result)

    print()
    print("Total Profit:")
    print(portfolio.total_profit())

    # BTCUSD:
    # $1,200 movement × 1 contract size × 0.02 lot
    # = $24 simulated profit
    portfolio.add_position(
        "BTCUSD",
        "BUY",
        115000,
        0.02,
        114500,
        116000
    )

    result = portfolio.close_position(
        "BTCUSD",
        116200
    )

    print()
    print("Closed BTCUSD position:")
    print(result)

    print()
    print("Final Total Profit:")
    print(portfolio.total_profit())
