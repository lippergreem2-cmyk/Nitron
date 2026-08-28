"""
Nitron Memory Manager
"""

import json
import os


class MemoryManager:

    def __init__(self, filename="memory.json"):

        self.filename = filename
        self.memory = {}

        self.load()

    def load(self):

        if os.path.exists(self.filename):

            try:
                with open(self.filename, "r") as f:
                    self.memory = json.load(f)

            except Exception:
                self.memory = {}

    def save(self):

        with open(self.filename, "w") as f:
            json.dump(self.memory, f, indent=4)

    def remember(self, key, value):

        self.memory[key] = value
        self.save()

    def recall(self, key, default=None):

        return self.memory.get(key, default)

    def forget(self, key):

        if key in self.memory:
            del self.memory[key]
            self.save()

    def clear(self):

        self.memory = {}
        self.save()

    def all(self):

        return self.memory


memory = MemoryManager()
