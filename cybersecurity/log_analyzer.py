# log_analyzer.py

import os


SUSPICIOUS_WORDS = [
    "error",
    "failed",
    "denied",
    "unauthorized",
    "attack",
    "warning",
    "critical",
    "invalid",
    "login",
    "permission"
]


def analyze_log(filename):

    if not os.path.exists(filename):
        return "Log file not found."

    total = 0
    suspicious = []

    with open(filename, "r", errors="ignore") as file:

        for line in file:

            total += 1

            lower = line.lower()

            for word in SUSPICIOUS_WORDS:

                if word in lower:
                    suspicious.append(line.strip())
                    break

    report = []
    report.append("=" * 60)
    report.append("NITRON LOG ANALYZER")
    report.append("=" * 60)
    report.append(f"File : {filename}")
    report.append(f"Total Lines : {total}")
    report.append(f"Suspicious Entries : {len(suspicious)}")
    report.append("")

    if suspicious:

        report.append("Detected Entries")
        report.append("-" * 60)

        for line in suspicious[:20]:
            report.append(line)

    else:

        report.append("No suspicious entries detected.")

    report.append("=" * 60)

    return "\n".join(report)


if __name__ == "__main__":

    filename = input("Log file: ").strip()

    print(analyze_log(filename))
