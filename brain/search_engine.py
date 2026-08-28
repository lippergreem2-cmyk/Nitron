"""
==========================================================
NITRON INTERNAL SEARCH ENGINE
==========================================================

Features:
    - Document indexing
    - Tokenization
    - Inverted index
    - Keyword matching
    - Relevance scoring
    - Ranked search results
    - Phrase matching
    - Automatic index rebuilding

This is Nitron's INTERNAL search engine.

It does not replace search.py.
search.py remains responsible for Google/Wikipedia/web searches.
==========================================================
"""

import os
import re
import json
from collections import defaultdict, Counter


class SearchEngine:

    def __init__(self):

        self.index_file = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "data",
            "search_index.json"
        )

        self.documents = {}
        self.index = defaultdict(set)

        self.stop_words = {
            "a", "an", "and", "are", "as", "at",
            "be", "by", "for", "from", "has",
            "he", "in", "is", "it", "its",
            "of", "on", "or", "that", "the",
            "to", "was", "were", "will", "with",
            "this", "these", "those", "can",
            "could", "should", "would", "do",
            "does", "did", "how", "what",
            "when", "where", "who", "why"
        }

        self.load_index()


    # ======================================================
    # TOKENIZATION
    # ======================================================

    def tokenize(self, text):

        if text is None:
            return []

        text = str(text).lower()

        words = re.findall(
            r"[a-zA-Z0-9_]+",
            text
        )

        return [
            word
            for word in words
            if word not in self.stop_words
            and len(word) > 1
        ]


    # ======================================================
    # CONVERT ANY OBJECT INTO SEARCHABLE TEXT
    # ======================================================

    def flatten(self, value):

        if value is None:
            return ""

        if isinstance(value, str):
            return value

        if isinstance(value, dict):

            parts = []

            for key, item in value.items():

                parts.append(str(key))
                parts.append(self.flatten(item))

            return " ".join(parts)

        if isinstance(value, (list, tuple, set)):

            return " ".join(
                self.flatten(item)
                for item in value
            )

        return str(value)


    # ======================================================
    # ADD DOCUMENT
    # ======================================================

    def add_document(
        self,
        document_id,
        title,
        content,
        source=""
    ):

        document_id = str(document_id)

        text = " ".join([
            str(title),
            self.flatten(content),
            str(source)
        ])

        tokens = self.tokenize(text)

        self.documents[document_id] = {
            "id": document_id,
            "title": str(title),
            "content": content,
            "source": str(source),
            "text": text,
            "tokens": tokens
        }

        # Add document to inverted index
        for token in set(tokens):

            self.index[token].add(
                document_id
            )


    # ======================================================
    # REMOVE DOCUMENT
    # ======================================================

    def remove_document(self, document_id):

        document_id = str(document_id)

        if document_id not in self.documents:
            return False

        for token in list(self.index.keys()):

            self.index[token].discard(
                document_id
            )

            if not self.index[token]:
                del self.index[token]

        del self.documents[document_id]

        return True


    # ======================================================
    # CLEAR INDEX
    # ======================================================

    def clear(self):

        self.documents = {}
        self.index = defaultdict(set)


    # ======================================================
    # BUILD FROM NITRON LEARNER
    # ======================================================

    def index_learner(self, learner):

        self.clear()

        knowledge = getattr(
            learner,
            "knowledge",
            {}
        )

        for topic, data in knowledge.items():

            if isinstance(data, dict):

                title = data.get(
                    "title",
                    topic
                )

                source = data.get(
                    "source",
                    ""
                )

                content = data

            else:

                title = topic
                source = ""
                content = data

            self.add_document(
                document_id=f"knowledge:{topic}",
                title=title,
                content=content,
                source=source
            )

        self.save_index()

        return len(self.documents)


    # ======================================================
    # BUILD FROM DATA/KNOWLEDGE
    # ======================================================

    def index_knowledge(self, knowledge):

        if knowledge is None:
            return 0

        for topic, data in knowledge.items():

            self.add_document(
                document_id=f"data:{topic}",
                title=topic,
                content=data,
                source="Nitron Knowledge"
            )

        self.save_index()

        return len(self.documents)


    # ======================================================
    # SEARCH
    # ======================================================

    def search(
        self,
        query,
        limit=10
    ):

        query = str(query).strip()

        if not query:
            return []

        query_tokens = self.tokenize(query)

        if not query_tokens:
            return []

        candidate_documents = set()

        for token in query_tokens:

            candidate_documents.update(
                self.index.get(token, set())
            )

        results = []

        for document_id in candidate_documents:

            document = self.documents.get(
                document_id
            )

            if not document:
                continue

            score = self.score_document(
                document,
                query,
                query_tokens
            )

            if score <= 0:
                continue

            results.append({
                "id": document["id"],
                "title": document["title"],
                "source": document["source"],
                "score": score,
                "content": document["content"]
            })

        results.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        return results[:limit]


    # ======================================================
    # RELEVANCE SCORING
    # ======================================================

    def score_document(
        self,
        document,
        query,
        query_tokens
    ):

        title = str(
            document.get("title", "")
        ).lower()

        text = str(
            document.get("text", "")
        ).lower()

        tokens = document.get(
            "tokens",
            []
        )

        counts = Counter(tokens)

        score = 0

        # ----------------------------------------------
        # Keyword frequency
        # ----------------------------------------------

        for token in query_tokens:

            frequency = counts.get(
                token,
                0
            )

            score += frequency * 2

        # ----------------------------------------------
        # Title match gets higher weight
        # ----------------------------------------------

        for token in query_tokens:

            if token in title:
                score += 8

        # ----------------------------------------------
        # Exact phrase
        # ----------------------------------------------

        if query.lower() in text:
            score += 10

        # ----------------------------------------------
        # Exact title
        # ----------------------------------------------

        if query.lower() == title:
            score += 20

        return score


    # ======================================================
    # SAVE INDEX
    # ======================================================

    def save_index(self):

        os.makedirs(
            os.path.dirname(self.index_file),
            exist_ok=True
        )

        data = {
            "documents": self.documents,
            "index": {
                token: list(document_ids)
                for token, document_ids
                in self.index.items()
            }
        }

        try:

            with open(
                self.index_file,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    data,
                    file,
                    indent=2,
                    ensure_ascii=False
                )

        except Exception as error:

            print(
                f"[SEARCH] Could not save index: {error}"
            )


    # ======================================================
    # LOAD INDEX
    # ======================================================

    def load_index(self):

        if not os.path.exists(
            self.index_file
        ):
            return

        try:

            with open(
                self.index_file,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

            self.documents = data.get(
                "documents",
                {}
            )

            self.index = defaultdict(
                set
            )

            for token, document_ids in data.get(
                "index",
                {}
            ).items():

                self.index[token] = set(
                    document_ids
                )

        except Exception:

            self.documents = {}

            self.index = defaultdict(
                set
            )


    # ======================================================
    # STATISTICS
    # ======================================================

    def stats(self):

        return {
            "documents": len(
                self.documents
            ),
            "keywords": len(
                self.index
            )
        }


# ==========================================================
# GLOBAL SEARCH ENGINE
# ==========================================================

search_engine = SearchEngine()
