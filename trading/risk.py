try:
    from .instrument_specs import get_instrument
except ImportError:
    from instrument_specs import get_instrument


class RiskEngine:
    """
    Risk calculations for Nitron paper trading.

    No real orders are placed.
    """

    def __init__(
        self,
        account_balance=10000.0,
        risk_percent=1.0,
        max_risk_percent=2.0
    ):
        self.account_balance = float(account_balance)
        self.risk_percent = float(risk_percent)
        self.max_risk_percent = float(max_risk_percent)

    def risk_amount(self, risk_percent=None):
        if risk_percent is None:
            risk_percent = self.risk_percent

        return round(
            self.account_balance * float(risk_percent) / 100,
            2
        )

    def position_size_for_risk(
        self,
        symbol,
        entry,
        stop_loss,
        risk_percent=None
    ):
        spec = get_instrument(symbol)

        if spec is None:
            return {
                "valid": False,
                "message": f"Unsupported instrument: {symbol}"
            }

        entry = float(entry)
        stop_loss = float(stop_loss)

        if entry <= 0:
            return {
                "valid": False,
                "message": "Entry must be greater than zero"
            }

        stop_distance = abs(entry - stop_loss)

        if stop_distance <= 0:
            return {
                "valid": False,
                "message": "Entry and stop-loss cannot be equal"
            }

        if risk_percent is None:
            risk_percent = self.risk_percent

        risk_amount = self.risk_amount(risk_percent)

        contract_size = spec["contract_size"]

        raw_lot_size = (
            risk_amount /
            (stop_distance * contract_size)
        )

        minimum_lot = spec["minimum_lot"]
        maximum_lot = spec["maximum_lot"]
        lot_step = spec["lot_step"]

        # Round DOWN to the instrument's lot step.
        lot_size = (
            int(raw_lot_size / lot_step) *
            lot_step
        )

        lot_size = round(lot_size, 8)

        if lot_size < minimum_lot:
            lot_size = 0.0

        if lot_size > maximum_lot:
            lot_size = maximum_lot

        estimated_loss = (
            stop_distance *
            contract_size *
            lot_size
        )

        return {
            "valid": lot_size > 0,
            "symbol": symbol.upper(),
            "account_balance": round(
                self.account_balance, 2
            ),
            "risk_percent": float(risk_percent),
            "risk_amount": risk_amount,
            "entry": entry,
            "stop_loss": stop_loss,
            "stop_distance": round(
                stop_distance, 5
            ),
            "contract_size": contract_size,
            "raw_lot_size": round(
                raw_lot_size, 8
            ),
            "suggested_lot_size": lot_size,
            "estimated_loss": round(
                estimated_loss, 2
            ),
            "minimum_lot": minimum_lot,
            "maximum_lot": maximum_lot,
            "lot_step": lot_step
        }

    def analyze(
        self,
        symbol,
        signal,
        entry,
        stop_loss,
        take_profit,
        lot_size
    ):
        signal = str(signal).upper()

        spec = get_instrument(symbol)

        if spec is None:
            return {
                "valid": False,
                "message": f"Unsupported instrument: {symbol}"
            }

        entry = float(entry)
        stop_loss = float(stop_loss)
        take_profit = float(take_profit)
        lot_size = float(lot_size)

        if signal not in ("BUY", "SELL"):
            return {
                "valid": False,
                "message": "Signal must be BUY or SELL"
            }

        if lot_size <= 0:
            return {
                "valid": False,
                "message": "Lot size must be greater than zero"
            }

        if signal == "BUY":

            if stop_loss >= entry:
                return {
                    "valid": False,
                    "message": "BUY stop-loss must be below entry"
                }

            if take_profit <= entry:
                return {
                    "valid": False,
                    "message": "BUY take-profit must be above entry"
                }

            stop_distance = entry - stop_loss
            target_distance = take_profit - entry

        else:

            if stop_loss <= entry:
                return {
                    "valid": False,
                    "message": "SELL stop-loss must be above entry"
                }

            if take_profit >= entry:
                return {
                    "valid": False,
                    "message": "SELL take-profit must be below entry"
                }

            stop_distance = stop_loss - entry
            target_distance = entry - take_profit

        contract_size = spec["contract_size"]

        potential_loss = (
            stop_distance *
            contract_size *
            lot_size
        )

        potential_profit = (
            target_distance *
            contract_size *
            lot_size
        )

        risk_reward = (
            potential_profit / potential_loss
            if potential_loss > 0
            else 0
        )

        maximum_allowed_risk = (
            self.account_balance *
            self.max_risk_percent /
            100
        )

        return {
            "valid": True,
            "symbol": symbol.upper(),
            "signal": signal,
            "asset_class": spec["asset_class"],
            "entry": entry,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "lot_size": lot_size,
            "contract_size": contract_size,
            "stop_distance": round(
                stop_distance, 5
            ),
            "target_distance": round(
                target_distance, 5
            ),
            "potential_loss": round(
                potential_loss, 2
            ),
            "potential_profit": round(
                potential_profit, 2
            ),
            "risk_reward": round(
                risk_reward, 2
            ),
            "risk_amount": self.risk_amount(),
            "maximum_allowed_risk": round(
                maximum_allowed_risk, 2
            ),
            "risk_within_limit": (
                potential_loss <= maximum_allowed_risk
            )
        }


if __name__ == "__main__":

    print("===== NITRON RISK ENGINE V2 =====")

    risk = RiskEngine(
        account_balance=10000,
        risk_percent=1
    )

    print()
    print("===== POSITION SIZE =====")

    size = risk.position_size_for_risk(
        symbol="XAUUSD",
        entry=4000,
        stop_loss=3980
    )

    print(size)

    print()
    print("===== TRADE ANALYSIS =====")

    analysis = risk.analyze(
        symbol="XAUUSD",
        signal="BUY",
        entry=4000,
        stop_loss=3980,
        take_profit=4040,
        lot_size=0.05
    )

    print(analysis)
