#!/usr/bin/env python3

import json
import os
import shutil
import socket
import subprocess
from pathlib import Path

BASE = Path(__file__).resolve().parent
TOOLS_FILE = BASE / "tools.json"

with open(TOOLS_FILE, "r", encoding="utf-8") as f:
    TOOLS = json.load(f)

LESSONS = {
    "nmap": [
        "What hosts and ports are",
        "TCP and UDP basics",
        "Service discovery",
        "Reading scan results",
        "Defensive network auditing"
    ],
    "wireshark": [
        "Packets and frames",
        "TCP/IP",
        "DNS",
        "HTTP/HTTPS",
        "Reading packet captures"
    ],
    "burp_suite": [
        "HTTP requests and responses",
        "Proxy concepts",
        "Web application testing",
        "Authentication testing",
        "Secure web development"
    ],
    "sqlmap": [
        "SQL databases",
        "SQL injection concepts",
        "Parameterized queries",
        "Vulnerable training applications",
        "SQL injection prevention"
    ],
    "kali_linux": [
        "Linux fundamentals",
        "Security tool categories",
        "Terminal workflow",
        "Authorized security labs",
        "Defensive security"
    ],
    "splunk": [
        "Logs and events",
        "Searching security events",
        "Dashboards",
        "Detection concepts",
        "Incident investigation"
    ],
    "elk": [
        "Elasticsearch",
        "Logstash",
        "Kibana",
        "Log collection",
        "Security analytics"
    ]
}


def normalize(name):
    return name.lower().strip().replace(" ", "_").replace("-", "_")


def find_tool(name):
    n = normalize(name)

    aliases = {
        "burp": "burp_suite",
        "burpsuite": "burp_suite",
        "port_swigger": "port_swigger",
        "portswigger": "port_swigger",
        "juice_shop": "owasp_juice_shop",
        "webgoat": "owasp_webgoat",
        "sqlmap": "sqlmap",
        "nmap": "nmap",
        "wireshark": "wireshark",
        "splunk": "splunk",
        "elk": "elk",
        "kali": "kali_linux",
        "amass": "amass",
        "subfinder": "subfinder",
        "rustscan": "rustscan"
    }

    n = aliases.get(n, n)

    return n if n in TOOLS else None


def list_tools():
    groups = {}

    for name, info in TOOLS.items():
        groups.setdefault(info["category"], []).append(name)

    out = ["NITRON CYBERSECURITY ACADEMY", ""]

    for category, names in sorted(groups.items()):
        out.append(category.upper())
        for name in sorted(set(names)):
            out.append(f"  • {name}")
        out.append("")

    return "\n".join(out)


def explain(name):
    tool = find_tool(name)

    if not tool:
        return f"I don't have a cybersecurity module registered for '{name}'."

    info = TOOLS[tool]

    lines = [
        f"TOOL: {tool}",
        f"Category: {info.get('category', 'general')}",
        f"Purpose: {info.get('purpose', 'Security analysis')}"
    ]

    if info.get("safe_use"):
        lines.append(f"Safe-use boundary: {info['safe_use']}")

    if tool in LESSONS:
        lines.append("")
        lines.append("LEARNING PATH:")
        for i, lesson in enumerate(LESSONS[tool], 1):
            lines.append(f"{i}. {lesson}")

    return "\n".join(lines)


def teach(name):
    tool = find_tool(name)

    if not tool:
        return f"I don't have a lesson for '{name}' yet."

    if tool not in LESSONS:
        return (
            f"I can explain {tool}, but its detailed lesson path has not "
            f"been added yet."
        )

    lines = [
        f"NITRON LESSON — {tool.upper()}",
        "",
        f"Purpose: {TOOLS[tool].get('purpose', '')}",
        "",
        "Lessons:"
    ]

    for i, lesson in enumerate(LESSONS[tool], 1):
        lines.append(f"{i}. {lesson}")

    lines += [
        "",
        "Practice should be performed only against your own device "
        "or an explicitly authorized training environment."
    ]

    return "\n".join(lines)


def local_target(target):
    """
    Only allow local/private lab targets for automatic execution.
    Public targets are not accepted by this executor.
    """
    target = target.strip().lower()

    if target in ("localhost", "127.0.0.1", "::1"):
        return True

    try:
        ip = socket.gethostbyname(target)
        first = int(ip.split(".")[0])
        second = int(ip.split(".")[1])

        return (
            first == 10 or
            (first == 172 and 16 <= second <= 31) or
            (first == 192 and second == 168)
        )
    except Exception:
        return False


def run_local_nmap(target="127.0.0.1"):
    if not local_target(target):
        return (
            "Blocked: automatic Nmap execution is restricted to "
            "localhost/private lab targets."
        )

    if not shutil.which("nmap"):
        return (
            "Nmap is not installed in Termux.\n"
            "Install it with: pkg install nmap"
        )

    try:
        result = subprocess.run(
            ["nmap", "-sV", target],
            capture_output=True,
            text=True,
            timeout=60
        )

        return result.stdout[-12000:] or result.stderr[-4000:]

    except subprocess.TimeoutExpired:
        return "Nmap timed out."


def command(command_text):
    text = command_text.strip()
    lower = text.lower()

    if lower in ("cyber tools", "cybersecurity tools", "list cyber tools"):
        return list_tools()

    if lower.startswith("explain "):
        return explain(text[8:])

    if lower.startswith("teach "):
        return teach(text[6:])

    if lower.startswith("cyber teach "):
        return teach(text[12:])

    if lower.startswith("cyber explain "):
        return explain(text[14:])

    if lower in ("scan localhost", "nmap localhost"):
        return run_local_nmap("127.0.0.1")

    if lower.startswith("nmap localhost"):
        return run_local_nmap("127.0.0.1")

    return (
        "Cybersecurity Academy commands:\n"
        "  cyber tools\n"
        "  teach nmap\n"
        "  teach wireshark\n"
        "  teach burp suite\n"
        "  teach sqlmap\n"
        "  teach kali linux\n"
        "  teach splunk\n"
        "  teach elk\n"
        "  explain <tool>\n"
        "  scan localhost"
    )


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        print(command(" ".join(sys.argv[1:])))
    else:
        print(list_tools())
