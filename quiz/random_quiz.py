import json
import random
import os

LESSON_FILE = os.path.expanduser("~/Nitron/mathematics.json")


class RandomMathQuiz:

    def __init__(self):

        if os.path.exists(LESSON_FILE):

            with open(LESSON_FILE, "r") as f:

                self.lessons = json.load(f)

        else:

            self.lessons = {}

    def topics(self):

        return sorted(self.lessons.keys())

    def start(self, topic):

        topic = topic.lower().strip()

        if topic not in self.lessons:

            print("Topic not found.")

            return

        lesson = self.lessons[topic]

        questions = lesson.get("exercise", [])

        if not questions:

            print("No exercises available.")

            return

        random.shuffle(questions)

        score = 0

        total = len(questions)

        print()

        print("=" * 40)

        print("MATHEMATICS QUIZ")

        print("Topic:", topic.title())

        print("=" * 40)

        print()

        for number, question in enumerate(questions, 1):

            print(f"{number}. {question}")

            input("Press ENTER after solving...")

            print()

            score += 1

        print("=" * 40)

        print("Quiz Completed")

        print(f"Questions Attempted: {total}")

        print("Remember to check your answers with your teacher or notes.")

        print("=" * 40)

    def random_topic(self):

        if not self.lessons:

            return None

        return random.choice(self.topics())

    def daily_quiz(self):

        topic = self.random_topic()

        if topic:

            self.start(topic)
