"""
Nitron Trading Bot - Configuration
Fill in your exchange API keys below, or set them as environment variables
(recommended, so keys never get committed to git):

    export EXCHANGE_API_KEY="your_key"
    export EXCHANGE_API_SECRET="your_secret"
"""

import os

# --- Exchange settings ---
EXCHANGE_ID = "binance"          # any exchange ccxt supports: binance, kraken, bybit, etc.
API_KEY = os.getenv("EXCHANGE_API_KEY", "")
API_SECRET = os.getenv("EXCHANGE_API_SECRET", "")

# --- Trading mode ---
PAPER_TRADING = True             # ALWAYS start True. Only flip to False once tested.

# --- Market settings ---
SYMBOLS = ["BTC/USDT", "ETH/USDT"]
TIMEFRAME = "15m"                # candle interval: 1m, 5m, 15m, 1h, 4h, 1d
CANDLE_LOOKBACK = 200             # how many candles to pull per check

# --- Strategy settings (EMA crossover example) ---
FAST_EMA = 12
SLOW_EMA = 26

# --- Risk management ---
RISK_PER_TRADE_PCT = 1.0         # % of account balance risked per trade
STOP_LOSS_PCT = 2.0              # stop loss distance from entry, in %
TAKE_PROFIT_PCT = 4.0            # take profit distance from entry, in %
MAX_OPEN_POSITIONS = 3

# --- Loop settings ---
CHECK_INTERVAL_SECONDS = 60      # how often the bot checks for signals

# --- Paper trading starting balance (used only if PAPER_TRADING = True) ---
PAPER_STARTING_BALANCE_USDT = 1000
