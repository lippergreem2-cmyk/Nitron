"""
Nitron Trading Bot - Main Loop
Run with: python main.py
Stop with Ctrl+C.
"""

import time
import config
import data_feed
import strategy
import risk_manager
import executor


def run():
    print(f"Starting Nitron trading bot | mode = {'PAPER' if config.PAPER_TRADING else 'LIVE'}")
    exchange = data_feed.get_exchange()

    while True:
        for symbol in config.SYMBOLS:
            try:
                df = data_feed.fetch_candles(exchange, symbol)
                signal = strategy.generate_signal(df)
                price = data_feed.get_latest_price(exchange, symbol)

                open_positions = executor.get_open_positions()
                if signal in ("BUY", "SELL") and len(open_positions) < config.MAX_OPEN_POSITIONS:
                    balance = (
                        executor.get_paper_balance()
                        if config.PAPER_TRADING
                        else data_feed.get_account_balance(exchange)
                    )
                    size = risk_manager.calculate_position_size(balance, price)
                    sl = risk_manager.calculate_stop_loss(price, signal)
                    tp = risk_manager.calculate_take_profit(price, signal)

                    executor.place_order(exchange, symbol, signal, size, price, sl, tp)
                else:
                    print(f"{symbol}: {signal} (no action) | price={price:.2f}")

            except Exception as e:
                print(f"Error processing {symbol}: {e}")

        time.sleep(config.CHECK_INTERVAL_SECONDS)


if __name__ == "__main__":
    run()
