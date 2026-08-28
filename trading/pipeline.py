from market_scanner import MarketScanner
from risk import RiskManager
from news_filter import NewsFilter
from executor import TradeExecutor
from journal import TradeJournal
from alerts import AlertManager


class TradingPipeline:

    def __init__(self):

        self.scanner = MarketScanner()
        self.risk = RiskManager()
        self.news = NewsFilter()
        self.executor = TradeExecutor()
        self.journal = TradeJournal()
        self.alerts = AlertManager()

    def run(self, analyses):

        opportunities = self.scanner.scan(analyses)

        if not opportunities:
            return {
                "success": False,
                "message": "No trading opportunities."
            }

        trade = opportunities[0]

        news = self.news.can_trade(
            trade["symbol"]
        )

        if not news["allowed"]:
            return {
                "success": False,
                "message": news["reason"]
            }

        order = {
            "symbol": trade["symbol"],
            "signal": trade["signal"],
            "entry": 0,
            "stop_loss": 0,
            "take_profit": 0,
            "lot_size": 0.01,
            "confidence": trade["confidence"]
        }

        valid, message = self.executor.validate(order)

        if not valid:
            return {
                "success": False,
                "message": message
            }

        result = self.executor.prepare(order)

        if result["success"]:

            self.journal.save_trade(result["trade"])

            self.alerts.signal_alert(
                trade["symbol"],
                trade["signal"],
                trade["confidence"]
            )

        return result


if __name__ == "__main__":

    pipeline = TradingPipeline()

    market = [
        {
            "symbol": "BTCUSD",
            "signal": "BUY",
            "confidence": 91
        },
        {
            "symbol": "XAUUSD",
            "signal": "SELL",
            "confidence": 84
        }
    ]

    print(pipeline.run(market))
