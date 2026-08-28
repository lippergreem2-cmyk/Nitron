"""
Nitron Plugin: Network Scanner
Scans your own WiFi network and remembers IP/MAC history.
"""

import subprocess
import json
import os
import re
from datetime import datetime

STATE_FILE = os.path.join(
    os.path.dirname(__file__),
    "network_scanner_state.json"
)

SUBNET = "172.31.203.0/24"


def _run_scan():

    try:

        result = subprocess.run(
            ["nmap", "-sn", SUBNET],
            capture_output=True,
            text=True,
            timeout=60
        )

        output = result.stdout

    except Exception as e:

        return None, str(e)

    devices = []

    current_ip = None

    for line in output.splitlines():

        match = re.search(
            r"Nmap scan report for (?:.* \()?([\d.]+)\)?",
            line
        )

        if match:
            current_ip = match.group(1)

            devices.append({
                "ip": current_ip,
                "mac": None
            })

            continue

        mac_match = re.search(
            r"MAC Address:\s*([0-9A-Fa-f:]{17})",
            line
        )

        if mac_match and current_ip:

            for device in reversed(devices):

                if device["ip"] == current_ip:
                    device["mac"] = mac_match.group(1).upper()
                    break

    return devices, None


def _load_state():

    if not os.path.exists(STATE_FILE):
        return {"devices": {}}

    try:

        with open(STATE_FILE) as f:
            state = json.load(f)

        # Compatibility with the old state format
        if "known_ips" in state and "devices" not in state:

            devices = {}

            for ip in state["known_ips"]:
                devices[ip] = {
                    "mac": None,
                    "last_seen": None
                }

            return {"devices": devices}

        return state

    except Exception:

        return {"devices": {}}


def _save_state(state):

    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def scan_network(command):

    devices, error = _run_scan()

    if error:
        return f"Scan failed: {error}"

    if devices is None:
        return "Scan failed — no results."

    state = _load_state()

    history = state.get("devices", {})

    current_ips = set()

    for device in devices:

        ip = device["ip"]
        mac = device["mac"]

        current_ips.add(ip)

        old = history.get(ip, {})

        # Keep previously discovered MAC if the device
        # is currently not exposing one.
        if not mac:
            mac = old.get("mac")

        history[ip] = {
            "mac": mac,
            "last_seen": datetime.now().isoformat(timespec="seconds")
        }

    new_devices = [
        ip for ip in current_ips
        if ip not in history
    ]

    # The above check happens after updating history, so
    # determine NEW devices from the previous state instead.
    previous_ips = set(state.get("_previous_scan_ips", []))

    new_devices = current_ips - previous_ips

    state["devices"] = history
    state["_previous_scan_ips"] = sorted(current_ips)

    _save_state(state)

    lines = [
        "=== Nitron Network Scan ===",
        f"Subnet: {SUBNET}",
        f"Devices found: {len(current_ips)}",
        ""
    ]

    for ip in sorted(current_ips):

        info = history.get(ip, {})
        mac = info.get("mac")

        marker = " (NEW)" if ip in new_devices else ""

        lines.append(f"  {ip}{marker}")

        if mac:
            lines.append(f"      MAC: {mac}")
        else:
            lines.append("      MAC: unavailable")

    if new_devices:

        lines.append("")
        lines.append(
            f"⚠ {len(new_devices)} new device(s) since last scan."
        )

    else:

        lines.append("")
        lines.append("No new devices since last scan.")

    return "\n".join(lines)


def network_status(command):

    state = _load_state()

    devices = state.get("devices", {})

    if not devices:
        return "No scan history yet. Run 'scan network' first."

    lines = [
        "=== Nitron Network History ===",
        f"Known devices: {len(devices)}",
        ""
    ]

    for ip in sorted(devices):

        info = devices[ip]

        mac = info.get("mac") or "unknown"
        last_seen = info.get("last_seen") or "unknown"

        lines.append(f"  {ip}")
        lines.append(f"      MAC: {mac}")
        lines.append(f"      Last seen: {last_seen}")

    return "\n".join(lines)


def plugin():

    return {
        "name": "network_scanner",
        "commands": [
            "scan network",
            "network status"
        ],
        "aliases": [
            "check network",
            "who's on my wifi"
        ],
        "priority": 100,
        "enabled": True,
        "run": lambda command: (
            scan_network(command)
            if "status" not in command
            else network_status(command)
        )
    }
