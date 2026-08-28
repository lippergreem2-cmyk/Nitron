import MetaTrader5 as mt5


class MT5Trader:

    def __init__(self):
        self.connected = False

    def connect(self):

        if mt5.initialize():
            self.connected = True
            return True

        print("Failed to connect:", mt5.last_error())
        return False

    def disconnect(self):
        mt5.shutdown()
        self.connected = False

    def account_info(self):

        if not self.connected:
            return None

        info = mt5.account_info()

        if info is None:
            return None

        return {
            "login": info.login,
            "server": info.server,
            "name": info.name,
            "balance": info.balance,
            "equity": info.equity,
            "margin": info.margin,
            "profit": info.profit
        }

    def price(self, symbol):

        tick = mt5.symbol_info_tick(symbol)

        if tick is None:
            return None

        return {
            "bid": tick.bid,
            "ask": tick.ask,
            "spread": tick.ask - tick.bid
        }

    def buy(self, symbol, lot):

        price = mt5.symbol_info_tick(symbol).ask

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": mt5.ORDER_TYPE_BUY,
            "price": price,
            "deviation": 20,
            "magic": 123456,
            "comment": "Nitron Buy",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        return mt5.order_send(request)

    def sell(self, symbol, lot):

        price = mt5.symbol_info_tick(symbol).bid

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": mt5.ORDER_TYPE_SELL,
            "price": price,
            "deviation": 20,
            "magic": 123456,
            "comment": "Nitron Sell",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        return mt5.order_send(request)


if __name__ == "__main__":

    trader = MT5Trader()

    if trader.connect():

        print("Connected to MT5")

        print(trader.account_info())

        print(trader.price("XAUUSD"))

        trader.disconnect()
