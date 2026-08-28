"""
Nitron Knowledge Base
"""

import json
import os


class Knowledge:
    def __init__(self, filename="data/knowledge.json"):
        self.filename = filename
        self.knowledge = {}
        self.load()

    def load(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as file:
                    self.knowledge = json.load(file)
            except Exception:
                self.knowledge = {}
        else:
            self.knowledge = {}

    def save(self):
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)

        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(self.knowledge, file, indent=4)

    def add(self, topic, information):
        self.knowledge[topic.lower()] = information
        self.save()

    def get(self, topic):
        return self.knowledge.get(topic.lower())

    def remove(self, topic):
        topic = topic.lower()
        if topic in self.knowledge:
            del self.knowledge[topic]
            self.save()

    def exists(self, topic):
        return topic.lower() in self.knowledge

    def topics(self):
        return sorted(self.knowledge.keys())

    def search(self, keyword):
        keyword = keyword.lower()
        results = {}

        for topic, info in self.knowledge.items():
            if keyword in topic or keyword in str(info).lower():
                results[topic] = info

        return results

    def clear(self):
        self.knowledge = {}
        self.save()


knowledge = Knowledge()
