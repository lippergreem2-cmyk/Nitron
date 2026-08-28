"""
NITRON DEFENSIVE SECURITY SCANNER
Safe first version:
- Checks running processes
- Checks network connections
- Checks Termux startup files
- Reports findings
- Does NOT automatically delete or disable anything
"""

import os
import subprocess
import json
from pathlib import Path
from datetime import datetime


HOME = Path.home()


def run_command(command):
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.stdout.strip()
    except Exception as error:
        return f"ERROR: {error}"


def scan_processes():
    output = run_command("ps -A")

    if not output:
        return {
            "name": "Processes",
            "status": "unknown",
            "details": "Unable to read running processes."
        }

    lines = output.splitlines()

    return {
        "name": "Processes",
        "status": "checked",
        "count": max(0, len(lines) - 1),
        "details": lines[:25]
    }


def scan_network():
    output = run_command(
        "ss -tunap 2>/dev/null || "
        "netstat -tunap 2>/dev/null || "
        "true"
    )

    if not output:
        return {
            "name": "Network",
            "status": "checked",
            "details": "No network connection information was available."
        }

    return {
        "name": "Network",
        "status": "checked",
        "details": output.splitlines()[:40]
    }


def scan_startup():
    possible_files = [
        HOME / ".bashrc",
        HOME / ".profile",
        HOME / ".bash_profile",
        HOME / ".zshrc",
    ]

    found = []

    for path in possible_files:
        if path.exists():
            found.append(str(path))

    return {
        "name": "Startup files",
        "status": "checked",
        "files": found
    }


def scan_unknown_executables():
    suspicious = []

    locations = [
        HOME / ".local" / "bin",
        HOME / "bin",
    ]

    for directory in locations:
        if not directory.exists():
            continue

        try:
            for item in directory.iterdir():
                if item.is_file() and os.access(item, os.X_OK):
                    suspicious.append(str(item))
        except Exception:
            pass

    return {
        "name": "Executable files",
        "status": "checked",
        "files": suspicious
    }


def scan():
    results = {
        "scanner": "Nitron Defensive Security Scanner",
        "time": datetime.now().isoformat(timespec="seconds"),
        "warning": (
            "Findings are indicators for investigation, "
            "not proof that the device has been hacked."
        ),
        "checks": [
            scan_processes(),
            scan_network(),
            scan_startup(),
            scan_unknown_executables(),
        ]
    }

    return results


def print_report():
    report = scan()

    report_dir = HOME / "Nitron" / "security_reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    report_file = (
        report_dir /
        f"security_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )

    report_file.write_text(
        json.dumps(report, indent=4),
        encoding="utf-8"
    )

    print("=" * 60)
    print("NITRON DEFENSIVE SECURITY SCAN")
    print("=" * 60)
    print(f"Time: {report['time']}")
    print()
    print(report["warning"])
    print()

    for check in report["checks"]:
        print(f"--- {check['name']} ---")
        print(f"Status: {check['status']}")

        if "count" in check:
            print(f"Process entries: {check['count']}")

        if "files" in check:
            files = check["files"]
            print(f"Files found: {len(files)}")

        if "details" in check:
            details = check["details"]

            if isinstance(details, list):
                print(f"Details recorded: {len(details)}")
            else:
                print("Details recorded.")

        print()

    print("FULL REPORT:")
    print(report_file)

    return report


if __name__ == "__main__":
    print_report()
