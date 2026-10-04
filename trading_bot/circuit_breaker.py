import json
import os

STATE_FILE = "circuit_breaker_state.json"

MAX_DRAWDOWN_PCT = 10.0
MAX_CONSECUTIVE_LOSSES = 5


def _load():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {"peak_balance": 0, "consecutive_losses": 0, "halted": False, "halt_reason": None}


def _save(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def update_and_check(current_balance, last_trade_won=None):
    state = _load()

    if current_balance > state["peak_balance"]:
        state["peak_balance"] = current_balance

    if last_trade_won is not None:
        state["consecutive_losses"] = 0 if last_trade_won else state["consecutive_losses"] + 1

    if state["peak_balance"] > 0:
        drawdown_pct = (state["peak_balance"] - current_balance) / state["peak_balance"] * 100
    else:
        drawdown_pct = 0

    if not state["halted"]:
        if drawdown_pct >= MAX_DRAWDOWN_PCT:
            state["halted"] = True
            state["halt_reason"] = f"Drawdown hit {drawdown_pct:.1f}% (limit {MAX_DRAWDOWN_PCT}%)"
        elif state["consecutive_losses"] >= MAX_CONSECUTIVE_LOSSES:
            state["halted"] = True
            state["halt_reason"] = f"{state['consecutive_losses']} consecutive losses (limit {MAX_CONSECUTIVE_LOSSES})"

    _save(state)
    return state["halted"], state["halt_reason"]


def reset():
    state = _load()
    state["halted"] = False
    state["halt_reason"] = None
    state["consecutive_losses"] = 0
    _save(state)
    print("Circuit breaker reset. Trading can resume.")
