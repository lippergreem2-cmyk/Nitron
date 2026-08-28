# password_audit.py

import math
import string


def calculate_entropy(password):

    charset = 0

    if any(c.islower() for c in password):
        charset += 26

    if any(c.isupper() for c in password):
        charset += 26

    if any(c.isdigit() for c in password):
        charset += 10

    if any(c in string.punctuation for c in password):
        charset += len(string.punctuation)

    if charset == 0:
        return 0

    return round(len(password) * math.log2(charset), 2)


def check_password(password):

    score = 0
    issues = []

    if len(password) >= 8:
        score += 20
    else:
        issues.append("Password is shorter than 8 characters.")

    if len(password) >= 12:
        score += 20

    if any(c.islower() for c in password):
        score += 10
    else:
        issues.append("Missing lowercase letters.")

    if any(c.isupper() for c in password):
        score += 10
    else:
        issues.append("Missing uppercase letters.")

    if any(c.isdigit() for c in password):
        score += 10
    else:
        issues.append("Missing numbers.")

    if any(c in string.punctuation for c in password):
        score += 20
    else:
        issues.append("Missing special characters.")

    entropy = calculate_entropy(password)

    if entropy >= 60:
        score += 10

    score = min(score, 100)

    if score >= 90:
        level = "Excellent"

    elif score >= 75:
        level = "Strong"

    elif score >= 50:
        level = "Moderate"

    else:
        level = "Weak"

    report = []
    report.append("=" * 40)
    report.append("PASSWORD SECURITY REPORT")
    report.append("=" * 40)
    report.append(f"Length   : {len(password)}")
    report.append(f"Entropy  : {entropy} bits")
    report.append(f"Score    : {score}/100")
    report.append(f"Strength : {level}")
    report.append("")

    if issues:
        report.append("Recommendations:")
        for issue in issues:
            report.append(f"- {issue}")
    else:
        report.append("No obvious weaknesses detected.")

    report.append("=" * 40)

    return "\n".join(report)


if __name__ == "__main__":

    while True:

        pwd = input("Password (or exit): ")

        if pwd.lower() == "exit":
            break

        print(check_password(pwd))
