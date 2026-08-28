"""
Nitron Plugin: Device Check
Checks your own phone for common signs of compromise —
unusual apps, battery drain, unexpected admin/VPN settings.
"""

import subprocess
import json


def _run(cmd):
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=15
        )
        return result.stdout.strip()
    except Exception as e:
        return f"(error: {e})"


def device_check(command):

    lines = ["=== Nitron Device Check ===", ""]

    # Installed packages (user-installed, not system)
    pkgs = _run(["pm", "list", "packages", "-3"])
    pkg_count = len(pkgs.splitlines()) if pkgs else 0
    lines.append(f"User-installed apps: {pkg_count}")

    # Battery status via termux-api
    battery = _run(["termux-battery-status"])
    if battery and not battery.startswith("(error"):
        try:
            b = json.loads(battery)
            lines.append(f"Battery: {b.get('percentage')}%  status: {b.get('status')}")
        except Exception:
            lines.append("Battery: (could not parse)")
    else:
        lines.append("Battery: termux-api not available — install Termux:API app")

    lines.append("")
    lines.append("Manual checks still needed (not automatable from Termux):")
    lines.append("  - Settings > Security > Device Admin Apps")
    lines.append("  - Settings > Security > VPN")
    lines.append("  - Settings > Apps > check Accessibility permissions")

    return "\n".join(lines)


def plugin():

    return {
        "name": "device_check",
        "commands": ["device check", "check my phone"],
        "aliases": ["am i hacked", "check device"],
        "priority": 100,
        "enabled": True,
        "run": device_check
    }
