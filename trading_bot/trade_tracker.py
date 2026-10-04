import json
import os
from datetime import datetime
import circuit_breaker

PAPER_STATE_FILE = "paper_state.json"


def _load_state():
    if os.path.exists(PAPER_STATE_FILE):
        with open(PAPER_STATE_FILE, "r") as f:
            return json.load(f)
    return {"balance": 0, "positions": [], "trade_log": []}


def _save_state(state):
    with open(PAPER_STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def check_and_close_positions(current_prices: dict, learner):
    state = _load_state()
    still_open = []

    for pos in state["positions"]:
        if pos["status"] != "OPEN":
            still_open.append(pos)
            continue

        symbol = pos["symbol"]
        price = current_prices.get(symbol)
        if price is None:
            still_open.append(pos)
            continue

        hit_tp = (price >= pos["take_profit"]) if pos["side"] == "BUY" else (price <= pos["take_profit"])
        hit_sl = (price <= pos["stop_loss"]) if pos["side"] == "BUY" else (price >= pos["stop_loss"])

        if hit_tp or hit_sl:
            won = hit_tp
            pnl_pct = ((price - pos["entry_price"]) / pos["entry_price"] * 100
                       if pos["side"] == "BUY"
                       else (pos["entry_price"] - price) / pos["entry_price"] * 100)

            pos["status"] = "WON" if won else "LOST"
            pos["close_price"] = price
            pos["closed_at"] = datetime.utcnow().isoformat()
            pos["pnl_pct"] = pnl_pct

            state["balance"] += state["balance"] * (pnl_pct / 100)

            if "features" in pos:
                learner.learn(pos["features"], won)

            circuit_breaker.update_and_check(state["balance"], last_trade_won=won)

            print(f"[CLOSED] {symbol} {pos['side']} -> {'WIN' if won else 'LOSS'} "
                  f"({pnl_pct:+.2f}%) | new balance: {state['balance']:.2f}")
        else:
            still_open.append(pos)

    state["positions"] = still_open
    _save_state(state)
