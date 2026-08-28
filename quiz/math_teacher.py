import json
import os

LESSON_FILE = os.path.expanduser("~/Nitron/mathematics.json")


class MathTeacher:

    def __init__(self):

        if os.path.exists(LESSON_FILE):

            with open(LESSON_FILE, "r") as f:

                self.lessons = json.load(f)

        else:

            self.lessons = {}

    def teach(self, topic):

        topic = topic.lower().strip()

        if topic not in self.lessons:

            print("I don't know that mathematics topic yet.")

            return

        lesson = self.lessons[topic]

        lines = []

        if "definition" in lesson:

            lines.append("Definition:")
            lines.append(lesson["definition"])
            lines.append("")

        if "formula" in lesson:

            lines.append("Formula:")
            lines.append(lesson["formula"])
            lines.append("")

        if "example" in lesson:

            lines.append("Example:")
            lines.append(lesson["example"])
            lines.append("")

        if "notes" in lesson:

            lines.append("Important Notes:")

            for note in lesson["notes"]:

                lines.append("- " + note)

        position = 0

        while position < len(lines):

            for line in lines[position:position+5]:

                print(line)

            position += 5

            if position >= len(lines):

                break

            answer = input(
                "\nDid you understand?\nType 'continue' to continue or 'repeat' to repeat:\n> "
            ).strip().lower()

            while answer not in ["continue", "repeat"]:

                answer = input("> ").strip().lower()

            if answer == "repeat":

                position -= 5

                if position < 0:

                    position = 0

        print()

        print("Lesson completed.")

    def ask_question(self, topic):

        topic = topic.lower().strip()

        if topic not in self.lessons:

            print("Topic not found.")

            return

        exercises = self.lessons[topic].get("exercise", [])

        if not exercises:

            print("No exercises available.")

            return

        print()

        print("Practice Questions")

        print("-------------------")

        for question in exercises:

            print(question)

            input("Press ENTER after solving...")

            print("Good. Let's continue.\n")

        print("Practice completed.")
