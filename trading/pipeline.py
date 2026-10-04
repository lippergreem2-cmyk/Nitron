"""
Nitron Trading Pipeline V2.

Connects:
Market Data -> Technical Engine -> Market Structure
-> Strategy -> Risk Engine

Analysis only by default.
No automatic trade execution.
"""

# Support both:
#   python trading/pipeline.py
#   python -m trading.pipeline

import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_TRADING_DIR = Path(__file__).resolve().parent

# Put the trading module directory FIRST.
# This prevents conflicts with top-level packages such as
# ~/Nitron/indicators/.
if str(_TRADING_DIR) in sys.path:
    sys.path.remove(str(_TRADING_DIR))

sys.path.insert(0, str(_TRADING_DIR))

if str(_PROJECT_ROOT) in sys.path:
    sys.path.remove(str(_PROJECT_ROOT))

sys.path.insert(1, str(_PROJECT_ROOT))

try:
    from .market_data import MarketData
    from .indicators import TechnicalIndicators
    from .market_structure import MarketStructure
    from .strategy import StrategyEngine
    from .risk import RiskEngine
except ImportError:
    from market_data import MarketData
    from indicators import TechnicalIndicators
    from market_structure import MarketStructure
    from strategy import StrategyEngine
    from risk import RiskEngine



class TradingPipeline:

    def __init__(
        self,
        account_balance=10000.0,
        risk_percent=1.0
    ):
        self.market = MarketData()
        self.indicators = TechnicalIndicators()
        self.structure = MarketStructure()
        self.strategy = StrategyEngine()

        self.account_balance = float(account_balance)
        self.risk_percent = float(risk_percent)

        self.risk = RiskEngine(
            account_balance=self.account_balance,
            risk_percent=self.risk_percent
        )

    def analyze(
        self,
        symbol="XAUUSD",
        timeframe="15min",
        bars=50
    ):
        symbol = str(symbol).upper().strip()

        candles = self._get_candles(
            symbol,
            timeframe,
            bars
        )

        if not candles:
            return {
                "success": False,
                "symbol": symbol,
                "message": "No market candles available."
            }

        technical = self.indicators.analyze(candles)

        if not technical.get("success"):
            return technical

        structure = self.structure.analyze(candles)

        if not structure.get("success"):
            return structure

        strategy = self.strategy.generate_signal(
            technical,
            structure
        )

        current_price = technical.get("current_price")
        atr = technical.get("atr_14")

        result = {
            "success": True,
            "symbol": symbol,
            "timeframe": timeframe,
            "candles": len(candles),
            "current_price": current_price,
            "signal": strategy["signal"],
            "confidence": strategy["confidence"],
            "buy_score": strategy["buy_score"],
            "sell_score": strategy["sell_score"],
            "reasons": strategy["reasons"],
            "market_structure":
                structure["structure"],
            "technical": technical,
            "structure": structure
        }

        # Only calculate analytical risk levels
        # when the strategy produces a directional signal.
        if (
            strategy["signal"] in ("BUY", "SELL")
            and current_price is not None
            and atr is not None
            and atr > 0
        ):

            if strategy["signal"] == "BUY":
                stop_loss = current_price - (atr * 2)
                take_profit = current_price + (atr * 4)

            else:
                stop_loss = current_price + (atr * 2)
                take_profit = current_price - (atr * 4)

            risk = self.risk.position_size_for_risk(
                symbol=symbol,
                entry=current_price,
                stop_loss=stop_loss,
                risk_percent=self.risk_percent
            )

            if risk.get("valid"):

                lot_size = risk["suggested_lot_size"]

                risk_analysis = self.risk.analyze(
                    symbol=symbol,
                    signal=strategy["signal"],
                    entry=current_price,
                    stop_loss=stop_loss,
                    take_profit=take_profit,
                    lot_size=lot_size
                )

                result["reference_stop"] = round(
                    stop_loss,
                    8
                )

                result["reference_target"] = round(
                    take_profit,
                    8
                )

                result["risk"] = risk_analysis

        return result

    def _get_candles(
        self,
        symbol,
        timeframe,
        bars
    ):
        from mt5_data import get_candles

        return get_candles(
            symbol,
            timeframe=timeframe,
            bars=bars
        )


if __name__ == "__main__":

    import sys
    from pathlib import Path

    project_root = Path(__file__).resolve().parent.parent

    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    print("===== NITRON TRADING PIPELINE V2 =====")

    pipeline = TradingPipeline(
        account_balance=10000,
        risk_percent=1.0
    )

    result = pipeline.analyze(
        symbol="XAUUSD",
        timeframe="15min",
        bars=50
    )

    print()
    print("===== LIVE ANALYSIS =====")

    print("Success:", result.get("success"))
    print("Symbol:", result.get("symbol"))
    print("Timeframe:", result.get("timeframe"))
    print("Candles:", result.get("candles"))
    print("Current price:", result.get("current_price"))
    print("Signal:", result.get("signal"))
    print("Confidence:", result.get("confidence"))
    print("Buy score:", result.get("buy_score"))
    print("Sell score:", result.get("sell_score"))
    print("Market structure:",
          result.get("market_structure"))

    print()
    print("Reasons:")

    for reason in result.get("reasons", []):
        print("-", reason)

    if "reference_stop" in result:
        print()
        print("Reference stop:",
              result["reference_stop"])

        print("Reference target:",
              result["reference_target"])

    if "risk" in result:
        print()
        print("===== RISK =====")
        print(result["risk"])
