import os
import json


class KnowledgeEngine:

    def __init__(self):
        self.base_dir = os.path.dirname(__file__)
        self.knowledge_dir = os.path.join(
            self.base_dir,
            "knowledge"
        )

        self.knowledge = {}

        self.load_all()


    def load_all(self):
        """
        Load every knowledge file automatically
        """

        if not os.path.exists(self.knowledge_dir):
            os.makedirs(self.knowledge_dir)

        for file in os.listdir(self.knowledge_dir):

            if file.endswith(".json"):

                path = os.path.join(
                    self.knowledge_dir,
                    file
                )

                try:
                    with open(
                        path,
                        "r",
                        encoding="utf-8"
                    ) as f:

                        name = file.replace(
                            ".json",
                            ""
                        )

                        self.knowledge[name] = json.load(f)

                except Exception as e:
                    print(
                        "Knowledge load error:",
                        file,
                        e
                    )


    def search(self, keyword):

        results = []

        keyword = keyword.lower()

        for category, data in self.knowledge.items():

            text = json.dumps(
                data
            ).lower()

            if keyword in text:

                results.append(category)


        return results


    def get_category(self, category):

        return self.knowledge.get(
            category,
            {}
        )


    def list_knowledge(self):

        return list(
            self.knowledge.keys()
        )


    def count(self):

        return len(
            self.knowledge
        )


knowledge = KnowledgeEngine()


def search(keyword):
    return knowledge.search(keyword)


def get(category):
    return knowledge.get_category(category)


def list_all():
    return knowledge.list_knowledge()


def count():
    return knowledge.count()
