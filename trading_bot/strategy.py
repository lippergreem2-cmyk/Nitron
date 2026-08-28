"""
Nitron Trading Bot - Strategy
Simple EMA crossover strategy. Swap this out with your own logic
(RSI, MACD, order blocks, liquidity sweeps, etc) — the rest of the
bot doesn't care how the signal is generated, only what it returns.

Signal returned is one of: "BUY", "SELL", "HOLD"
"""

import config


def add_indicators(df):
    """Add EMA columns to the candle DataFrame."""
    df["ema_fast"] = df["close"].ewm(span=config.FAST_EMA, adjust=False).mean()
    df["ema_slow"] = df["close"].ewm(span=config.SLOW_EMA, adjust=False).mean()
    return df


def generate_signal(df):
    """
    Look at the last two candles and detect a crossover:
    - fast EMA crosses above slow EMA  -> BUY
    - fast EMA crosses below slow EMA  -> SELL
    - otherwise                        -> HOLD
    """
    df = add_indicators(df)

    if len(df) < 2:
        return "HOLD"

    prev = df.iloc[-2]
    curr = df.iloc[-1]

    crossed_up = prev["ema_fast"] <= prev["ema_slow"] and curr["ema_fast"] > curr["ema_slow"]
    crossed_down = prev["ema_fast"] >= prev["ema_slow"] and curr["ema_fast"] < curr["ema_slow"]

    if crossed_up:
        return "BUY"
    if crossed_down:
        return "SELL"
    return "HOLD"
