# security_advisor.py

from datetime import datetime


TIPS = [

    "Keep your operating system updated.",

    "Enable automatic security updates.",

    "Use strong and unique passwords.",

    "Enable Multi-Factor Authentication (MFA).",

    "Never reuse passwords across accounts.",

    "Lock your device when unattended.",

    "Back up important files regularly.",

    "Use a firewall.",

    "Install software only from trusted sources.",

    "Beware of phishing emails and fake websites.",

    "Avoid downloading unknown attachments.",

    "Use HTTPS websites whenever possible.",

    "Review application permissions regularly.",

    "Remove software you no longer use.",

    "Encrypt sensitive files when possible.",

    "Do not share verification codes.",

    "Use antivirus or endpoint protection software.",

    "Monitor login activity on important accounts.",

    "Protect your recovery email and phone number.",

    "Think before clicking links."
]


CHECKLIST = {

    "System Updates": False,

    "Firewall Enabled": False,

    "Strong Passwords": False,

    "MFA Enabled": False,

    "Backups": False,

    "Antivirus": False

}


def security_tips():

    text = []

    text.append("=" * 50)

    text.append("NITRON SECURITY ADVISOR")

    text.append("=" * 50)

    text.append(f"Generated: {datetime.now()}")

    text.append("")

    for i, tip in enumerate(TIPS, 1):

        text.append(f"{i}. {tip}")

    text.append("")

    text.append("Security Checklist")

    text.append("-" * 50)

    for item, status in CHECKLIST.items():

        mark = "✓" if status else "✗"

        text.append(f"{mark} {item}")

    text.append("=" * 50)

    return "\n".join(text)


def mark_completed(item):

    if item in CHECKLIST:

        CHECKLIST[item] = True

        return f"{item} marked complete."

    return "Unknown checklist item."


def security_score():

    completed = sum(CHECKLIST.values())

    total = len(CHECKLIST)

    return round((completed / total) * 100)


if __name__ == "__main__":

    print(security_tips())

    print()

    print("Current Security Score:", security_score(), "%")
