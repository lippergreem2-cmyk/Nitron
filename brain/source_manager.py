"""
Nitron Source Manager
"""

import json
import os


class SourceManager:

    def __init__(self):

        self.file = os.path.join(
            os.path.dirname(__file__),
            "sources.json"
        )

        self.sources = self.load()

    def load(self):

        if not os.path.exists(self.file):
            return []

        try:

            with open(
                self.file,
                "r",
                encoding="utf-8"
            ) as f:

                return json.load(f)

        except Exception:

            return []

    def save(self):

        with open(
            self.file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.sources,
                f,
                indent=4
            )

    def add(self, url):

        if url not in self.sources:

            self.sources.append(url)

            self.save()

        return "Source added."

    def remove(self, url):

        if url in self.sources:

            self.sources.remove(url)

            self.save()

        return "Source removed."

    def list(self):

        return self.sources


source_manager = SourceManager()
