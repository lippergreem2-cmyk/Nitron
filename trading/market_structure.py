"""
Nitron Market Structure Engine.

Analyzes price structure from OHLC candles.

Analysis only.
No trade execution.
"""


class MarketStructure:

    def __init__(self, swing_window=2):
        self.swing_window = int(swing_window)

    def _is_swing_high(self, candles, index):
        window = self.swing_window

        if index < window:
            return False

        if index + window >= len(candles):
            return False

        high = float(candles[index]["high"])

        for i in range(index - window, index + window + 1):
            if i == index:
                continue

            if float(candles[i]["high"]) >= high:
                return False

        return True

    def _is_swing_low(self, candles, index):
        window = self.swing_window

        if index < window:
            return False

        if index + window >= len(candles):
            return False

        low = float(candles[index]["low"])

        for i in range(index - window, index + window + 1):
            if i == index:
                continue

            if float(candles[i]["low"]) <= low:
                return False

        return True

    def find_swings(self, candles):
        swing_highs = []
        swing_lows = []

        for i in range(len(candles)):

            if self._is_swing_high(candles, i):
                swing_highs.append({
                    "index": i,
                    "time": candles[i]["time"],
                    "price": float(candles[i]["high"])
                })

            if self._is_swing_low(candles, i):
                swing_lows.append({
                    "index": i,
                    "time": candles[i]["time"],
                    "price": float(candles[i]["low"])
                })

        return {
            "highs": swing_highs,
            "lows": swing_lows
        }

    def classify_structure(self, swings):
        highs = swings["highs"]
        lows = swings["lows"]

        higher_high = False
        lower_high = False
        higher_low = False
        lower_low = False

        if len(highs) >= 2:
            previous_high = highs[-2]["price"]
            latest_high = highs[-1]["price"]

            higher_high = latest_high > previous_high
            lower_high = latest_high < previous_high

        if len(lows) >= 2:
            previous_low = lows[-2]["price"]
            latest_low = lows[-1]["price"]

            higher_low = latest_low > previous_low
            lower_low = latest_low < previous_low

        if higher_high and higher_low:
            structure = "BULLISH"

        elif lower_high and lower_low:
            structure = "BEARISH"

        elif higher_high or higher_low:
            structure = "BULLISH_BIAS"

        elif lower_high or lower_low:
            structure = "BEARISH_BIAS"

        else:
            structure = "NEUTRAL"

        return {
            "structure": structure,
            "higher_high": higher_high,
            "lower_high": lower_high,
            "higher_low": higher_low,
            "lower_low": lower_low
        }

    def analyze(self, candles):
        if not candles:
            return {
                "success": False,
                "message": "No candles supplied."
            }

        if len(candles) < 10:
            return {
                "success": False,
                "message": "At least 10 candles are required."
            }

        swings = self.find_swings(candles)
        classification = self.classify_structure(swings)

        latest_high = (
            swings["highs"][-1]
            if swings["highs"]
            else None
        )

        latest_low = (
            swings["lows"][-1]
            if swings["lows"]
            else None
        )

        return {
            "success": True,
            "candles": len(candles),
            "swing_high_count": len(swings["highs"]),
            "swing_low_count": len(swings["lows"]),
            "latest_swing_high": latest_high,
            "latest_swing_low": latest_low,
            **classification
        }


if __name__ == "__main__":

    import sys
    from pathlib import Path

    project_root = Path(__file__).resolve().parent.parent

    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    from mt5_data import get_candles

    print("===== NITRON MARKET STRUCTURE TEST =====")

    candles = get_candles(
        "XAUUSD",
        timeframe="15min",
        bars=50
    )

    print("Candles:", len(candles))

    engine = MarketStructure()

    result = engine.analyze(candles)

    print()
    print("===== STRUCTURE SNAPSHOT =====")

    for key, value in result.items():
        print(f"{key}: {value}")
