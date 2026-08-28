"""
Nitron Knowledge Storage Manager
"""

import json
import os
from datetime import datetime


class KnowledgeStore:

    def __init__(self):

        self.file = os.path.join(
            os.path.dirname(__file__),
            "knowledge_database.json"
        )

        self.data = {}

        self.load()


    def load(self):

        if os.path.exists(self.file):

            try:
                with open(
                    self.file,
                    "r",
                    encoding="utf-8"
                ) as f:

                    self.data = json.load(f)

            except Exception:

                self.data = {}


    def save(self):

        with open(
            self.file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.data,
                f,
                indent=4,
                ensure_ascii=False
            )


    def add(self, topic, knowledge):

        self.data[topic.lower()] = {

            "date": str(datetime.now()),

            "knowledge": knowledge

        }

        self.save()


    def get(self, topic):

        return self.data.get(
            topic.lower(),
            None
        )


    def topics(self):

        return sorted(
            self.data.keys()
        )


store = KnowledgeStore()
