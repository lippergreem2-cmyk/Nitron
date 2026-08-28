"""
Nitron Brain Memory
"""

import json
import os


class Memory:
    def __init__(self, filename="data/memory.json"):
        self.filename = filename
        self.data = {}
        self.load()

    def load(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as file:
                    self.data = json.load(file)
            except Exception:
                self.data = {}
        else:
            self.data = {}

    def save(self):
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)

        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=4)

    def remember(self, key, value):
        self.data[key] = value
        self.save()

    def recall(self, key, default=None):
        return self.data.get(key, default)

    def forget(self, key):
        if key in self.data:
            del self.data[key]
            self.save()

    def clear(self):
        self.data = {}
        self.save()

    def keys(self):
        return list(self.data.keys())

    def all(self):
        return self.data


memory = Memory()
