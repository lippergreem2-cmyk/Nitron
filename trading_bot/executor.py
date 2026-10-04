import config
import json
import os
from datetime import datetime

PAPER_STATE_FILE = "paper_state.json"


def _load_paper_state():
    if os.path.exists(PAPER_STATE_FILE):
        with open(PAPER_STATE_FILE, "r") as f:
            return json.load(f)
    return {"balance": config.PAPER_STARTING_BALANCE_USDT, "positions": [], "trade_log": []}


def _save_paper_state(state):
    with open(PAPER_STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def place_order(exchange, symbol, side, amount, entry_price, stop_loss, take_profit, features=None):
    if config.PAPER_TRADING:
        state = _load_paper_state()
        trade = {
            "symbol": symbol,
            "side": side,
            "amount": amount,
            "entry_price": entry_price,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "timestamp": datetime.utcnow().isoformat(),
            "status": "OPEN",
            "features": features or {},
        }
        state["positions"].append(trade)
        state["trade_log"].append(trade)
        _save_paper_state(state)
        print(f"[PAPER] {side} {amount:.6f} {symbol} @ {entry_price:.2f} "
              f"(SL {stop_loss:.2f} / TP {take_profit:.2f})")
        return trade
    else:
        order_side = "buy" if side == "BUY" else "sell"
        order = exchange.create_market_order(symbol, order_side, amount)
        print(f"[LIVE] {side} order placed: {order}")
        return order


def get_paper_balance():
    state = _load_paper_state()
    return state["balance"]


def get_open_positions():
    state = _load_paper_state()
    return [p for p in state["positions"] if p["status"] == "OPEN"]
