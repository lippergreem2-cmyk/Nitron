"""
Nitron Conversation History
"""

import json
import os
from datetime import datetime


class History:
    def __init__(self, filename="data/history.json"):
        self.filename = filename
        self.records = []
        self.load()

    def load(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as file:
                    self.records = json.load(file)
            except Exception:
                self.records = []
        else:
            self.records = []

    def save(self):
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)

        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(self.records, file, indent=4)

    def add(self, user, response):
        self.records.append({
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user": user,
            "response": response
        })

        self.save()

    def get_all(self):
        return self.records

    def get_last(self):
        if self.records:
            return self.records[-1]

        return None

    def search(self, word):
        word = word.lower()

        return [
            item for item in self.records
            if word in item["user"].lower()
            or word in item["response"].lower()
        ]

    def clear(self):
        self.records = []
        self.save()


history = History()
