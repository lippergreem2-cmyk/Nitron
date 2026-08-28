import subprocess


def show_notification():

    subprocess.run(
        [
            "termux-notification",
            "--title",
            "NITRON",
            "--content",
            "Nitron is running",
            "--button1",
            "WAKE",
            "--button1-action",
            "python ~/Nitron/wake_nitron.py"
        ]
    )


if __name__ == "__main__":
    show_notification()
