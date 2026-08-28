# risk.py
# Nitron Risk Manager v1.0

class RiskManager:

    def __init__(
        self,
        account_balance=10000,
        risk_percent=2,
        reward_ratio=2
    ):

        self.account_balance = account_balance
        self.risk_percent = risk_percent
        self.reward_ratio = reward_ratio


    def risk_amount(self):

        return self.account_balance * (
            self.risk_percent / 100
        )


    def calculate(
        self,
        entry,
        direction,
        stop_distance
    ):

        risk_money = self.risk_amount()


        if direction == "BUY":

            stop_loss = entry - stop_distance

            take_profit = (
                entry +
                (stop_distance * self.reward_ratio)
            )


        elif direction == "SELL":

            stop_loss = entry + stop_distance

            take_profit = (
                entry -
                (stop_distance * self.reward_ratio)
            )


        else:

            return None



        lot = self.lot_size(
            stop_distance
        )


        return {

            "entry": round(entry, 5),

            "stop_loss":
                round(stop_loss, 5),

            "take_profit":
                round(take_profit, 5),

            "lot_size":
                lot,

            "risk_money":
                round(risk_money, 2),

            "risk_reward":
                f"1:{self.reward_ratio}"

        }



    def lot_size(
        self,
        stop_distance,
        pip_value=10
    ):

        if stop_distance <= 0:

            return 0


        risk = self.risk_amount()


        lots = risk / (
            stop_distance *
            pip_value
        )


        return round(lots, 2)



if __name__ == "__main__":

    manager = RiskManager(
        account_balance=1000,
        risk_percent=2
    )


    print(
        manager.calculate(
            2500,
            "BUY",
            20
        )
    )
