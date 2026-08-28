import math
import os
import time
import shutil

GREEN = "\033[20m"
CYAN = "\033[14m"
RESET = "\033[0m"

def clear():
    os.system("clear")

def butterfly(t):
    width, height = shutil.get_terminal_size((80, 24))

    # Keep the butterfly large but inside the terminal
    w = min(70, width - 2)
    h = min(28, height - 2)

    cx = w // 2
    cy = h // 2

    lines = []

    for y in range(-h // 2, h // 2 + 1):
        line = ""

        for x in range(-w // 2, w // 2 + 1):
            # Butterfly curve
            X = x / 18.0
            Y = y / 9.0

            r = math.sqrt(X * X + Y * Y)

            if r == 0:
                value = 0
            else:
                theta = math.atan2(Y, X)

                # Butterfly curve
                value = math.exp(
                    math.cos(theta)
                ) - 2 * math.cos(4 * theta) + math.sin(
                    theta / 12
                ) ** 5

                value *= 1.0 / r

            # Animated wing shimmer
            shimmer = math.sin(t * 3 + x * 0.15 + y * 0.25)

            if abs(value - 1.0) < 0.09:
                line += GREEN + "█" + RESET

            elif abs(value - 0.85) < 0.07 and shimmer > -0.3:
                line += CYAN + "▓" + RESET

            else:
                line += " "

        lines.append(line)

    # Animate the body and wings slightly
    clear()

    print(GREEN + " " * max(0, (width - 30) // 2) +
          "🦋  NITRON BUTTERFLY  🦋" + RESET)
    print()

    for line in lines:
        print(line)

    print()
    print(CYAN + " " * max(0, (width - 28) // 2) +
          "Press Ctrl+C to stop" + RESET)


try:
    t = 0

    while True:
        butterfly(t)
        t += 0.12
        time.sleep(0.05)

except KeyboardInterrupt:
    clear()
    print("🦋 Butterfly stopped.")
