import config


def calculate_position_size(balance, entry_price):
    risk_amount = balance * (config.RISK_PER_TRADE_PCT / 100)
    stop_distance = entry_price * (config.STOP_LOSS_PCT / 100)
    if stop_distance == 0:
        return 0
    return risk_amount / stop_distance


def calculate_stop_loss(entry_price, side):
    if side == "BUY":
        return entry_price * (1 - config.STOP_LOSS_PCT / 100)
    return entry_price * (1 + config.STOP_LOSS_PCT / 100)


def calculate_take_profit(entry_price, side):
    if side == "BUY":
        return entry_price * (1 + config.TAKE_PROFIT_PCT / 100)
    return entry_price * (1 - config.TAKE_PROFIT_PCT / 100)
