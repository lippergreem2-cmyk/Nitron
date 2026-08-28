"""
Nitron Knowledge Graph
"""

import json
import os


class KnowledgeGraph:

    def __init__(self):

        self.file = os.path.join(
            os.path.dirname(__file__),
            "knowledge_graph.json"
        )

        self.graph = {}

        self.load()


    def load(self):

        if os.path.exists(self.file):

            try:

                with open(
                    self.file,
                    "r",
                    encoding="utf-8"
                ) as f:

                    self.graph = json.load(f)

            except Exception:

                self.graph = {}


    def save(self):

        with open(
            self.file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.graph,
                f,
                indent=4,
                ensure_ascii=False
            )


    def add_topic(self, topic, knowledge):

        topic = topic.lower()

        concepts = knowledge.get(
            "concepts",
            []
        )

        self.graph[topic] = {

            "concepts": sorted(
                list(set(concepts))
            )

        }

        self.save()


    def related(self, topic):

        topic = topic.lower()

        data = self.graph.get(
            topic,
            {}
        )

        return data.get(
            "concepts",
            []
        )


    def topics(self):

        return sorted(
            self.graph.keys()
        )


graph = KnowledgeGraph()
