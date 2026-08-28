# ==========================================
# NITRON CONFIGURATION
# ==========================================

import os

# API keys are loaded from environment variables.
# NEVER put real API keys directly in this file.
TWELVEDATA_API_KEY = os.getenv("TWELVEDATA_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

ASSETS = {
    "gold": "XAUUSD",
    "xauusd": "XAUUSD",
    "silver": "XAGUSD",
    "xagusd": "XAGUSD",
    "eurusd": "EURUSD",
    "gbpusd": "GBPUSD",
    "audusd": "AUDUSD",
    "nzdusd": "NZDUSD",
    "usdjpy": "USDJPY",
    "usdchf": "USDCHF",
    "usdcad": "USDCAD",

    "bitcoin": "BTCUSD",
    "btc": "BTCUSD",
    "ethereum": "ETHUSD",
    "eth": "ETHUSD",

    "apple": "AAPL",
    "tesla": "TSLA",
    "nvidia": "NVDA"
}

DEFAULT_TIMEFRAME = "15min"
DEFAULT_RISK_PERCENT = 1.0
DEFAULT_LOT_SIZE = 0.01

NITRON_NAME = "Nitron"
OWNER_NAME = "Boss Nimrod"

VOICE_ENABLED = True
AUTO_ANALYZE = True
AUTO_SAVE_TRADES = True
