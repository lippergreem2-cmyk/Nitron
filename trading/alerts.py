from datetime import datetime


class AlertManager:

    def __init__(self):
        self.alerts = []

    def create(
        self,
        title,
        message,
        level="INFO"
    ):

        alert = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "title": title,
            "message": message,
            "level": level
        }

        self.alerts.append(alert)

        return alert

    def signal_alert(
        self,
        symbol,
        signal,
        confidence
    ):

        return self.create(
            title="Trading Signal",
            message=(
                f"{signal} signal detected on "
                f"{symbol} "
                f"({confidence}% confidence)"
            ),
            level="SIGNAL"
        )

    def tp_alert(
        self,
        symbol,
        profit
    ):

        return self.create(
            title="Take Profit",
            message=(
                f"{symbol} reached Take Profit. "
                f"Profit: {profit}"
            ),
            level="SUCCESS"
        )

    def sl_alert(
        self,
        symbol,
        loss
    ):

        return self.create(
            title="Stop Loss",
            message=(
                f"{symbol} reached Stop Loss. "
                f"Loss: {loss}"
            ),
            level="WARNING"
        )

    def news_alert(
        self,
        event
    ):

        return self.create(
            title="High Impact News",
            message=event,
            level="NEWS"
        )

    def get_alerts(self):

        return self.alerts

    def clear(self):

        self.alerts.clear()


if __name__ == "__main__":

    alerts = AlertManager()

    alerts.signal_alert(
        "BTCUSD",
        "BUY",
        91
    )

    alerts.tp_alert(
        "BTCUSD",
        145.75
    )

    alerts.news_alert(
        "High-impact USD news in 15 minutes."
    )

    for alert in alerts.get_alerts():
        print(alert)
