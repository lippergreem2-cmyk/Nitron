"""
Nitron Section Analyzer
"""

import re


class SectionAnalyzer:

    def analyze(self, section):

        heading = section["heading"].replace("¶", "").strip()

        text = section["text"].strip()

        lines = [
            line.strip()
            for line in text.split("\n")
            if line.strip()
        ]

        summary = ""

        if lines:
            summary = lines[0]

        return {
            "heading": heading,
            "summary": summary,
            "paragraphs": lines,
            "code": section["code"],
            "lists": section["lists"]
        }


analyzer = SectionAnalyzer()
