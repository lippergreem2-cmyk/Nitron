import math
import os
import time

W, H = 60, 24

def clear():
    os.system("clear")

def flower(t):
    clear()

    for y in range(H):
        line = ""
        for x in range(W):
            # Convert terminal coordinates to a centered coordinate system
            xx = (x - W / 2) / 2.2
            yy = (y - H / 2) / 1.1

            r = math.sqrt(xx * xx + yy * yy)
            angle = math.atan2(yy, xx)

            # Animated petals
            petals = 6 + 2 * math.sin(t)
            petal = abs(math.sin(petals * angle + t))

            # Flower shape
            flower_shape = petal * 5.5

            if r < flower_shape and r > 1.2:
                line += "🌸"
            elif r < 2.0:
                line += "🌼"
            else:
                # Stem
                if abs(xx) < 1.2 and yy > 3:
                    line += "🌿"
                # Leaves
                elif yy > 5 and (
                    abs(xx - math.sin(yy * 0.7) * 3) < 1
                    or abs(xx + math.sin(yy * 0.7) * 3) < 1
                ):
                    line += "🍃"
                else:
                    line += " "

        print(line)

try:
    t = 0
    while True:
        flower(t)
        t += 0.15
        time.sleep(0.08)

except KeyboardInterrupt:
    clear()
    print("🌸 Flower stopped. 🌿")
