# network_tools.py

import socket
import platform
import subprocess


def get_hostname():
    return socket.gethostname()


def get_local_ip():
    try:
        return socket.gethostbyname(socket.gethostname())
    except:
        return "Unknown"


def get_public_ip():
    try:
        import requests
        return requests.get(
            "https://api.ipify.org",
            timeout=5
        ).text
    except:
        return "Unavailable"


def ping(host="8.8.8.8"):

    try:

        result = subprocess.run(
            ["ping", "-c", "1", host],
            capture_output=True,
            text=True
        )

        return "Reachable" if result.returncode == 0 else "Unreachable"

    except Exception as e:

        return str(e)


def network_info():

    report = []

    report.append("=" * 60)
    report.append("NITRON NETWORK TOOLS")
    report.append("=" * 60)

    report.append(f"Hostname      : {get_hostname()}")
    report.append(f"Operating Sys : {platform.system()} {platform.release()}")
    report.append(f"Machine       : {platform.machine()}")
    report.append(f"Processor     : {platform.processor()}")
    report.append(f"Python        : {platform.python_version()}")

    report.append("")
    report.append("Network")

    report.append(f"Local IP      : {get_local_ip()}")
    report.append(f"Public IP     : {get_public_ip()}")
    report.append(f"Internet      : {ping()}")

    report.append("=" * 60)

    return "\n".join(report)


if __name__ == "__main__":

    print(network_info())
