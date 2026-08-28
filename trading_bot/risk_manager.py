"""
Nitron Trading Bot - Risk Manager
Calculates position size and stop loss / take profit levels
so no single trade risks more than your configured %.
"""

import config


def calculate_position_size(balance, entry_price):
    """
    Position size (in base currency units) such that a stop-loss hit
    loses no more than RISK_PER_TRADE_PCT of the account balance.
    """
    risk_amount = balance * (config.RISK_PER_TRADE_PCT / 100)
    stop_distance = entry_price * (config.STOP_LOSS_PCT / 100)

    if stop_distance == 0:
        return 0

    position_size = risk_amount / stop_distance
    return position_size


def calculate_stop_loss(entry_price, side):
    if side == "BUY":
        return entry_price * (1 - config.STOP_LOSS_PCT / 100)
    else:  # SELL / short
        return entry_price * (1 + config.STOP_LOSS_PCT / 100)


def calculate_take_profit(entry_price, side):
    if side == "BUY":
        return entry_price * (1 + config.TAKE_PROFIT_PCT / 100)
    else:  # SELL / short
        return entry_price * (1 - config.TAKE_PROFIT_PCT / 100)
