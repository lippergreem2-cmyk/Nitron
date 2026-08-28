import json
import os

BASE_DIR = os.path.dirname(__file__)


class Academy:

    def __init__(self):
        self.cache = {}

    def load_lessons(self, topic):
        topic = topic.lower().strip()

        if topic in self.cache:
            return self.cache[topic]

        file_path = os.path.join(BASE_DIR, f"{topic}.json")

        if not os.path.exists(file_path):
            return None

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                lessons = json.load(file)
                self.cache[topic] = lessons
                return lessons
        except Exception as e:
            print("Lesson loading error:", e)
            return None

    def get_lesson(self, topic, number):
        lessons = self.load_lessons(topic)

        if lessons is None:
            return None

        return lessons.get(str(number))

    def list_lessons(self, topic):
        lessons = self.load_lessons(topic)

        if lessons is None:
            return []

        return list(lessons.keys())

    def count(self, topic):
        lessons = self.load_lessons(topic)

        if lessons is None:
            return 0

        return len(lessons)

    def available_subjects(self):
        subjects = []

        for file in os.listdir(BASE_DIR):
            if file.endswith(".json"):
                subjects.append(file[:-5])

        subjects.sort()
        return subjects

    def teach(self, topic="python", lesson_number=1):

        lesson = self.get_lesson(topic, lesson_number)

        if lesson is None:

            subjects = ", ".join(self.available_subjects())

            return (
                f"I don't have lesson {lesson_number} for '{topic}'.\n\n"
                f"Available subjects:\n{subjects}"
            )

        return (
            f"Subject: {topic.title()}\n"
            f"Lesson {lesson_number}: {lesson['title']}\n\n"
            f"{lesson['explanation']}\n\n"
            f"Code:\n{lesson['code']}\n\n"
            f"Output:\n{lesson['output']}\n\n"
            f"Practice:\n{lesson['practice']}\n\n"
            f"Quiz:\n{lesson['quiz']}"
        )


academy = Academy()


def teach(topic="python", lesson_number=1):
    return academy.teach(topic, lesson_number)


def get_lesson(topic, number):
    return academy.get_lesson(topic, number)


def list_lessons(topic):
    return academy.list_lessons(topic)


def count(topic):
    return academy.count(topic)


def available_subjects():
    return academy.available_subjects()
