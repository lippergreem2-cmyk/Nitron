# ~/Nitron/bubble_service.py

import os
import subprocess


running = False


def start():

    global running

    if running:
        return

    running = True

    print("Nitron bubble service started.")

    try:
        subprocess.Popen(
            [
                "termux-toast",
                "Nitron bubble active"
            ]
        )

    except Exception as e:
        print("Bubble notification error:", e)



def stop():

    global running

    running = False

    print("Nitron bubble service stopped.")



def status():

    return running
