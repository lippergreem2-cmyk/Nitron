class DecisionEngine:

    def __init__(self):
        self.minimum_confidence = 80

    def decide(self, analysis):

        score = analysis["confidence"]

        if score >= self.minimum_confidence:

            return {
                "action": analysis["signal"],
                "confidence": score,
                "reason": "Confidence above minimum threshold."
            }

        return {
            "action": "WAIT",
            "confidence": score,
            "reason": "Confidence below minimum threshold."
        }

    def explain(self, analysis):

        explanation = []

        if analysis.get("trend") == "UPTREND":
            explanation.append("Bullish trend")

        if analysis.get("trend") == "DOWNTREND":
            explanation.append("Bearish trend")

        if analysis.get("rsi", 50) < 30:
            explanation.append("RSI is oversold")

        if analysis.get("rsi", 50) > 70:
            explanation.append("RSI is overbought")

        if analysis.get("macd") == "BULLISH":
            explanation.append("MACD bullish crossover")

        if analysis.get("macd") == "BEARISH":
            explanation.append("MACD bearish crossover")

        if analysis.get("adx", 0) > 25:
            explanation.append("Strong trend")

        return explanation


if __name__ == "__main__":

    engine = DecisionEngine()

    analysis = {
        "signal": "BUY",
        "confidence": 91,
        "trend": "UPTREND",
        "rsi": 27,
        "macd": "BULLISH",
        "adx": 34
    }

    print(engine.decide(analysis))
    print(engine.explain(analysis))
