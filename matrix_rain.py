"""
matrix_rain.py
Classic falling-character "Matrix" terminal animation.
Works in any terminal, including Termux.
"""

import random
import time
import os
import sys

characters = "アイウエオカキクケコサシスセソタチツテト0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def get_terminal_size():
    size = os.get_terminal_size()
    return size.columns, size.lines


def main():
    columns, rows = get_terminal_size()
    drops = [0] * columns

    try:
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            for i in range(columns):
                if drops[i] > 0:
                    line = " " * i + random.choice(characters)
                    print(line[:columns])
                if random.random() > 0.975:
                    drops[i] = 1
                else:
                    drops[i] = (drops[i] + 1) % rows
            time.sleep(0.05)
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()
