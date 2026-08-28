from datetime import datetime


class NewsFilter:

    def __init__(self):
        self.events = [
            {
                "time": "14:30",
                "currency": "USD",
                "impact": "HIGH",
                "title": "Non-Farm Payrolls"
            },
            {
                "time": "15:00",
                "currency": "USD",
                "impact": "HIGH",
                "title": "FOMC Statement"
            }
        ]

    def get_events(self):
        return self.events

    def has_high_impact_news(self, currency):

        for event in self.events:
            if (
                event["currency"] == currency
                and event["impact"] == "HIGH"
            ):
                return True

        return False

    def can_trade(self, symbol):

        if "USD" in symbol:
            if self.has_high_impact_news("USD"):
                return {
                    "allowed": False,
                    "reason": "High-impact USD news detected."
                }

        return {
            "allowed": True,
            "reason": "No high-impact news."
        }

    def summary(self):

        return {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "events": self.events
        }


if __name__ == "__main__":

    news = NewsFilter()

    print(news.summary())
    print(news.can_trade("EURUSD"))
    print(news.can_trade("BTCUSD"))
