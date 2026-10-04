"""
Nitron Paper Trader V2.

Simulation only.
Never sends orders to a broker.
"""

from datetime import datetime

try:
    from .portfolio import Portfolio
    from .risk import RiskEngine
    from .instrument_specs import get_instrument
except ImportError:
    from portfolio import Portfolio
    from risk import RiskEngine
    from instrument_specs import get_instrument


class PaperTrader:

    def __init__(
        self,
        starting_balance=10000.0,
        risk_percent=1.0
    ):
        self.starting_balance = float(starting_balance)
        self.balance = float(starting_balance)

        self.risk = RiskEngine(
            account_balance=self.balance,
            risk_percent=risk_percent
        )

        self.portfolio = Portfolio()
        self.trade_history = []

    def _now(self):
        return datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    def _sync_risk_balance(self):
        self.risk.account_balance = self.balance

    def open_trade(
        self,
        symbol,
        signal,
        entry,
        stop_loss,
        take_profit,
        lot_size=None,
        confidence=0
    ):
        symbol = str(symbol).upper().strip()
        signal = str(signal).upper().strip()

        spec = get_instrument(symbol)

        if spec is None:
            return {
                "success": False,
                "message": f"Unsupported instrument: {symbol}"
            }

        if signal not in ("BUY", "SELL"):
            return {
                "success": False,
                "message": "Signal must be BUY or SELL"
            }

        entry = float(entry)
        stop_loss = float(stop_loss)
        take_profit = float(take_profit)

        if entry <= 0:
            return {
                "success": False,
                "message": "Entry must be greater than zero"
            }

        if signal == "BUY":

            if stop_loss >= entry:
                return {
                    "success": False,
                    "message":
                        "BUY stop-loss must be below entry"
                }

            if take_profit <= entry:
                return {
                    "success": False,
                    "message":
                        "BUY take-profit must be above entry"
                }

        else:

            if stop_loss <= entry:
                return {
                    "success": False,
                    "message":
                        "SELL stop-loss must be above entry"
                }

            if take_profit >= entry:
                return {
                    "success": False,
                    "message":
                        "SELL take-profit must be below entry"
                }

        self._sync_risk_balance()

        risk_result = self.risk.position_size_for_risk(
            symbol=symbol,
            entry=entry,
            stop_loss=stop_loss
        )

        if not risk_result.get("valid"):
            return {
                "success": False,
                "message": risk_result.get(
                    "message",
                    "Unable to calculate position size."
                )
            }

        suggested_lot = float(
            risk_result["suggested_lot_size"]
        )

        if lot_size is None:
            lot_size = suggested_lot
        else:
            lot_size = float(lot_size)

        if lot_size <= 0:
            return {
                "success": False,
                "message": "Lot size must be greater than zero"
            }

        if lot_size < spec["minimum_lot"]:
            return {
                "success": False,
                "message":
                    f"Lot size below minimum "
                    f"({spec['minimum_lot']})."
            }

        if lot_size > spec["maximum_lot"]:
            return {
                "success": False,
                "message":
                    f"Lot size above maximum "
                    f"({spec['maximum_lot']})."
            }

        # Round to instrument lot step.
        step = float(spec["lot_step"])
        lot_size = round(
            int(lot_size / step) * step,
            8
        )

        if lot_size <= 0:
            return {
                "success": False,
                "message": "Lot size becomes zero after rounding."
            }

        risk_analysis = self.risk.analyze(
            symbol=symbol,
            signal=signal,
            entry=entry,
            stop_loss=stop_loss,
            take_profit=take_profit,
            lot_size=lot_size
        )

        if not risk_analysis.get("valid"):
            return {
                "success": False,
                "message": risk_analysis.get(
                    "message",
                    "Risk validation failed."
                ),
                "risk": risk_analysis
            }

        if not risk_analysis["risk_within_limit"]:
            return {
                "success": False,
                "message": "Trade exceeds maximum risk limit.",
                "risk": risk_analysis
            }

        position = self.portfolio.add_position(
            symbol=symbol,
            signal=signal,
            entry=entry,
            lot_size=lot_size,
            stop_loss=stop_loss,
            take_profit=take_profit
        )

        position["confidence"] = float(confidence)
        position["opened_at"] = self._now()
        position["paper_trade"] = True
        position["risk_amount"] = risk_analysis["potential_loss"]
        position["risk_reward"] = risk_analysis["risk_reward"]

        self.trade_history.append({
            "event": "OPEN",
            "time": self._now(),
            "symbol": symbol,
            "signal": signal,
            "entry": entry,
            "lot_size": lot_size,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "confidence": float(confidence),
            "risk_amount": risk_analysis["potential_loss"],
            "risk_reward": risk_analysis["risk_reward"]
        })

        return {
            "success": True,
            "message": "Paper trade opened",
            "position": position,
            "risk": risk_analysis
        }

    def close_trade(self, symbol, exit_price):
        symbol = str(symbol).upper().strip()
        exit_price = float(exit_price)

        position = self.portfolio.close_position(
            symbol,
            exit_price
        )

        if position is None:
            return {
                "success": False,
                "message":
                    f"No open paper position for {symbol}"
            }

        profit = float(
            position.get("profit", 0.0)
        )

        self.balance += profit
        self._sync_risk_balance()

        position["closed_at"] = self._now()

        self.trade_history.append({
            "event": "CLOSE",
            "time": self._now(),
            "symbol": position["symbol"],
            "signal": position["signal"],
            "entry": position["entry"],
            "exit": exit_price,
            "lot_size": position["lot_size"],
            "profit": profit
        })

        return {
            "success": True,
            "message": "Paper trade closed",
            "position": position,
            "profit": profit,
            "balance": round(self.balance, 2)
        }

    def check_price(self, symbol, price):
        symbol = str(symbol).upper().strip()
        price = float(price)

        for position in self.portfolio.get_open_positions():

            if position["symbol"] != symbol:
                continue

            signal = position["signal"]

            if signal == "BUY":

                if price <= position["stop_loss"]:
                    result = self.close_trade(
                        symbol,
                        position["stop_loss"]
                    )
                    result["reason"] = "STOP_LOSS"
                    return result

                if price >= position["take_profit"]:
                    result = self.close_trade(
                        symbol,
                        position["take_profit"]
                    )
                    result["reason"] = "TAKE_PROFIT"
                    return result

            elif signal == "SELL":

                if price >= position["stop_loss"]:
                    result = self.close_trade(
                        symbol,
                        position["stop_loss"]
                    )
                    result["reason"] = "STOP_LOSS"
                    return result

                if price <= position["take_profit"]:
                    result = self.close_trade(
                        symbol,
                        position["take_profit"]
                    )
                    result["reason"] = "TAKE_PROFIT"
                    return result

        return {
            "success": True,
            "triggered": False,
            "message": "No exit level triggered"
        }

    def status(self):
        return {
            "mode": "PAPER_TRADING",
            "starting_balance":
                round(self.starting_balance, 2),
            "balance":
                round(self.balance, 2),
            "realized_profit":
                round(
                    self.balance - self.starting_balance,
                    2
                ),
            "open_positions":
                len(self.portfolio.get_open_positions()),
            "total_events":
                len(self.trade_history)
        }

    def history(self):
        return list(self.trade_history)


if __name__ == "__main__":

    print("===== NITRON PAPER TRADER V2 =====")

    trader = PaperTrader(
        starting_balance=10000,
        risk_percent=1.0
    )

    result = trader.open_trade(
        symbol="XAUUSD",
        signal="BUY",
        entry=4000,
        stop_loss=3980,
        take_profit=4040,
        confidence=72
    )

    print()
    print("===== OPEN TRADE =====")
    print(result)

    print()
    print("===== STATUS =====")
    print(trader.status())

    print()
    print("===== PRICE UPDATE =====")

    result = trader.check_price(
        "XAUUSD",
        4040
    )

    print(result)

    print()
    print("===== FINAL STATUS =====")
    print(trader.status())

    print()
    print("===== HISTORY =====")
    print(trader.history())
