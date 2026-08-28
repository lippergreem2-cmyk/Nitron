"""
Nitron Knowledge Index
"""

import json
import os


class KnowledgeIndex:

    def __init__(self):

        self.file = os.path.join(
            os.path.dirname(__file__),
            "knowledge_index.json"
        )

        self.index = self.load()

    def load(self):

        if not os.path.exists(self.file):
            return {}

        try:
            with open(
                self.file,
                "r",
                encoding="utf-8"
            ) as f:
                return json.load(f)

        except Exception:
            return {}

    def save(self):

        with open(
            self.file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.index,
                f,
                indent=4
            )

    def add(self, topic, keywords):

        topic = topic.strip().lower()

        self.index[topic] = {
            "keywords": keywords
        }

        self.save()

    def search(self, word):

        word = word.lower()

        results = []

        for topic, data in self.index.items():

            if word == topic:

                results.append(topic)

                continue

            for keyword in data["keywords"]:

                if word in keyword.lower():

                    results.append(topic)

                    break

        return sorted(set(results))

    def topics(self):

        return sorted(self.index.keys())


knowledge_index = KnowledgeIndex()
