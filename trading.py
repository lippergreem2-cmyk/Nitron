import MetaTrader5 as mt5

def connect():
    if not mt5.initialize():
        return False
    return True

def disconnect():
    mt5.shutdown()

def analyze(symbol="EURUSD"):

    if not connect():
        return "Could not connect to MT5."

    tick = mt5.symbol_info_tick(symbol)

    if tick is None:
        disconnect()
        return "Symbol not found."

    price = tick.ask

    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M15, 0, 50)

    if rates is None:
        disconnect()
        return "No market data."

    closes = [r["close"] for r in rates]

    ema20 = sum(closes[-20:]) / 20
    ema50 = sum(closes[-50:]) / 50

    if ema20 > ema50:
        signal = "BUY"
        entry = price
        sl = entry - 0.0020
        tp = entry + 0.0040

    elif ema20 < ema50:
        signal = "SELL"
        entry = price
        sl = entry + 0.0020
        tp = entry - 0.0040

    else:
        signal = "WAIT"
        entry = price
        sl = 0
        tp = 0

    disconnect()

    return f"""
Symbol: {symbol}

Signal: {signal}

Entry: {entry:.5f}

Stop Loss: {sl:.5f}

Take Profit: {tp:.5f}

EMA20: {ema20:.5f}
EMA50: {ema50:.5f}
"""
