"""
Nitron Strategy Engine.

Combines:
- Technical indicators
- Market structure
- Price action

Analysis only.
No trade execution.
"""

try:
    from .indicators import TechnicalIndicators
    from .market_structure import MarketStructure
except ImportError:
    from indicators import TechnicalIndicators
    from market_structure import MarketStructure


class StrategyEngine:

    def __init__(self):
        self.indicators = TechnicalIndicators()
        self.structure = MarketStructure()

    def _score(self, technical, structure):
        buy_score = 0
        sell_score = 0
        reasons = []

        # Moving-average context
        trend = technical.get("trend_context")

        if trend == "ABOVE_AVERAGES":
            buy_score += 1
            reasons.append("Price is above SMA20 and EMA20.")

        elif trend == "BELOW_AVERAGES":
            sell_score += 1
            reasons.append("Price is below SMA20 and EMA20.")

        # RSI
        rsi = technical.get("rsi_14")

        if rsi is not None:
            if 50 < rsi < 70:
                buy_score += 1
                reasons.append("RSI shows positive momentum.")

            elif 30 < rsi < 50:
                sell_score += 1
                reasons.append("RSI shows negative momentum.")

            elif rsi >= 70:
                reasons.append("RSI is elevated; bullish momentum may be extended.")

            elif rsi <= 30:
                reasons.append("RSI is depressed; bearish momentum may be extended.")

        # Candle direction
        candle = technical.get("candle", {})
        direction = candle.get("direction")

        if direction == "BULLISH":
            buy_score += 1
            reasons.append("Latest candle is bullish.")

        elif direction == "BEARISH":
            sell_score += 1
            reasons.append("Latest candle is bearish.")

        # Market structure
        market_structure = structure.get("structure")

        if market_structure == "BULLISH":
            buy_score += 2
            reasons.append("Market structure is bullish.")

        elif market_structure == "BEARISH":
            sell_score += 2
            reasons.append("Market structure is bearish.")

        elif market_structure == "BULLISH_BIAS":
            buy_score += 1
            reasons.append("Market structure has a bullish bias.")

        elif market_structure == "BEARISH_BIAS":
            sell_score += 1
            reasons.append("Market structure has a bearish bias.")

        else:
            reasons.append("Market structure is neutral.")

        return buy_score, sell_score, reasons

    def generate_signal(self, technical, structure):
        buy_score, sell_score, reasons = self._score(
            technical,
            structure
        )

        difference = abs(buy_score - sell_score)

        # Require multiple aligned factors.
        if buy_score >= 3 and buy_score > sell_score:
            signal = "BUY"

        elif sell_score >= 3 and sell_score > buy_score:
            signal = "SELL"

        else:
            signal = "WAIT"

        total_score = max(buy_score, sell_score)

        if signal == "WAIT":
            confidence = 0
        else:
            confidence = min(
                95,
                50 + (difference * 10)
            )

        return {
            "signal": signal,
            "buy_score": buy_score,
            "sell_score": sell_score,
            "confidence": confidence,
            "reasons": reasons
        }

    def analyze(self, candles):
        if not candles:
            return {
                "success": False,
                "message": "No candles supplied."
            }

        technical = self.indicators.analyze(candles)
        structure = self.structure.analyze(candles)

        if not technical.get("success"):
            return technical

        if not structure.get("success"):
            return structure

        signal = self.generate_signal(
            technical,
            structure
        )

        current_price = technical.get("current_price")
        atr = technical.get("atr_14")

        result = {
            "success": True,
            "symbol": None,
            "timeframe": None,
            "current_price": current_price,
            "signal": signal["signal"],
            "confidence": signal["confidence"],
            "buy_score": signal["buy_score"],
            "sell_score": signal["sell_score"],
            "reasons": signal["reasons"],
            "technical": technical,
            "market_structure": structure
        }

        # Reference levels only.
        # These are analytical levels, not guaranteed execution prices.
        if current_price is not None and atr is not None:
            if signal["signal"] == "BUY":
                result["reference_stop"] = round(
                    current_price - (atr * 2),
                    8
                )
                result["reference_target"] = round(
                    current_price + (atr * 4),
                    8
                )

            elif signal["signal"] == "SELL":
                result["reference_stop"] = round(
                    current_price + (atr * 2),
                    8
                )
                result["reference_target"] = round(
                    current_price - (atr * 4),
                    8
                )

        return result


if __name__ == "__main__":

    import sys
    from pathlib import Path

    project_root = Path(__file__).resolve().parent.parent

    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    from mt5_data import get_candles

    print("===== NITRON STRATEGY ENGINE TEST =====")

    candles = get_candles(
        "XAUUSD",
        timeframe="15min",
        bars=50
    )

    print("Candles:", len(candles))

    engine = StrategyEngine()

    result = engine.analyze(candles)

    print()
    print("===== STRATEGY SNAPSHOT =====")

    print("Signal:", result.get("signal"))
    print("Confidence:", result.get("confidence"))
    print("Buy score:", result.get("buy_score"))
    print("Sell score:", result.get("sell_score"))
    print("Current price:", result.get("current_price"))

    print()
    print("Reasons:")

    for reason in result.get("reasons", []):
        print("-", reason)

    if "reference_stop" in result:
        print()
        print("Reference stop:", result["reference_stop"])
        print("Reference target:", result["reference_target"])

    print()
    print("Market structure:",
          result.get("market_structure", {}).get("structure"))
