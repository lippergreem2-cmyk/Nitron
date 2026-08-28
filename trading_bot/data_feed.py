"""
Nitron Trading Bot - Data Feed
Wraps ccxt to fetch live market data.
"""

import ccxt
import pandas as pd
import config


def get_exchange():
    """Create and return a ccxt exchange instance."""
    exchange_class = getattr(ccxt, config.EXCHANGE_ID)
    exchange = exchange_class({
        "apiKey": config.API_KEY,
        "secret": config.API_SECRET,
        "enableRateLimit": True,
    })
    return exchange


def fetch_candles(exchange, symbol, timeframe=None, limit=None):
    """
    Fetch OHLCV candles and return as a pandas DataFrame with columns:
    timestamp, open, high, low, close, volume
    """
    timeframe = timeframe or config.TIMEFRAME
    limit = limit or config.CANDLE_LOOKBACK

    raw = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(raw, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df


def get_latest_price(exchange, symbol):
    """Fetch the current market price for a symbol."""
    ticker = exchange.fetch_ticker(symbol)
    return ticker["last"]


def get_account_balance(exchange, quote_currency="USDT"):
    """Fetch available balance for a given quote currency (live trading only)."""
    balance = exchange.fetch_balance()
    return balance.get("free", {}).get(quote_currency, 0)
