"""
Nitron Knowledge Builder
"""

import re

try:
    from brain.concept_extractor import extractor
    from brain.concept_classifier import classifier
except ImportError:
    from concept_extractor import extractor
    from concept_classifier import classifier


class KnowledgeBuilder:

    def __init__(self):
        self.name = "Nitron Knowledge Builder"

    def _format_categories(self, categories):

        formatted = {}

        for category in sorted(categories.keys()):

            items = sorted(
                list(set(categories[category]))
            )

            formatted[category] = {
                "count": len(items),
                "items": items
            }

        return formatted

    def build(self, analyzed):

        knowledge = {
            "heading": analyzed["heading"],
            "definition": "",
            "features": [],
            "examples": analyzed["code"],
            "links": [],
            "concepts": [],
            "categories": {}
        }

        # Definition

        for paragraph in analyzed["paragraphs"]:

            if " is " in paragraph.lower():

                knowledge["definition"] = paragraph

                break

        # Links

        for paragraph in analyzed["paragraphs"]:

            urls = re.findall(
                r"https?://\S+",
                paragraph
            )

            knowledge["links"].extend(urls)

        knowledge["links"] = sorted(
            list(set(knowledge["links"]))
        )

        # Features

        for group in analyzed["lists"]:

            knowledge["features"].extend(group)

        # Concepts

        text = " ".join([

            analyzed["heading"],

            knowledge["definition"],

            " ".join(
                knowledge["features"]
            )

        ])

        knowledge["concepts"] = sorted(

            extractor.extract(text)

        )

        # Categories

        categories = classifier.classify(

            knowledge["concepts"]

        )

        knowledge["categories"] = self._format_categories(
            categories
        )

        return knowledge


builder = KnowledgeBuilder()
