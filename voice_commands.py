# voice_commands.py

import re

class VoiceCommands:

    def __init__(self):
        self.commands = {
            "analyze": self.analyze,
            "buy": self.buy,
            "sell": self.sell,
            "scan": self.scan,
            "journal": self.journal,
            "balance": self.balance,
            "positions": self.positions,
            "close": self.close,
            "news": self.news,
            "help": self.help
        }

    def process(self, text):

        text = text.lower().strip()

        if "analyze" in text:

            symbol = self.extract_symbol(text)

            return self.commands["analyze"](symbol)

        elif "buy" in text:

            symbol = self.extract_symbol(text)

            return self.commands["buy"](symbol)

        elif "sell" in text:

            symbol = self.extract_symbol(text)

            return self.commands["sell"](symbol)

        elif "scan" in text:

            return self.commands["scan"]()

        elif "journal" in text:

            return self.commands["journal"]()

        elif "balance" in text:

            return self.commands["balance"]()

        elif "positions" in text:

            return self.commands["positions"]()

        elif "close" in text:

            symbol = self.extract_symbol(text)

            return self.commands["close"](symbol)

        elif "news" in text:

            return self.commands["news"]()

        else:

            return self.help()

    def extract_symbol(self, text):

        symbols = [

            "xauusd",
            "eurusd",
            "gbpusd",
            "usdjpy",
            "audusd",
            "usdcad",
            "usdchf",
            "nzdusd",
            "nas100",
            "us30",
            "btcusd",
            "ethusd"

        ]

        for s in symbols:

            if s in text:

                return s.upper()

        return "XAUUSD"

    def analyze(self, symbol):

        return f"Analyzing {symbol}..."

    def buy(self, symbol):

        return f"Preparing BUY analysis for {symbol}..."

    def sell(self, symbol):

        return f"Preparing SELL analysis for {symbol}..."

    def scan(self):

        return "Scanning all markets..."

    def journal(self):

        return "Opening trade journal..."

    def balance(self):

        return "Reading account balance..."

    def positions(self):

        return "Checking open positions..."

    def close(self, symbol):

        return f"Preparing to close {symbol} position..."

    def news(self):

        return "Checking economic calendar..."

    def help(self):

        return """
Available Commands

Analyze XAUUSD
Analyze EURUSD
Buy Gold
Sell EURUSD
Scan Market
Open Journal
Account Balance
Open Positions
Close Trade
Economic News
"""


if __name__ == "__main__":

    jarvis = VoiceCommands()

    while True:

        command = input("You: ")

        if command.lower() == "exit":
            break

        print("Nitron:", jarvis.process(command))
