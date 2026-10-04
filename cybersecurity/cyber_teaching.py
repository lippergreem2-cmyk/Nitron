#!/usr/bin/env python3

import json
from pathlib import Path

BASE = Path(__file__).resolve().parent

TOOLS_FILE = BASE / "tools.json"

with open(TOOLS_FILE, "r", encoding="utf-8") as f:
    TOOLS = json.load(f)


CURRICULUM = {

    "threat_mindset": {
        "title": "Think Like an Attacker — Defend Like a Security Engineer",
        "level": "Beginner → Advanced",
        "lessons": [
            (
                "1. Think like an attacker",
                "For every system, identify what an attacker might want, "
                "what assets are valuable, what entry points exist, and "
                "what assumptions could be abused."
            ),
            (
                "2. Map the attack surface",
                "Identify accounts, applications, APIs, devices, services, "
                "ports, dependencies and exposed information. Focus on "
                "understanding exposure rather than exploiting it."
            ),
            (
                "3. Threat modeling",
                "For each important asset, ask: what could go wrong, "
                "who could cause it, what would the impact be, and "
                "which controls reduce the risk?"
            ),
            (
                "4. Identity and authentication",
                "Think about weak passwords, stolen sessions, excessive "
                "permissions, missing multi-factor authentication and "
                "poor account recovery. Learn the corresponding defenses."
            ),
            (
                "5. Web application defense",
                "Consider untrusted input, authentication, authorization, "
                "sessions, APIs and sensitive data. Connect each risk to "
                "secure development practices."
            ),
            (
                "6. Network defense",
                "Understand exposed services, unnecessary ports, weak "
                "segmentation, insecure protocols and suspicious traffic."
            ),
            (
                "7. Social engineering awareness",
                "Learn how phishing and manipulation work at a conceptual "
                "level and how users and organizations can recognize them."
            ),
            (
                "8. Detection and logging",
                "Ask what evidence an attempted compromise would leave "
                "behind and which logs or alerts could reveal it."
            ),
            (
                "9. Incident response",
                "Learn the defensive cycle: identify, contain, investigate, "
                "eradicate, recover and learn."
            ),
            (
                "10. Continuous hardening",
                "After finding a weakness, fix it, verify the fix and "
                "repeat the assessment."
            )
        ],
        "practice": (
            "Use a local application, your own device, or an intentionally "
            "vulnerable training lab. Build a threat model before testing."
        ),
        "defense": (
            "Minimize attack surface, use least privilege, patch systems, "
            "protect credentials, enable strong authentication, monitor "
            "important events and maintain backups."
        ),
        "quiz": [
            (
                "What is an attack surface?",
                "The collection of exposed points through which a system "
                "could potentially be affected."
            ),
            (
                "What is threat modeling?",
                "A structured process for identifying threats, assets, "
                "risks and appropriate defenses."
            ),
            (
                "What does least privilege mean?",
                "Giving users and services only the permissions they need."
            ),
            (
                "Why are logs important?",
                "They provide evidence that can help detect and investigate "
                "security events."
            ),
            (
                "What should happen after fixing a vulnerability?",
                "Verify the fix and reassess the system."
            )
        ]
    },



"nmap": {
    "title": "Nmap — Network Discovery",
    "level": "Beginner → Intermediate",
    "lessons": [
        ("Networking foundations",
         "Learn hosts, IP addresses, ports, TCP and UDP."),
        ("Understanding ports",
         "Learn what open, closed and filtered ports mean."),
        ("Service discovery",
         "Learn how services and versions can be identified."),
        ("Reading results",
         "Learn how to interpret an Nmap result."),
        ("Defensive network auditing",
         "Learn how administrators use scans to understand their own networks.")
    ],
    "practice": "Use localhost or an authorized training machine.",
    "defense": "Reduce unnecessary exposed services and keep network services patched.",
    "quiz": [
        ("What identifies a device on an IP network?", "An IP address."),
        ("What does an open port generally indicate?", "A service is accepting connections."),
        ("Why should scans be authorized?", "Because scanning another system without permission can violate rules or laws.")
    ]
},

"wireshark": {
    "title": "Wireshark — Network Traffic Analysis",
    "level": "Beginner → Intermediate",
    "lessons": [
        ("Packets and frames",
         "Understand how network data is divided into packets and frames."),
        ("TCP/IP basics",
         "Learn the major protocols involved in network communication."),
        ("DNS analysis",
         "Understand how domain names are resolved."),
        ("HTTP and HTTPS",
         "Learn what web traffic looks like at the protocol level."),
        ("Reading packet captures",
         "Learn how to filter and interpret authorized packet captures.")
    ],
    "practice": "Use your own traffic or a supplied training PCAP.",
    "defense": "Use encryption, secure protocols and network monitoring.",
    "quiz": [
        ("What is a packet?", "A unit of data transmitted across a network."),
        ("What does DNS do?", "It translates domain names into network addresses."),
        ("Why is HTTPS important?", "It protects web traffic with encryption.")
    ]
},

"burp_suite": {
    "title": "Burp Suite — Web Security",
    "level": "Beginner → Intermediate",
    "lessons": [
        ("HTTP fundamentals",
         "Understand requests, responses, headers and parameters."),
        ("Proxy concepts",
         "Learn how a web proxy sits between a client and server."),
        ("Web application testing",
         "Learn how authorized testers inspect application behavior."),
        ("Authentication and sessions",
         "Understand cookies, sessions and authentication controls."),
        ("Secure web development",
         "Learn how developers prevent common web vulnerabilities.")
    ],
    "practice": "Use OWASP Juice Shop, WebGoat or another authorized lab.",
    "defense": "Validate input, protect sessions and enforce server-side authorization.",
    "quiz": [
        ("What is an HTTP request?", "A message sent by a client to a web server."),
        ("What is a cookie commonly used for?", "Maintaining client-side state such as a session identifier."),
        ("Where should authorization be enforced?", "On the server.")
    ]
},

"sqlmap": {
    "title": "SQLMap — SQL Injection Education",
    "level": "Beginner → Intermediate",
    "lessons": [
        ("Databases",
         "Learn tables, rows, columns and SQL queries."),
        ("SQL injection",
         "Understand how unsafe input can alter a database query."),
        ("Parameterized queries",
         "Learn the primary defensive technique against SQL injection."),
        ("Authorized vulnerable labs",
         "Practice concepts using intentionally vulnerable applications."),
        ("Detection and remediation",
         "Learn how developers identify and fix SQL injection vulnerabilities.")
    ],
    "practice": "Use only an intentionally vulnerable local or authorized training application.",
    "defense": "Use parameterized queries, input validation and least-privilege database accounts.",
    "quiz": [
        ("What is SQL injection?", "A vulnerability where untrusted input changes the intended SQL query."),
        ("What is a parameterized query?", "A query where data values are passed separately from SQL syntax."),
        ("Should user input be concatenated directly into SQL?", "No.")
    ]
},

"kali_linux": {
    "title": "Kali Linux — Security Learning Environment",
    "level": "Beginner",
    "lessons": [
        ("Linux fundamentals",
         "Learn files, directories, permissions and processes."),
        ("Terminal fundamentals",
         "Learn commands, pipes, redirection and environment variables."),
        ("Security tool categories",
         "Understand reconnaissance, analysis, web security and defensive tools."),
        ("Authorized labs",
         "Learn how security professionals use isolated training environments."),
        ("Defensive workflow",
         "Connect tools to vulnerability assessment and remediation.")
    ],
    "practice": "Use an isolated lab or your own systems.",
    "defense": "Keep systems updated and minimize unnecessary software and privileges.",
    "quiz": [
        ("What is Kali Linux?", "A Linux distribution designed for security testing and related work."),
        ("Why use an isolated lab?", "To practice without affecting unauthorized systems."),
        ("What is least privilege?", "Giving an account only the permissions it needs.")
    ]
},

"splunk": {
    "title": "Splunk — Security Log Analysis",
    "level": "Beginner → Intermediate",
    "lessons": [
        ("What are logs?",
         "Learn why systems record events."),
        ("Events and fields",
         "Learn how security information is represented."),
        ("Searching logs",
         "Learn how analysts find relevant events."),
        ("Dashboards",
         "Learn how security data can be visualized."),
        ("Incident investigation",
         "Learn how multiple events can form an investigation timeline.")
    ],
    "practice": "Use sample or your own authorized security logs.",
    "defense": "Centralize important logs and monitor suspicious activity.",
    "quiz": [
        ("What is a log?", "A recorded event or activity from a system."),
        ("Why centralize logs?", "To make monitoring and investigation easier."),
        ("What is a security event?", "An observable activity relevant to security.")
    ]
},

"elk": {
    "title": "ELK — Security Analytics",
    "level": "Beginner → Intermediate",
    "lessons": [
        ("Elasticsearch",
         "Learn the role of searchable indexed data."),
        ("Logstash",
         "Learn how data can be collected and transformed."),
        ("Kibana",
         "Learn how data can be searched and visualized."),
        ("Security analytics",
         "Learn how logs can reveal suspicious patterns."),
        ("Detection workflow",
         "Learn how alerts can lead to investigation and response.")
    ],
    "practice": "Use sample logs or an authorized lab.",
    "defense": "Collect useful logs, protect them and monitor important events.",
    "quiz": [
        ("What does Kibana provide?", "A visualization and analysis interface."),
        ("What is Logstash used for?", "Collecting and processing data."),
        ("Why analyze logs?", "To detect and investigate events.")
    ]
}
}


CATEGORY_LESSONS = {
    "osint": [
        "OSINT fundamentals",
        "Sources and information reliability",
        "Domains and digital assets",
        "Threat intelligence",
        "Privacy and responsible investigation"
    ],
    "network_security": [
        "Networking fundamentals",
        "Hosts and ports",
        "Services and protocols",
        "Network auditing",
        "Defensive network security"
    ],
    "threat_intelligence": [
        "Indicators of compromise",
        "IP and domain intelligence",
        "Threat feeds",
        "Reputation analysis",
        "Defensive response"
    ],
    "training": [
        "Setting up an authorized lab",
        "Understanding vulnerabilities",
        "Reading lab objectives",
        "Documenting findings",
        "Remediation"
    ],
    "web_security": [
        "HTTP fundamentals",
        "Web application architecture",
        "Input validation",
        "Authentication and authorization",
        "Secure development"
    ],
    "network_analysis": [
        "Packets",
        "Protocols",
        "TCP/IP",
        "Traffic analysis",
        "Defensive monitoring"
    ],
    "siem": [
        "Logs",
        "Events",
        "Searching",
        "Visualization",
        "Incident investigation"
    ],
    "analysis": [
        "Data formats",
        "Encoding and decoding",
        "Transformation",
        "Validation",
        "Safe analysis"
    ],
    "knowledge": [
        "Security terminology",
        "Attack techniques",
        "Defensive techniques",
        "Threat modeling",
        "MITRE ATT&CK concepts"
    ],
    "security_platform": [
        "Linux fundamentals",
        "Security tools",
        "Terminal workflow",
        "Authorized labs",
        "Defensive operations"
    ]
}


def normalize(name):
    name = name.lower().strip()
    name = name.replace("-", "_").replace(" ", "_")

    aliases = {
        "nmap": "nmap",
        "wireshark": "wireshark",
        "burp": "burp_suite",
        "burpsuite": "burp_suite",
        "burp_suite": "burp_suite",
        "sqlmap": "sqlmap",
        "kali": "kali_linux",
        "kali_linux": "kali_linux",
        "splunk": "splunk",
        "elk": "elk",
        "owasp_juice_shop": "owasp_juice_shop",
        "juice_shop": "owasp_juice_shop",
        "webgoat": "owasp_webgoat",
        "port_swigger": "port_swigger",
        "portswigger": "port_swigger",
        "hack_the_box": "hack_the_box",
        "tryhackme": "tryhackme",
        "amass": "amass",
        "subfinder": "subfinder",
        "rustscan": "rustscan",
        "shodan": "shodan",
        "censys": "censys",
        "spiderfoot": "spiderfoot",
        "spider_foot": "spiderfoot",
        "maltego": "maltego",
        "theharvester": "theharvester"
        ,"threat_mindset": "threat_mindset"
        ,"hacker_mindset": "threat_mindset"
        ,"think_like_an_attacker": "threat_mindset"
    }

    return aliases.get(name, name)


def available_tools():
    return sorted(TOOLS.keys())


def get_tool(name):
    key = normalize(name)

    if key not in TOOLS:
        return None, key

    return TOOLS[key], key


def teach(name, lesson=None):
    tool, key = get_tool(name)

    if tool is None:
        return (
            f"I don't have '{name}' registered yet.\n"
            f"Try: cyber tools"
        )

    curriculum = CURRICULUM.get(key)

    if curriculum:
        lessons = curriculum["lessons"]

        if lesson is not None:
            try:
                number = int(lesson)
            except ValueError:
                number = 0

            if 1 <= number <= len(lessons):
                title, explanation = lessons[number - 1]

                return (
                    f"NITRON CYBER LESSON {number}/{len(lessons)}\n\n"
                    f"{curriculum['title']}\n"
                    f"Topic: {title}\n\n"
                    f"{explanation}\n\n"
                    f"Practice:\n"
                    f"{curriculum['practice']}\n\n"
                    f"DEFENSIVE FOCUS:\n"
                    f"{curriculum['defense']}\n\n"
                    f"When you're ready, ask:\n"
                    f"teach {key} {number + 1}"
                )

        output = [
            f"NITRON CYBER COURSE",
            "",
            curriculum["title"],
            f"Level: {curriculum['level']}",
            "",
            "COURSE PLAN:"
        ]

        for i, (title, _) in enumerate(lessons, 1):
            output.append(f"{i}. {title}")

        output += [
            "",
            "Practice:",
            curriculum["practice"],
            "",
            "Defensive focus:",
            curriculum["defense"],
            "",
            f"Start with: teach {key} 1"
        ]

        return "\n".join(output)

    category = tool.get("category", "general")
    lessons = CATEGORY_LESSONS.get(
        category,
        [
            "Introduction",
            "Core concepts",
            "Safe practical use",
            "Result interpretation",
            "Defensive applications"
        ]
    )

    output = [
        "NITRON CYBER COURSE",
        "",
        f"Tool: {key}",
        f"Purpose: {tool.get('purpose', '')}",
        f"Category: {category}",
        "",
        "COURSE PLAN:"
    ]

    for i, lesson_name in enumerate(lessons, 1):
        output.append(f"{i}. {lesson_name}")

    output += [
        "",
        "Safety:",
        tool.get(
            "safe_use",
            "Use only with your own data, systems or authorized training environments."
        ),
        "",
        f"Start with: teach {key} 1"
    ]

    return "\n".join(output)


def quiz(name):
    tool, key = get_tool(name)

    if tool is None:
        return f"I don't know that cybersecurity tool: {name}"

    course = CURRICULUM.get(key)

    if not course or not course.get("quiz"):
        return (
            f"Nitron can teach {key}, but a dedicated quiz "
            f"has not been added yet."
        )

    output = [
        f"NITRON QUIZ — {course['title']}",
        ""
    ]

    for i, (question, answer) in enumerate(course["quiz"], 1):
        output.append(f"{i}. {question}")
        output.append(f"   Answer: {answer}")
        output.append("")

    return "\n".join(output)


def cyber_course():
    categories = {}

    for name, info in TOOLS.items():
        categories.setdefault(info.get("category", "general"), []).append(name)

    output = [
        "NITRON CYBERSECURITY ACADEMY",
        "",
        "Nitron can teach these areas:"
    ]

    for category in sorted(categories):
        output.append("")
        output.append(category.upper())

        for name in sorted(set(categories[category])):
            output.append(f"  • {name}")

    output += [
        "",
        "TEACHING COMMANDS:",
        "  teach nmap",
        "  teach nmap 1",
        "  teach wireshark",
        "  teach sqlmap",
        "  teach burp suite",
        "  teach kali linux",
        "  teach splunk",
        "  teach elk",
        "  quiz nmap"
    ]

    return "\n".join(output)


def command(text):
    text = text.strip()

    if not text:
        return cyber_course()

    lower = text.lower()

    if lower in (
        "cyber tools",
        "cybersecurity tools",
        "cyber course",
        "cybersecurity course",
        "cyber academy"
    ):
        return cyber_course()

    if lower in (
        "think like a hacker",
        "think like an attacker",
        "hacker mindset",
        "defensive hacker",
        "security mindset",
        "threat modeling"
    ):
        return teach("threat_mindset")

    if lower.startswith("quiz "):
        return quiz(text[5:].strip())

    if lower.startswith("teach "):
        parts = text[6:].strip().split()

        if not parts:
            return cyber_course()

        # Handle "burp suite", "kali linux", etc.
        if len(parts) >= 2 and " ".join(parts[:2]).lower() in (
            "burp suite",
            "kali linux",
            "juice shop",
            "hack the box"
        ):
            name = " ".join(parts[:2])
            rest = parts[2:]
        else:
            name = parts[0]
            rest = parts[1:]

        lesson = rest[0] if rest else None

        return teach(name, lesson)

    return cyber_course()


if __name__ == "__main__":
    import sys

    query = " ".join(sys.argv[1:])

    print(command(query))
