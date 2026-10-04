import numpy as np
import pandas as pd

def rsi(close, period=14):
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1/period, min_periods=period).mean()
    avg_loss = loss.ewm(alpha=1/period, min_periods=period).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))

def macd(close, fast=12, slow=26, signal=9):
    ema_fast = close.ewm(span=fast, adjust=False).mean()
    ema_slow = close.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram

def adx(high, low, close, period=14):
    up_move = high.diff()
    down_move = -low.diff()
    plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0.0)
    minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0.0)
    tr1 = high - low
    tr2 = (high - close.shift()).abs()
    tr3 = (low - close.shift()).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.ewm(alpha=1/period, min_periods=period).mean()
    plus_di = 100 * pd.Series(plus_dm, index=high.index).ewm(alpha=1/period, min_periods=period).mean() / atr
    minus_di = 100 * pd.Series(minus_dm, index=high.index).ewm(alpha=1/period, min_periods=period).mean() / atr
    dx = 100 * (plus_di - minus_di).abs() / (plus_di + minus_di).replace(0, np.nan)
    return dx.ewm(alpha=1/period, min_periods=period).mean()

def bollinger_bands(close, period=20, num_std=2.0):
    middle = close.rolling(period).mean()
    std = close.rolling(period).std()
    upper = middle + num_std * std
    lower = middle - num_std * std
    pct_b = (close - lower) / (upper - lower).replace(0, np.nan)
    return upper, middle, lower, pct_b

def detect_order_blocks(df, lookback=20, threshold_pct=0.5):
    """
    Returns a Series of strings: 'bullish', 'bearish', or 'none' per bar.
    Bullish OB: down-candle followed by a strong up-move (potential buy zone).
    Bearish OB: up-candle followed by a strong down-move (potential sell zone).
    """
    body = (df["close"] - df["open"]).abs()
    avg_body = body.rolling(lookback).mean()
    strong_move = body > avg_body * (1 + threshold_pct)

    bullish = (df["close"].shift(1) < df["open"].shift(1)) & strong_move & (df["close"] > df["open"])
    bearish = (df["close"].shift(1) > df["open"].shift(1)) & strong_move & (df["close"] < df["open"])

    result = pd.Series("none", index=df.index)
    result[bullish.fillna(False)] = "bullish"
    result[bearish.fillna(False)] = "bearish"
    return result

def detect_liquidity_sweep(df, lookback=10):
    """
    Returns a Series of strings: 'bullish', 'bearish', or 'none' per bar.
    Bullish sweep: price wicks below recent low then closes back above it
        (stop hunt on sellers -- often precedes upward move).
    Bearish sweep: price wicks above recent high then closes back below it
        (stop hunt on buyers -- often precedes downward move).
    """
    recent_high = df["high"].rolling(lookback).max().shift(1)
    recent_low = df["low"].rolling(lookback).min().shift(1)

    bearish = (df["high"] > recent_high) & (df["close"] < recent_high)
    bullish = (df["low"] < recent_low) & (df["close"] > recent_low)

    result = pd.Series("none", index=df.index)
    result[bullish.fillna(False)] = "bullish"
    result[bearish.fillna(False)] = "bearish"
    return result

def compute_all_features(df):
    close, high, low = df["close"], df["high"], df["low"]
    rsi_series = rsi(close)
    macd_line, signal_line, hist = macd(close)
    adx_series = adx(high, low, close)
    upper, middle, lower, pct_b = bollinger_bands(close)
    order_blocks = detect_order_blocks(df)
    liquidity_sweeps = detect_liquidity_sweep(df)

    ob = order_blocks.iloc[-1]
    ls = liquidity_sweeps.iloc[-1]

    return {
        "rsi": round(float(rsi_series.iloc[-1]), 2) if not pd.isna(rsi_series.iloc[-1]) else None,
        "macd": round(float(macd_line.iloc[-1]), 5) if not pd.isna(macd_line.iloc[-1]) else None,
        "macd_signal": round(float(signal_line.iloc[-1]), 5) if not pd.isna(signal_line.iloc[-1]) else None,
        "macd_hist": round(float(hist.iloc[-1]), 5) if not pd.isna(hist.iloc[-1]) else None,
        "adx": round(float(adx_series.iloc[-1]), 2) if not pd.isna(adx_series.iloc[-1]) else None,
        "bollinger_pct": round(float(pct_b.iloc[-1]), 3) if not pd.isna(pct_b.iloc[-1]) else None,
        "order_block": ob,             # 'bullish' / 'bearish' / 'none'
        "liquidity_sweep": ls,          # 'bullish' / 'bearish' / 'none'
        "order_block_flag": ob != "none",         # numeric-friendly for the ML model
        "liquidity_sweep_flag": ls != "none",
    }

if __name__ == "__main__":
    np.random.seed(0)
    n = 100
    close = pd.Series(100 + np.cumsum(np.random.randn(n)))
    high = close + np.random.rand(n)
    low = close - np.random.rand(n)
    open_ = close.shift(1).fillna(close.iloc[0])
    df = pd.DataFrame({"open": open_, "high": high, "low": low, "close": close})
    features = compute_all_features(df)
    print("Latest features:", features)
