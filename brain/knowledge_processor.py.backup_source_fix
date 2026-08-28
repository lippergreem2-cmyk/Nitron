"""
Nitron Knowledge Processor

Turns raw webpage text into cleaner, useful knowledge.
"""

import re


class KnowledgeProcessor:

    def __init__(self):
        self.name = "Nitron Knowledge Processor"

    # ======================================================
    # CLEAN
    # ======================================================

    def clean(self, text):
        if not text:
            return ""

        text = str(text)

        # Normalize whitespace.
        text = re.sub(r"\s+", " ", text)

        # Remove spaces before punctuation.
        text = re.sub(r"\s+([.,!?;:])", r"\1", text)

        # Normalize spaces around brackets.
        text = re.sub(r"\(\s+", "(", text)
        text = re.sub(r"\s+\)", ")", text)

        # Avoid duplicate spaces.
        text = re.sub(r" {2,}", " ", text)

        return text.strip()

    # REMOVE WEBPAGE NOISE
    # ======================================================

    def remove_noise(self, text):

        text = self.clean(text)

        if not text:
            return ""

        noise_patterns = [

            # Wikipedia/interface noise
            r"Jump to content",
            r"Main menu",
            r"move to sidebar",
            r"hide Navigation",
            r"Create account",
            r"Log in",
            r"Personal tools",
            r"Donate",
            r"Search",
            r"Appearance",
            r"Edit links",
            r"Article Talk",
            r"Read Edit",
            r"View history",
            r"Tools move to sidebar",
            r"Actions Read Edit",
            r"Toggle the table of contents",
            r"Contents move to sidebar",
            r"Download as PDF",
            r"Printable version",

            # Common Wikipedia footer/interface text
            r"Random article",
            r"About Wikipedia",
            r"Contact us",
            r"Contribute",
            r"Help",
            r"Learn to edit",
            r"Community portal",
            r"Recent changes",
            r"Upload file",
            r"Special pages",
            r"Further reading",
            r"External links",
        ]

        for pattern in noise_patterns:

            text = re.sub(
                pattern,
                " ",
                text,
                flags=re.IGNORECASE
            )

        return self.clean(text)

    # ======================================================
    # SENTENCES
    # ======================================================

    def sentences(self, text):

        text = self.clean(text)

        if not text:
            return []

        parts = re.split(
            r"(?<=[.!?])\s+",
            text
        )

        sentences = []

        for sentence in parts:

            sentence = sentence.strip()

            if len(sentence) < 40:
                continue

            sentences.append(sentence)

        return sentences

    # ======================================================
    # BAD SENTENCE DETECTION
    # ======================================================

    def is_noise_sentence(self, sentence):

        lower = sentence.lower().strip()

        # Very short fragments
        if len(lower) < 50:
            return True

        # Navigation/interface fragments
        noise_words = (
            "language",
            "languages",
            "menu",
            "toggle",
            "contents",
            "edit",
            "random article",
            "about wikipedia",
            "contact us",
            "community portal",
            "recent changes",
            "upload file",
            "special pages",
            "external links",
            "further reading",
        )

        # Ignore sentences that are mostly navigation.
        if any(word in lower for word in noise_words):

            # Don't reject legitimate technical sentences
            # merely because they contain one common word.
            if len(lower.split()) < 30:
                return True

        return False

    # ======================================================
    # KEYWORDS
    # ======================================================

    def keywords(self, text, limit=30):

        words = self.clean(text).lower().split()

        ignore = {
            "the",
            "a",
            "an",
            "and",
            "or",
            "to",
            "of",
            "in",
            "on",
            "for",
            "is",
            "are",
            "was",
            "were",
            "this",
            "that",
            "with",
            "as",
            "by",
            "be",
            "it",
            "from",
            "which",
            "their",
            "they",
            "these",
            "those",
            "about",
            "into",
            "than",
        }

        keywords = []

        for word in words:

            word = word.strip(
                ".,:;!?()[]{}<>\"'`"
            )

            if len(word) < 3:
                continue

            if word in ignore:
                continue

            if word not in keywords:
                keywords.append(word)

            if len(keywords) >= limit:
                break

        return keywords

    # ======================================================
    # SUMMARY
    # ======================================================

    def summarize(self, text, max_length=1200):

        text = self.remove_noise(text)

        if not text:
            return ""

        # --------------------------------------------------
        # REMOVE COMMON IMAGE/CAPTION PREFIXES
        # --------------------------------------------------
        # Wikipedia sometimes places an image caption directly
        # before the article's first real sentence without a
        # sentence boundary.
        #
        # Example:
        #   "Programmable Universal Machine for Assembly, one
        #    of the first industrial robots (1990) Robotics is..."
        #
        # Remove that caption so the actual definition starts
        # the summary.
        text = re.sub(
            r"^.*?one of the first industrial robots?\s*\(\d{4}\)\s*",
            "",
            text,
            count=1,
            flags=re.IGNORECASE
        )

        text = self.clean(text)

        sentences = self.sentences(text)

        if not sentences:
            return text[:max_length]

        selected = []

        for sentence in sentences:

            if self.is_noise_sentence(sentence):
                continue

            lower = sentence.lower()

            # Skip obvious image-caption fragments.
            if (
                "one of the first" in lower
                and len(sentence.split()) < 20
            ):
                continue

            # Skip sentences that look like lists of languages.
            if (
                "afrikaans" in lower
                and "العربية" in lower
            ):
                continue

            selected.append(sentence)

            current = " ".join(selected)

            if len(current) >= max_length:
                break

            # 4–6 useful sentences are normally enough.
            if len(selected) >= 6:
                break

        summary = " ".join(selected)

        if not summary:
            summary = text[:max_length]

        if len(summary) > max_length:

            summary = (
                summary[:max_length]
                .rsplit(" ", 1)[0]
                + "..."
            )

        return summary

    # ======================================================
    # PROCESS
    # ======================================================

    def process(self, title, content):

        content = self.clean(content)

        summary = self.summarize(content)

        return {
            "title": title,
            "summary": summary,
            "keywords": self.keywords(summary),
            "length": len(content),
        }


processor = KnowledgeProcessor()
