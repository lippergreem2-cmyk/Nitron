"""
Nitron Market Data

Uses the existing Twelve Data integration in mt5_data.py.

Market-data only. No trade execution.
"""

import sys
from pathlib import Path
from datetime import datetime

# Allow this file to work when executed as:
# python trading/market_data.py
PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from mt5_data import get_current_price, get_candles

try:
    from .instrument_specs import get_instrument
except ImportError:
    from instrument_specs import get_instrument


class MarketData:

    def __init__(self):
        self.supported_symbols = [
            "BTCUSD",
            "XAUUSD",
            "EURUSD",
            "GBPUSD",
            "USDJPY",
        ]

    def _validate_symbol(self, symbol):
        symbol = str(symbol).upper().strip()

        if symbol not in self.supported_symbols:
            return None

        if get_instrument(symbol) is None:
            return None

        return symbol

    def get_price(self, symbol):
        symbol = self._validate_symbol(symbol)

        if symbol is None:
            return {
                "success": False,
                "message": "Unsupported symbol."
            }

        result = get_current_price(symbol)

        if not result:
            return {
                "success": False,
                "symbol": symbol,
                "message": "Unable to retrieve live market data."
            }

        bid = float(result["bid"])
        ask = float(result["ask"])
        mid = (bid + ask) / 2

        return {
            "success": True,
            "symbol": symbol,
            "bid": bid,
            "ask": ask,
            "price": round(mid, 8),
            "source": "Twelve Data",
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def get_candle(self, symbol, timeframe="15min"):
        symbol = self._validate_symbol(symbol)

        if symbol is None:
            return {
                "success": False,
                "message": "Unsupported symbol."
            }

        candles = get_candles(
            symbol,
            timeframe=timeframe,
            bars=1
        )

        if not candles:
            return {
                "success": False,
                "symbol": symbol,
                "message": "Unable to retrieve live candle data."
            }

        return {
            "success": True,
            "symbol": symbol,
            "timeframe": timeframe,
            "data": candles[-1],
            "source": "Twelve Data"
        }

    def get_market(self, symbol, timeframe="15min"):
        price = self.get_price(symbol)

        if not price["success"]:
            return price

        candle = self.get_candle(symbol, timeframe)

        return {
            "success": True,
            "symbol": symbol,
            "price": price,
            "candle": candle,
            "source": "Twelve Data"
        }


if __name__ == "__main__":

    print("===== NITRON LIVE MARKET DATA =====")

    market = MarketData()

    result = market.get_market("XAUUSD")

    print(result)
