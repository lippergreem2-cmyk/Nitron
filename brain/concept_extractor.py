"""
Nitron Concept Extractor
"""

import re


class ConceptExtractor:

    def __init__(self):

        self.stop_words = {
            "the", "and", "for", "with", "from",
            "into", "this", "that", "these",
            "those", "about", "very", "more",
            "most", "less", "each", "every",
            "using", "used", "use", "thanks",
            "known", "based", "available",
            "fast", "easy", "great", "high",
            "time", "code", "developer",
            "developers", "features",
            "feature", "performance"
        }

    def extract(self, text):

        words = re.findall(
            r"[A-Za-z][A-Za-z0-9+#.-]*",
            text
        )

        concepts = []

        for word in words:

            clean = word.lower().strip(".,:;()[]{}")

            if len(clean) < 3:
                continue

            if clean in self.stop_words:
                continue

            if clean.isdigit():
                continue

            if clean not in concepts:
                concepts.append(clean)

        return concepts


extractor = ConceptExtractor()
