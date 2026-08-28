"""
Nitron Plugin: Wi-Fi Scanner

Lists nearby Wi-Fi networks when Android/Termux Wi-Fi
scanning support is available.

Displays:
- SSID
- BSSID
- signal strength
- frequency
- channel
- security
"""

import subprocess
import json
import shutil


def _run_wifi_scan():

    if not shutil.which("termux-wifi-scaninfo"):
        return None, "termux-wifi-scaninfo is not available."

    try:

        result = subprocess.run(
            ["termux-wifi-scaninfo"],
            capture_output=True,
            text=True,
            timeout=20
        )

    except Exception as e:

        return None, str(e)

    if result.returncode != 0:

        error = result.stderr.strip()

        if not error:
            error = "Wi-Fi scan failed."

        return None, error

    try:

        data = json.loads(result.stdout)

    except json.JSONDecodeError:

        return None, "Wi-Fi scan returned invalid data."

    return data, None


def _channel_from_frequency(freq):

    try:
        freq = int(freq)
    except (TypeError, ValueError):
        return "unknown"

    if 2412 <= freq <= 2484:
        return str((freq - 2407) // 5)

    if 5000 <= freq <= 5900:
        return str((freq - 5000) // 5)

    return "unknown"


def scan_wifi(command=None):

    networks, error = _run_wifi_scan()

    if error:

        return (
            "=== Nitron Wi-Fi Scan ===\n"
            "\n"
            "Wi-Fi scanning is currently unavailable.\n"
            f"Reason: {error}\n"
            "\n"
            "Nitron needs the Android Termux:API Wi-Fi "
            "scanning service to obtain nearby networks."
        )

    if not networks:

        return (
            "=== Nitron Wi-Fi Scan ===\n"
            "\n"
            "No Wi-Fi networks were returned."
        )

    lines = [
        "=== Nitron Wi-Fi Scan ===",
        f"Networks found: {len(networks)}",
        ""
    ]

    for network in networks:

        ssid = network.get("ssid") or "<hidden>"
        bssid = network.get("bssid") or "unavailable"

        rssi = network.get("rssi")
        frequency = network.get("frequency_mhz")

        if rssi is None:
            rssi = network.get("rssi_dbm", "unknown")

        if frequency is None:
            frequency = network.get("frequency", "unknown")

        channel = _channel_from_frequency(frequency)

        security = (
            network.get("capabilities")
            or network.get("security")
            or "unknown"
        )

        lines.append(f"SSID: {ssid}")
        lines.append(f"BSSID: {bssid}")
        lines.append(f"Signal: {rssi} dBm")
        lines.append(f"Frequency: {frequency} MHz")
        lines.append(f"Channel: {channel}")
        lines.append(f"Security: {security}")
        lines.append("")

    return "\n".join(lines)


def plugin():

    return {
        "name": "wifi_scanner",
        "commands": [
            "scan",
            "scan wifi",
            "scan WiFi",
            "wifi scan"
        ],
        "aliases": [
            "nearby wifi",
            "available wifi",
            "find wifi"
        ],
        "priority": 110,
        "enabled": True,
        "run": lambda command: scan_wifi(command)
    }
