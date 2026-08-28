import json
import os

MATH_FILE = os.path.expanduser("~/Nitron/academy/mathematics.json")


class MathTeacher:

    def __init__(self):
        if os.path.exists(MATH_FILE):
            with open(MATH_FILE, "r") as f:
                self.data = json.load(f)
        else:
            self.data = {}

    def topics(self):
        return list(self.data.keys())

    def teach(self, topic):
        topic = topic.lower().strip()
        return self.data.get(topic, "Mathematics topic not found.")
