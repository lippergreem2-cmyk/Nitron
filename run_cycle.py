"""
run_cycle.py
The main loop that ties everything together:

  1. Check if the market is open (market_hours.py)
  2. Fetch latest OHLC data (YOU need to plug in your MT5 data source below)
  3. Compute indicator features (indicators.py)
  4. Score the setup with the trained model (retrain.py)
  5. If confident enough, log the trade (trade_logger.py)

This is a decision-support scaffold, not an auto-executor. It tells you
(or a downstream execution module) what it thinks, and logs what happened
so retrain.py has data to learn from. Wiring actual order placement into
MT5 is a separate step -- do that deliberately once you trust the scoring.
"""

import time
import pandas as pd

from market_hours import market_status
from indicators import compute_all_features
from trade_logger import TradeLogger
from retrain import score_setup, MODEL_PATH

SYMBOL = "EURUSD"
WIN_PROB_THRESHOLD = 0.60   # only flag setups the model scores above this
LOT_SIZE = 0.1
POLL_SECONDS = 300           # how often to check (5 min default)


def fetch_ohlc(symbol: str) -> pd.DataFrame:
    """
    PLACEHOLDER -- replace this with your actual MT5 data pull.
    Must return a DataFrame with columns: open, high, low, close,
    most recent candle last, at least ~50 rows for indicators to warm up.

    Example with MetaTrader5 package:
        import MetaTrader5 as mt5
        rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M15, 0, 100)
        return pd.DataFrame(rates)[["open", "high", "low", "close"]]
    """
    raise NotImplementedError("Plug in your MT5 data fetch here.")


def run_once():
    status = market_status()
    print(f"\n[{status['time_et']}] market_open={status['market_open']} "
          f"sessions={status['active_sessions']} overlaps={status['overlaps']}")

    if not status["market_open"]:
        print("Market closed -- skipping this cycle.")
        return

    try:
        df = fetch_ohlc(SYMBOL)
    except NotImplementedError as e:
        print(f"[!] {e}")
        return

    features = compute_all_features(df)
    print(f"Features: {features}")

    if not MODEL_PATH.exists():
        print("[!] No trained model yet -- run retrain.py after logging some trades.")
        return

    win_prob = score_setup(features)
    print(f"Model win probability: {win_prob:.3f}")

    if win_prob >= WIN_PROB_THRESHOLD:
        print(f"[SIGNAL] Setup scores {win_prob:.3f} >= {WIN_PROB_THRESHOLD} threshold.")
        # This only LOGS the intent -- it does not place a live order.
        # Wire real MT5 order execution here once you're ready, then call
        # logger.log_entry(...) with the actual fill price.
        #
        # logger = TradeLogger()
        # entry_price = df["close"].iloc[-1]
        # trade_id = logger.log_entry(
        #     symbol=SYMBOL, direction="buy", entry_price=entry_price,
        #     lot_size=LOT_SIZE, features=features,
        # )
        # print(f"Logged trade_id={trade_id}")
    else:
        print("No signal this cycle.")


def run_loop():
    print(f"Starting Nitron cycle loop -- polling every {POLL_SECONDS}s. Ctrl+C to stop.")
    while True:
        try:
            run_once()
        except Exception as e:
            print(f"[ERROR] {e}")
        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    run_once()  # single run by default; call run_loop() for continuous polling
