import subprocess
import datetime
import json


def system_info(command):
    command = command.lower()

    # Battery
    if "battery" in command:
        try:
            battery = subprocess.check_output(
                ["termux-battery-status"]
            ).decode()

            info = json.loads(battery)

            return f"Battery is {info['percentage']} percent."

        except:
            return "Unable to read battery."

    # Time
    if "time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        return f"It is {now}."

    # Date
    if "date" in command:
        today = datetime.datetime.now().strftime("%A, %d %B %Y")
        return f"Today is {today}."

    # Storage
    if "storage" in command:
        try:
            storage = subprocess.check_output(
                ["df", "-h", "/storage/emulated/0"]
            ).decode()

            return storage

        except:
            return "Unable to check storage."

    # Wi-Fi
    if "wifi" in command:
        try:
            wifi = subprocess.check_output(
                ["termux-wifi-connectioninfo"]
            ).decode()

            return wifi

        except:
            return "Wi-Fi information unavailable."

    # IP Address
    if "ip address" in command or "my ip" in command:
        try:
            ip = subprocess.check_output(
                ["termux-wifi-connectioninfo"]
            ).decode()

            return ip

        except:
            return "Unable to get IP address."

    # Flashlight
    if "flashlight on" in command:
        return "Flashlight control is not supported on all devices."

    if "flashlight off" in command:
        return "Flashlight control is not supported on all devices."

    return None
