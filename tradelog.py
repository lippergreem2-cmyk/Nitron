import json, os, sqlite3, sys
from datetime import datetime, timezone

DB_PATH = os.path.expanduser("~/Nitron/data/trades.db")
SCHEMA = """
CREATE TABLE IF NOT EXISTS trades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    opened_at TEXT NOT NULL, symbol TEXT NOT NULL,
    direction TEXT NOT NULL CHECK (direction IN ('long','short')),
    setup TEXT NOT NULL, indicators TEXT,
    entry REAL NOT NULL, stop REAL NOT NULL, target REAL NOT NULL,
    mode TEXT NOT NULL DEFAULT 'demo', status TEXT NOT NULL DEFAULT 'open',
    closed_at TEXT, exit_price REAL, result_r REAL, outcome TEXT
);
"""

def _conn():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    c.executescript(SCHEMA)
    return c

def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")

def _r(direction, entry, stop, exit_price):
    risk = abs(entry - stop)
    if risk == 0:
        return 0.0
    move = exit_price - entry if direction == "long" else entry - exit_price
    return round(move / risk, 3)

def open_trade(symbol, direction, setup, entry, stop, target, indicators=None, mode="demo"):
    direction = direction.lower()
    if direction == "long" and not (stop < entry < target):
        raise ValueError("long needs stop < entry < target")
    if direction == "short" and not (target < entry < stop):
        raise ValueError("short needs target < entry < stop")
    with _conn() as c:
        cur = c.execute(
            "INSERT INTO trades (opened_at,symbol,direction,setup,indicators,entry,stop,target,mode)"
            " VALUES (?,?,?,?,?,?,?,?,?)",
            (_now(), symbol, direction, setup, json.dumps(indicators or {}), entry, stop, target, mode))
        return cur.lastrowid

def close_trade(trade_id, exit_price):
    with _conn() as c:
        t = c.execute("SELECT * FROM trades WHERE id=? AND status='open'", (trade_id,)).fetchone()
        if not t:
            return None
        r = _r(t["direction"], t["entry"], t["stop"], exit_price)
        outcome = "win" if r > 0 else "loss" if r < 0 else "breakeven"
        c.execute("UPDATE trades SET status='closed',closed_at=?,exit_price=?,result_r=?,outcome=? WHERE id=?",
                  (_now(), exit_price, r, outcome, trade_id))
        return {"id": trade_id, "result_r": r, "outcome": outcome}

def check_open(symbol, price):
    closed = []
    with _conn() as c:
        rows = c.execute("SELECT * FROM trades WHERE status='open' AND symbol=?", (symbol,)).fetchall()
    for t in rows:
        if t["direction"] == "long":
            hit = t["target"] if price >= t["target"] else t["stop"] if price <= t["stop"] else None
        else:
            hit = t["target"] if price <= t["target"] else t["stop"] if price >= t["stop"] else None
        if hit is not None:
            res = close_trade(t["id"], hit)
            if res:
                closed.append(res)
    return closed

def stats():
    with _conn() as c:
        rows = c.execute(
            "SELECT setup, COUNT(*) n, SUM(outcome='win') wins, ROUND(AVG(result_r),2) avg_r,"
            " ROUND(SUM(result_r),2) total_r FROM trades WHERE status='closed'"
            " GROUP BY setup ORDER BY total_r DESC").fetchall()
        o = c.execute(
            "SELECT 'ALL' setup, COUNT(*) n, SUM(outcome='win') wins, ROUND(AVG(result_r),2) avg_r,"
            " ROUND(SUM(result_r),2) total_r FROM trades WHERE status='closed'").fetchone()
    out = []
    for r in list(rows) + [o]:
        d = dict(r)
        d["win_rate"] = round(100 * (d["wins"] or 0) / d["n"], 1) if d["n"] else 0.0
        out.append(d)
    return out

def open_trades():
    with _conn() as c:
        return [dict(r) for r in c.execute(
            "SELECT id, symbol, direction, setup, entry, stop, target, mode"
            " FROM trades WHERE status='open' ORDER BY id")]


if __name__ == "__main__":
    print(f"{'setup':<16}{'n':>4}{'win%':>7}{'avgR':>7}{'totR':>8}")
    for r in stats():
        print(f"{r['setup']:<16}{r['n']:>4}{r['win_rate']:>7}{r['avg_r'] or 0:>7}{r['total_r'] or 0:>8}")
