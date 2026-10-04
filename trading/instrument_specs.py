"""
Instrument specifications used by Nitron's paper-trading risk engine.

These are simulation defaults, not broker-specific execution settings.
Do not use them for real-money orders.
"""

INSTRUMENTS = {
    "XAUUSD": {
        "name": "Gold / US Dollar",
        "asset_class": "METAL",
        "contract_size": 100.0,
        "tick_size": 0.01,
        "minimum_lot": 0.01,
        "maximum_lot": 100.0,
        "lot_step": 0.01,
    },

    "EURUSD": {
        "name": "Euro / US Dollar",
        "asset_class": "FOREX",
        "contract_size": 100000.0,
        "tick_size": 0.00001,
        "minimum_lot": 0.01,
        "maximum_lot": 100.0,
        "lot_step": 0.01,
    },

    "GBPUSD": {
        "name": "British Pound / US Dollar",
        "asset_class": "FOREX",
        "contract_size": 100000.0,
        "tick_size": 0.00001,
        "minimum_lot": 0.01,
        "maximum_lot": 100.0,
        "lot_step": 0.01,
    },

    "USDJPY": {
        "name": "US Dollar / Japanese Yen",
        "asset_class": "FOREX",
        "contract_size": 100000.0,
        "tick_size": 0.001,
        "minimum_lot": 0.01,
        "maximum_lot": 100.0,
        "lot_step": 0.01,
    },

    "BTCUSD": {
        "name": "Bitcoin / US Dollar",
        "asset_class": "CRYPTO",
        "contract_size": 1.0,
        "tick_size": 0.01,
        "minimum_lot": 0.01,
        "maximum_lot": 100.0,
        "lot_step": 0.01,
    },
}


def get_instrument(symbol):
    symbol = str(symbol).upper()
    return INSTRUMENTS.get(symbol)


def list_instruments():
    return list(INSTRUMENTS.keys())


if __name__ == "__main__":
    print("===== NITRON INSTRUMENT SPECS =====")

    for symbol in list_instruments():
        print(symbol, get_instrument(symbol))
