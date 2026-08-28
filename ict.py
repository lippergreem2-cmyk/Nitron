# ict.py

from order_blocks import latest_order_block, inside_order_block
from fair_value_gap import latest_fvg, inside_fvg
from liquidity import liquidity_sweep
from premium_discount import premium_discount
from session import analyze_session


def analyze_ict(candles):

    price = float(candles[-1]["close"])

    block = latest_order_block(candles)

    gap = latest_fvg(candles)

    liquidity = liquidity_sweep(candles)

    pd = premium_discount(candles)

    session = analyze_session()

    return {

        "order_block": block,

        "inside_order_block":
            inside_order_block(price, block),

        "fvg": gap,

        "inside_fvg":
            inside_fvg(price, gap),

        "liquidity": liquidity,

        "premium_discount": pd,

        "session": session

    }


if __name__ == "__main__":

    from mt5_data import get_candles

    candles = get_candles("XAUUSD")

    report = analyze_ict(candles)

    print("=" * 60)

    print("NITRON ICT ANALYSIS")

    print("=" * 60)

    for key, value in report.items():

        print()

        print(key.upper())

        print(value)

    print("=" * 60)
