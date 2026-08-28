# wifi_tools.py

import subprocess
import platform
import shutil


def run_command(command):
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=10
        )

        output = result.stdout.strip()

        if result.stderr.strip() and not output:
            output = result.stderr.strip()

        return output

    except FileNotFoundError:
        return f"Command not available: {command[0]}"

    except subprocess.TimeoutExpired:
        return f"Command timed out: {' '.join(command)}"

    except Exception as e:
        return f"Command failed: {e}"


def wps_status():
    report = []

    report.append("WPS STATUS")
    report.append("-" * 60)

    if shutil.which("termux-wifi-connectioninfo"):
        report.append("Termux Wi-Fi API : AVAILABLE")
    else:
        report.append("Termux Wi-Fi API : NOT AVAILABLE")

    if shutil.which("nmcli"):
        report.append("NetworkManager   : AVAILABLE")
    else:
        report.append("NetworkManager   : NOT AVAILABLE")

    report.append("")
    report.append(
        "WPS authentication/PIN-guessing operations are not performed."
    )

    return "\n".join(report)


def wifi_info():

    report = []

    report.append("=" * 60)
    report.append("NITRON WIFI TOOLS")
    report.append("=" * 60)

    report.append(f"Operating System : {platform.system()}")
    report.append("")

    try:
        result = subprocess.run(
            ["ip", "addr"],
            capture_output=True,
            text=True
        )

        report.append("Network Interfaces")
        report.append("-" * 60)
        report.append(result.stdout)

    except Exception as e:
        report.append(f"Unable to read interfaces: {e}")

    report.append("")
    report.append(wps_status())
    report.append("=" * 60)

    return "\n".join(report)


if __name__ == "__main__":
    print(wifi_info())
