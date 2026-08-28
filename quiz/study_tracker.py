import json
import os
import datetime

TRACKER_FILE = "study_tracker.json"


class StudyTracker:

    def __init__(self):

        if os.path.exists(TRACKER_FILE):

            with open(TRACKER_FILE, "r") as f:

                self.data = json.load(f)

        else:

            self.data = {

                "streak": 0,

                "last_date": "",

                "sessions": 0

            }

            self.save()

    def save(self):

        with open(TRACKER_FILE, "w") as f:

            json.dump(self.data, f, indent=4)

    def study_today(self):

        today = str(datetime.date.today())

        last = self.data["last_date"]

        if last != today:

            self.data["streak"] += 1

            self.data["last_date"] = today

            self.data["sessions"] += 1

            self.save()

        return self.data

    def show_progress(self):

        print()

        print("========== STUDY PROGRESS ==========")

        print("Study Sessions :", self.data["sessions"])

        print("Study Streak   :", self.data["streak"], "days")

        print("Last Study     :", self.data["last_date"])

        print("====================================")

    def timetable(self):

        print()

        print("====== DAILY REVISION TIMETABLE ======")

        print("08:00 - Mathematics")

        print("09:00 - English")

        print("10:00 - Kiswahili")

        print("11:00 - Chemistry")

        print("12:00 - Physics")

        print("13:00 - Lunch Break")

        print("14:00 - Biology")

        print("15:00 - Geography")

        print("16:00 - History")

        print("17:00 - CRE")

        print("18:00 - Computer Studies")

        print("19:00 - Revision")

        print("======================================")

    def motivation(self):

        streak = self.data["streak"]

        if streak >= 30:

            return "Outstanding! You have studied for 30 consecutive days."

        elif streak >= 14:

            return "Excellent! Keep the momentum going."

        elif streak >= 7:

            return "Great work! One week of consistent study."

        elif streak >= 3:

            return "Good progress. Keep studying every day."

        else:

            return "Today's study session has been recorded. Keep up the good work!"
