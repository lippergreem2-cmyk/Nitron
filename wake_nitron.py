# ~/Nitron/wake_nitron.py

import subprocess
import os


NITRON_DIR = os.path.expanduser("~/Nitron")


def wake():

    try:

        subprocess.Popen(
            [
                "bash",
                "-c",
                f"cd {NITRON_DIR} && python main.py"
            ]
        )

        print("Nitron awakened.")

    except Exception as e:

        print(
            "Wake error:",
            e
        )


if __name__ == "__main__":

    wake()
