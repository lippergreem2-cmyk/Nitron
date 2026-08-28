from decision_engine import DecisionEngine


class MarketScanner:

    def __init__(self):
        self.engine = DecisionEngine()

    def scan(self, analyses):

        opportunities = []

        for analysis in analyses:

            decision = self.engine.decide(analysis)

            if decision["action"] != "WAIT":

                opportunities.append({
                    "symbol": analysis["symbol"],
                    "signal": decision["action"],
                    "confidence": decision["confidence"],
                    "reason": decision["reason"]
                })

        opportunities.sort(
            key=lambda item: item["confidence"],
            reverse=True
        )

        return opportunities

    def best_trade(self, analyses):

        trades = self.scan(analyses)

        if not trades:
            return None

        return trades[0]


if __name__ == "__main__":

    scanner = MarketScanner()

    market = [
        {
            "symbol": "BTCUSD",
            "signal": "BUY",
            "confidence": 91
        },
        {
            "symbol": "XAUUSD",
            "signal": "SELL",
            "confidence": 83
        },
        {
            "symbol": "EURUSD",
            "signal": "BUY",
            "confidence": 72
        }
    ]

    print(scanner.scan(market))
    print(scanner.best_trade(market))
