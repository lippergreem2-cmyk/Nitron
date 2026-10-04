"""
backtest.py
Backtests Nitron's entry rule (order block + liquidity sweep, matched
direction) with a proper stop-loss/take-profit exit, using historical
data via yfinance.
"""

import yfinance as yf
import pandas as pd

from indicators import compute_all_features
from trade_logger import TradeLogger

SYMBOL = "EURUSD=X"
PERIOD = "6mo"
INTERVAL = "1h"
WARMUP_BARS = 50

STOP_LOSS_PIPS = 20
TAKE_PROFIT_PIPS = 40
PIP_SIZE = 0.0001
MAX_HOLD_BARS = 24


def fetch_historical(symbol: str, period: str, interval: str) -> pd.DataFrame:
    data = yf.download(symbol, period=period, interval=interval, progress=False)
    if data.empty:
        raise ValueError(f"No data returned for {symbol} -- check ticker/period/interval.")
    data = data.rename(columns={
        "Open": "open", "High": "high", "Low": "low", "Close": "close"
    })
    return data[["open", "high", "low", "close"]].dropna()


def simulate_exit(df: pd.DataFrame, entry_idx: int, entry_price: float, direction: str):
    sl_distance = STOP_LOSS_PIPS * PIP_SIZE
    tp_distance = TAKE_PROFIT_PIPS * PIP_SIZE

    if direction == "buy":
        stop_price = entry_price - sl_distance
        target_price = entry_price + tp_distance
    else:
        stop_price = entry_price + sl_distance
        target_price = entry_price - tp_distance

    for offset in range(1, MAX_HOLD_BARS + 1):
        idx = entry_idx + offset
        if idx >= len(df):
            break
        bar = df.iloc[idx]

        if direction == "buy":
            if bar["low"] <= stop_price:
                return stop_price, "stop_loss", offset
            if bar["high"] >= target_price:
                return target_price, "take_profit", offset
        else:
            if bar["high"] >= stop_price:
                return stop_price, "stop_loss", offset
            if bar["low"] <= target_price:
                return target_price, "take_profit", offset

    last_idx = min(entry_idx + MAX_HOLD_BARS, len(df) - 1)
    return float(df["close"].iloc[last_idx]), "max_hold_exit", MAX_HOLD_BARS


def run_backtest():
    df = fetch_historical(SYMBOL, PERIOD, INTERVAL)
    print(f"Loaded {len(df)} bars for {SYMBOL}")

    logger = TradeLogger()
    trades_logged = 0

    for i in range(WARMUP_BARS, len(df) - MAX_HOLD_BARS):
        window = df.iloc[: i + 1]
        features = compute_all_features(window)

        if features["rsi"] is None:
            continue

        # Entry rule: order block AND liquidity sweep present, matching direction.
        ob, ls = features["order_block"], features["liquidity_sweep"]
        if ob != "none" and ls != "none" and ob == ls:
            entry_price = float(df["close"].iloc[i])
            direction = "buy" if ob == "bullish" else "sell"

            exit_price, reason, bars_held = simulate_exit(df, i, entry_price, direction)

            trade_id = logger.log_entry(
                symbol=SYMBOL,
                direction=direction,
                entry_price=entry_price,
                lot_size=0.1,
                features=features,
            )
            logger.log_exit(trade_id, exit_price=exit_price, reason=reason)
            trades_logged += 1

    print(f"\nBacktest complete. Logged {trades_logged} simulated trades.")
    print("Stats:", logger.stats())
    print("\nRun retrain.py next to train the model on this data.")


if __name__ == "__main__":
    run_backtest()
