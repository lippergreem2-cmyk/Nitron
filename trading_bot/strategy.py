import config

REQUIRE_UNANIMOUS_AGREEMENT = True
MIN_ADX_FOR_TRADE = 25


def add_indicators(df):
    close = df["close"]

    df["ema_fast"] = close.ewm(span=config.FAST_EMA, adjust=False).mean()
    df["ema_slow"] = close.ewm(span=config.SLOW_EMA, adjust=False).mean()

    delta = close.diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()
    rs = gain / loss.replace(0, 1e-9)
    df["rsi"] = 100 - (100 / (1 + rs))

    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()
    df["macd"] = ema12 - ema26
    df["macd_signal"] = df["macd"].ewm(span=9, adjust=False).mean()

    sma20 = close.rolling(20).mean()
    std20 = close.rolling(20).std()
    df["bb_upper"] = sma20 + 2 * std20
    df["bb_lower"] = sma20 - 2 * std20

    high, low = df["high"], df["low"]
    plus_dm = (high.diff()).clip(lower=0)
    minus_dm = (-low.diff()).clip(lower=0)
    tr = (high - low).combine((high - close.shift()).abs(), max).combine(
        (low - close.shift()).abs(), max
    )
    atr = tr.rolling(14).mean()
    plus_di = 100 * (plus_dm.rolling(14).mean() / atr.replace(0, 1e-9))
    minus_di = 100 * (minus_dm.rolling(14).mean() / atr.replace(0, 1e-9))
    dx = 100 * (plus_di - minus_di).abs() / (plus_di + minus_di).replace(0, 1e-9)
    df["adx"] = dx.rolling(14).mean()

    return df


def _vote_ema(prev, curr):
    if prev["ema_fast"] <= prev["ema_slow"] and curr["ema_fast"] > curr["ema_slow"]:
        return "BUY"
    if prev["ema_fast"] >= prev["ema_slow"] and curr["ema_fast"] < curr["ema_slow"]:
        return "SELL"
    return "HOLD"


def _vote_rsi(curr):
    if curr["rsi"] < 30:
        return "BUY"
    if curr["rsi"] > 70:
        return "SELL"
    return "HOLD"


def _vote_macd(prev, curr):
    if prev["macd"] <= prev["macd_signal"] and curr["macd"] > curr["macd_signal"]:
        return "BUY"
    if prev["macd"] >= prev["macd_signal"] and curr["macd"] < curr["macd_signal"]:
        return "SELL"
    return "HOLD"


def _vote_bollinger(curr):
    if curr["close"] <= curr["bb_lower"]:
        return "BUY"
    if curr["close"] >= curr["bb_upper"]:
        return "SELL"
    return "HOLD"


def generate_signal(df):
    df = add_indicators(df)

    if len(df) < 30:
        return "HOLD"

    prev, curr = df.iloc[-2], df.iloc[-1]

    if curr["adx"] < MIN_ADX_FOR_TRADE:
        return "HOLD"

    votes = [
        _vote_ema(prev, curr),
        _vote_macd(prev, curr),
        _vote_rsi(curr),
        _vote_bollinger(curr),
    ]
    active_votes = [v for v in votes if v != "HOLD"]

    if not active_votes:
        return "HOLD"

    buy_votes = active_votes.count("BUY")
    sell_votes = active_votes.count("SELL")

    if REQUIRE_UNANIMOUS_AGREEMENT:
        if buy_votes == len(active_votes) and buy_votes >= 3:
            return "BUY"
        if sell_votes == len(active_votes) and sell_votes >= 3:
            return "SELL"
        return "HOLD"
    else:
        if buy_votes >= 3 and sell_votes == 0:
            return "BUY"
        if sell_votes >= 3 and buy_votes == 0:
            return "SELL"
        return "HOLD"
