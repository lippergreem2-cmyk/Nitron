# ~/Nitron/bubble_controller.py

import subprocess
import time


def show_bubble():

    try:

        subprocess.Popen(
            [
                "termux-toast",
                "🔷 Nitron Bubble Ready"
            ]
        )

        print("Bubble request sent.")

    except Exception as e:

        print(
            "Bubble error:",
            e
        )



def wake_nitron():

    print(
        "Waking Nitron..."
    )

    try:

        subprocess.Popen(
            [
                "python",
                "main.py"
            ]
        )

    except Exception as e:

        print(
            "Wake error:",
            e
        )



if __name__ == "__main__":

    show_bubble()

    time.sleep(2)

    print(
        "Waiting for bubble input..."
    )
