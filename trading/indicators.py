"""
Nitron Technical Indicator Engine.

Works with candle dictionaries containing:
time, open, high, low, close, volume

This module performs analysis only.
It does not place trades.
"""


class TechnicalIndicators:

    def _closes(self, candles):
        return [float(c["close"]) for c in candles]

    def sma(self, candles, period=20):
        closes = self._closes(candles)

        if len(closes) < period:
            return None

        return round(sum(closes[-period:]) / period, 8)

    def ema(self, candles, period=20):
        closes = self._closes(candles)

        if len(closes) < period:
            return None

        multiplier = 2 / (period + 1)

        ema_value = sum(closes[:period]) / period

        for price in closes[period:]:
            ema_value = (
                (price - ema_value) * multiplier
            ) + ema_value

        return round(ema_value, 8)

    def rsi(self, candles, period=14):
        closes = self._closes(candles)

        if len(closes) <= period:
            return None

        changes = [
            closes[i] - closes[i - 1]
            for i in range(1, len(closes))
        ]

        gains = [max(change, 0) for change in changes]
        losses = [max(-change, 0) for change in changes]

        avg_gain = sum(gains[:period]) / period
        avg_loss = sum(losses[:period]) / period

        for i in range(period, len(changes)):
            avg_gain = (
                (avg_gain * (period - 1)) + gains[i]
            ) / period

            avg_loss = (
                (avg_loss * (period - 1)) + losses[i]
            ) / period

        if avg_loss == 0:
            return 100.0

        relative_strength = avg_gain / avg_loss

        value = 100 - (
            100 / (1 + relative_strength)
        )

        return round(value, 2)

    def atr(self, candles, period=14):
        if len(candles) <= period:
            return None

        true_ranges = []

        for i, candle in enumerate(candles):

            high = float(candle["high"])
            low = float(candle["low"])

            if i == 0:
                previous_close = float(candle["close"])
            else:
                previous_close = float(
                    candles[i - 1]["close"]
                )

            true_range = max(
                high - low,
                abs(high - previous_close),
                abs(low - previous_close)
            )

            true_ranges.append(true_range)

        atr_value = sum(
            true_ranges[:period]
        ) / period

        for true_range in true_ranges[period:]:
            atr_value = (
                (atr_value * (period - 1))
                + true_range
            ) / period

        return round(atr_value, 8)

    def candle_statistics(self, candles):
        if not candles:
            return None

        candle = candles[-1]

        open_price = float(candle["open"])
        high = float(candle["high"])
        low = float(candle["low"])
        close = float(candle["close"])

        body = abs(close - open_price)
        range_value = high - low

        if close > open_price:
            direction = "BULLISH"
        elif close < open_price:
            direction = "BEARISH"
        else:
            direction = "NEUTRAL"

        return {
            "time": candle["time"],
            "open": open_price,
            "high": high,
            "low": low,
            "close": close,
            "body": round(body, 8),
            "range": round(range_value, 8),
            "direction": direction
        }

    def analyze(self, candles):
        if not candles:
            return {
                "success": False,
                "message": "No candles supplied."
            }

        if len(candles) < 20:
            return {
                "success": False,
                "message": "At least 20 candles are required."
            }

        closes = self._closes(candles)

        result = {
            "success": True,
            "candles": len(candles),
            "current_price": round(closes[-1], 8),

            "sma_20": self.sma(candles, 20),
            "ema_20": self.ema(candles, 20),
            "rsi_14": self.rsi(candles, 14),
            "atr_14": self.atr(candles, 14),

            "candle": self.candle_statistics(candles)
        }

        # Basic relationship information.
        current = result["current_price"]
        sma = result["sma_20"]
        ema = result["ema_20"]

        if sma is not None and ema is not None:

            if current > sma and current > ema:
                result["trend_context"] = "ABOVE_AVERAGES"

            elif current < sma and current < ema:
                result["trend_context"] = "BELOW_AVERAGES"

            else:
                result["trend_context"] = "MIXED"

        else:
            result["trend_context"] = "UNKNOWN"

        return result


if __name__ == "__main__":

    import sys
    from pathlib import Path

    project_root = Path(__file__).resolve().parent.parent

    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    from mt5_data import get_candles

    print("===== NITRON TECHNICAL ENGINE TEST =====")

    candles = get_candles(
        "XAUUSD",
        timeframe="15min",
        bars=50
    )

    print("Candles:", len(candles))

    engine = TechnicalIndicators()

    result = engine.analyze(candles)

    print()
    print("===== TECHNICAL SNAPSHOT =====")

    for key, value in result.items():
        print(f"{key}: {value}")
