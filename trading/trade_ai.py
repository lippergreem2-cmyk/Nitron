from strategy import Strategy
from risk import RiskManager
from executor import TradeExecutor
from journal import TradeJournal
from learning import LearningEngine
from news_filter import NewsFilter
from alerts import AlertManager


class TradeAI:

    def __init__(self):

        self.strategy = Strategy()
        self.risk = RiskManager()
        self.executor = TradeExecutor()
        self.journal = TradeJournal()
        self.learning = LearningEngine()
        self.news = NewsFilter()
        self.alerts = AlertManager()

    def analyze(self, market):

        signal = self.strategy.generate_signal(market)

        if signal is None:
            return {
                "success": False,
                "message": "No trade signal."
            }

        return signal

    def execute(self, signal):

        news = self.news.can_trade(signal["symbol"])

        if not news["allowed"]:
            return {
                "success": False,
                "message": news["reason"]
            }

        valid, message = self.executor.validate(signal)

        if not valid:
            return {
                "success": False,
                "message": message
            }

        result = self.executor.prepare(signal)

        if result["success"]:

            self.journal.save_trade(result["trade"])

            self.alerts.signal_alert(
                signal["symbol"],
                signal["signal"],
                signal["confidence"]
            )

        return result

    def performance(self):

        return self.learning.statistics()


if __name__ == "__main__":

    ai = TradeAI()

    sample = {
        "symbol": "BTCUSD",
        "price": 115000
    }

    signal = ai.analyze(sample)

    print(signal)

    if signal.get("success", True):
        print(ai.execute(signal))

    print(ai.performance())
