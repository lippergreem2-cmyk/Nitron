"""
Nitron Knowledge Formatter
"""

from datetime import datetime
import re


class KnowledgeFormatter:

    def __init__(self):
        self.name = "Nitron Knowledge Formatter"

    def format(self, topic, source, knowledge):

        topic = topic.strip().lower()

        title = knowledge.get(
            "title",
            ""
        )

        summary = knowledge.get(
            "summary",
            ""
        )

        # Support WebReader/content output.
        if not summary:
            summary = knowledge.get(
                "content",
                ""
            )

        # Support image analyzer output.
        if not summary:
            summary = knowledge.get(
                "description",
                ""
            )

        if not summary:
            analysis = knowledge.get(
                "analysis",
                ""
            )

            if isinstance(analysis, dict):
                summary = analysis.get(
                    "analysis",
                    ""
                )

            elif analysis:
                summary = str(analysis)

        # Generate simple keywords.
        words = re.findall(
            r"\b[a-zA-Z]{4,}\b",
            str(summary).lower()
        )

        keywords = []

        for word in words:

            if word not in keywords:
                keywords.append(word)

            if len(keywords) >= 20:
                break

        # Preserve explicitly supplied keywords.
        supplied_keywords = knowledge.get(
            "keywords",
            []
        )

        if supplied_keywords:
            keywords = supplied_keywords

        # Preserve image analysis details.
        sections = knowledge.get(
            "sections",
            {}
        )

        if not sections:
            analysis = knowledge.get(
                "analysis",
                None
            )

            if isinstance(analysis, dict):
                sections = {
                    "image_analysis": analysis
                }

        # Preserve notes.
        notes = knowledge.get(
            "notes",
            []
        )

        note = knowledge.get(
            "note",
            ""
        )

        if note and note not in notes:
            notes = list(notes)
            notes.append(note)

        return {
            "topic": topic,
            "title": title,
            "source": source,
            "date": str(datetime.now()),
            "summary": str(summary),
            "keywords": keywords,
            "sections": sections,
            "examples": knowledge.get(
                "examples",
                []
            ),
            "related_topics": knowledge.get(
                "related_topics",
                []
            ),
            "notes": notes,
            "confidence": knowledge.get(
                "confidence",
                1.0
            )
        }


formatter = KnowledgeFormatter()
