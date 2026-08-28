import json
import os
import random

PROGRESS_FILE = "quiz_progress.json"


class PersonalTutor:

    def __init__(self):

        if os.path.exists(PROGRESS_FILE):

            with open(PROGRESS_FILE, "r") as f:

                self.progress = json.load(f)

        else:

            self.progress = {}

    def recommend_subject(self):

        if not self.progress:

            return "Start with Mathematics."

        weakest = None
        lowest = 101

        for topic in self.progress:

            percentage = self.progress[topic]["percentage"]

            if percentage < lowest:

                lowest = percentage
                weakest = topic

        return (
            f"You should revise '{weakest.title()}' next.\n"
            f"Your score was {lowest}%."
        )

    def strongest_subject(self):

        if not self.progress:

            return "No quiz history."

        best = None
        highest = -1

        for topic in self.progress:

            percentage = self.progress[topic]["percentage"]

            if percentage > highest:

                highest = percentage
                best = topic

        return (
            f"Excellent work in '{best.title()}'.\n"
            f"Score: {highest}%."
        )

    def daily_plan(self):

        plan = [

            "Mathematics",
            "English",
            "Kiswahili",
            "Physics",
            "Chemistry",
            "Biology",
            "Geography",
            "History",
            "CRE",
            "Computer Studies"

        ]

        random.shuffle(plan)

        print()

        print("===== TODAY'S STUDY PLAN =====")

        hour = 8

        for subject in plan:

            print(f"{hour}:00 - {subject}")

            hour += 1

        print("==============================")

    def motivate(self):

        quotes = [

            "Small progress every day leads to big success.",

            "Practice until it becomes easy.",

            "Every expert was once a beginner.",

            "Learning never stops.",

            "Success comes from consistency, not luck.",

            "One lesson today is better than none."

        ]

        return random.choice(quotes)

    def welcome(self):

        print()

        print("Welcome back Boss Nimrod.")

        print(self.motivate())

        print()

        print(self.recommend_subject())

        print()

        print(self.strongest_subject())
