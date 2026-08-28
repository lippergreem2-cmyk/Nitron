"""
Nitron Logger
"""

from datetime import datetime
import os


class Logger:
    def __init__(self, logfile="logs/system.log"):
        self.logfile = logfile

        os.makedirs(os.path.dirname(logfile), exist_ok=True)

    def _write(self, level, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{timestamp}] [{level}] {message}"

        print(line)

        with open(self.logfile, "a", encoding="utf-8") as f:
            f.write(line + "\n")

    def info(self, message):
        self._write("INFO", message)

    def warning(self, message):
        self._write("WARNING", message)

    def error(self, message):
        self._write("ERROR", message)

    def debug(self, message):
        self._write("DEBUG", message)
