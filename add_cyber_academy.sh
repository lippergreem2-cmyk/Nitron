#!/data/data/com.termux/files/usr/bin/bash
set -e

echo "=== Nitron Cybersecurity Academy installer ==="

mkdir -p cybersecurity

cat > cybersecurity/tools.json <<'JSON'
{
  "nmap": {
    "category": "network_security",
    "purpose": "Network discovery and port/service auditing",
    "safe_use": "localhost or systems you are authorized to test"
  },
  "wireshark": {
    "category": "network_analysis",
    "purpose": "Capture and analyze network traffic",
    "safe_use": "your own device or authorized lab"
  },
  "burp_suite": {
    "category": "web_security",
    "purpose": "Inspect and test web applications",
    "safe_use": "your own applications and authorized labs"
  },
  "kali_linux": {
    "category": "security_platform",
    "purpose": "Linux environment containing many security tools",
    "safe_use": "authorized security testing"
  },
  "splunk": {
    "category": "siem",
    "purpose": "Search, analyze and visualize security logs"
  },
  "elk": {
    "category": "siem",
    "purpose": "Elasticsearch, Logstash and Kibana security analytics"
  },
  "sqlmap": {
    "category": "web_security",
    "purpose": "SQL injection testing",
    "safe_use": "local/authorized vulnerable applications only"
  },
  "virustotal": {
    "category": "threat_intelligence",
    "purpose": "Analyze suspicious files, URLs and indicators"
  },
  "cyberchef": {
    "category": "analysis",
    "purpose": "Decode, transform and analyze data"
  },
  "shodan": {
    "category": "osint",
    "purpose": "Search internet-connected assets"
  },
  "censys": {
    "category": "osint",
    "purpose": "Discover internet-facing assets"
  },
  "haveibeenpwned": {
    "category": "threat_intelligence",
    "purpose": "Check whether accounts appear in known breaches"
  },
  "urlscan": {
    "category": "threat_intelligence",
    "purpose": "Analyze website behavior and resources"
  },
  "abuseipdb": {
    "category": "threat_intelligence",
    "purpose": "Investigate reported IP abuse"
  },
  "alienvault_otx": {
    "category": "threat_intelligence",
    "purpose": "Threat-intelligence research"
  },
  "greynoise": {
    "category": "threat_intelligence",
    "purpose": "Analyze internet scanning and background noise"
  },
  "mitre_attack": {
    "category": "knowledge",
    "purpose": "Learn attacker techniques and defensive mappings"
  },
  "owasp_webgoat": {
    "category": "training",
    "purpose": "Practice web security in an intentionally vulnerable lab"
  },
  "owasp_juice_shop": {
    "category": "training",
    "purpose": "Practice web application security legally"
  },
  "tryhackme": {
    "category": "training",
    "purpose": "Hands-on cybersecurity learning labs"
  },
  "hack_the_box": {
    "category": "training",
    "purpose": "Authorized cybersecurity practice labs"
  },
  "port_swigger": {
    "category": "training",
    "purpose": "Web security learning and labs"
  },
  "securitytrails": {
    "category": "osint",
    "purpose": "Domain and DNS intelligence"
  },
  "intelx": {
    "category": "osint",
    "purpose": "Search and investigate public intelligence"
  },
  "spiderfoot": {
    "category": "osint",
    "purpose": "Automate OSINT investigations"
  },
  "maltego": {
    "category": "osint",
    "purpose": "Visualize relationships between digital assets"
  },
  "theharvester": {
    "category": "osint",
    "purpose": "Collect public domain, email and subdomain information"
  },
  "amass": {
    "category": "osint",
    "purpose": "Asset and subdomain discovery"
  },
  "subfinder": {
    "category": "osint",
    "purpose": "Passive subdomain discovery"
  },
  "rustscan": {
    "category": "network_security",
    "purpose": "Fast port discovery"
  },
  "wireshark": {
    "category": "network_analysis",
    "purpose": "Network packet analysis"
  }
}
JSON

cat > cybersecurity/cyber_academy.py <<'PY'
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
PY

cat > cybersecurity/__init__.py <<'PY'
from .cyber_academy import command, explain, teach, list_tools
PY

chmod +x cybersecurity/cyber_academy.py

echo
echo "=== Testing Nitron Cybersecurity Academy ==="
python cybersecurity/cyber_academy.py "cyber tools"

echo
echo "=== Testing Nmap lesson ==="
python cybersecurity/cyber_academy.py "teach nmap"

echo
echo "=== Installation complete ==="
echo
echo "Available:"
echo "  python cybersecurity/cyber_academy.py 'cyber tools'"
echo "  python cybersecurity/cyber_academy.py 'teach nmap'"
echo "  python cybersecurity/cyber_academy.py 'teach wireshark'"
echo "  python cybersecurity/cyber_academy.py 'teach burp suite'"
echo "  python cybersecurity/cyber_academy.py 'teach sqlmap'"
echo "  python cybersecurity/cyber_academy.py 'teach kali linux'"
echo "  python cybersecurity/cyber_academy.py 'teach splunk'"
echo "  python cybersecurity/cyber_academy.py 'teach elk'"
echo "  python cybersecurity/cyber_academy.py 'scan localhost'"
