import json
import os
import datetime

REPORT_FILE = "report_cards.json"


class ExamSystem:

    def __init__(self):

        self.score = 0
        self.total = 0

    def grade(self, percentage):

        if percentage >= 80:
            return "A"

        elif percentage >= 75:
            return "A-"

        elif percentage >= 70:
            return "B+"

        elif percentage >= 65:
            return "B"

        elif percentage >= 60:
            return "B-"

        elif percentage >= 55:
            return "C+"

        elif percentage >= 50:
            return "C"

        elif percentage >= 45:
            return "C-"

        elif percentage >= 40:
            return "D+"

        elif percentage >= 35:
            return "D"

        else:
            return "E"

    def finish_exam(self, subject, score, total):

        percentage = round((score / total) * 100, 1)

        grade = self.grade(percentage)

        report = {

            "subject": subject,

            "score": score,

            "total": total,

            "percentage": percentage,

            "grade": grade,

            "date": str(datetime.date.today())

        }

        reports = []

        if os.path.exists(REPORT_FILE):

            with open(REPORT_FILE, "r") as f:

                reports = json.load(f)

        reports.append(report)

        with open(REPORT_FILE, "w") as f:

            json.dump(reports, f, indent=4)

        print()

        print("========== REPORT CARD ==========")

        print("Subject    :", subject)

        print("Score      :", score, "/", total)

        print("Percentage :", percentage, "%")

        print("Grade      :", grade)

        print("Date       :", report["date"])

        print("=================================")

    def show_reports(self):

        if not os.path.exists(REPORT_FILE):

            print("No report cards found.")

            return

        with open(REPORT_FILE, "r") as f:

            reports = json.load(f)

        print()

        print("========== ALL REPORT CARDS ==========")

        for report in reports:

            print()

            print("Subject :", report["subject"])

            print("Score   :", report["score"], "/", report["total"])

            print("Grade   :", report["grade"])

            print("Date    :", report["date"])

        print()

        print("======================================")

    def average(self):

        if not os.path.exists(REPORT_FILE):

            return 0

        with open(REPORT_FILE, "r") as f:

            reports = json.load(f)

        if len(reports) == 0:

            return 0

        total = 0

        for report in reports:

            total += report["percentage"]

        return round(total / len(reports), 1)
