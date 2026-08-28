import random
import shutil
import sys
import time

SYMBOLS = "1111111000001111110000"

GREEN = "\033[32m"
BRIGHT_GREEN = "\033[92m"
RESET = "\033[0m"

def main():
    width, height = shutil.get_terminal_size((80, 24))
    drops = [random.randint(-height, 0) for _ in range(width)]

    sys.stdout.write("\033[2J\033[H")
    sys.stdout.write("\033[?25l")  # hide cursor

    try:
        while True:
            width, height = shutil.get_terminal_size((80, 24))

            if len(drops) != width:
                drops = [random.randint(-height, 0) for _ in range(width)]

            sys.stdout.write("\033[H")

            for y in range(height):
                line = ""

                for x in range(width):
                    distance = drops[x] - y

                    if distance == 0:
                        line += BRIGHT_GREEN + random.choice(SYMBOLS) + RESET
                    elif 0 < distance < 10:
                        line += GREEN + random.choice(SYMBOLS) + RESET
                    else:
                        line += " "

                sys.stdout.write(line + "\n")

            sys.stdout.flush()

            for x in range(width):
                if drops[x] > height + random.randint(3, 20):
                    drops[x] = random.randint(-15, 0)
                else:
                    drops[x] += 1

            time.sleep(0.04)

    except KeyboardInterrupt:
        sys.stdout.write("\033[?25h")
        sys.stdout.write("\033[0m\033[2J\033[H")
        sys.stdout.flush()
        print("Matrix stopped.")

if __name__ == "__main__":
    main()
