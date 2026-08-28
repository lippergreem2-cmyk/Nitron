"""
Nitron Web Reader
Extracts useful article content from webpages.
"""

import requests
from bs4 import BeautifulSoup


class WebReader:

    def fetch(self, url):

        try:

            headers = {
                "User-Agent": "Nitron/1.0"
            }

            response = requests.get(
                url,
                headers=headers,
                timeout=20
            )

            response.raise_for_status()

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            # --------------------------------------------------
            # REMOVE NON-CONTENT ELEMENTS
            # --------------------------------------------------

            for tag in soup([
                "script",
                "style",
                "noscript",
                "svg",
                "form",
                "nav",
                "footer",
                "header"
            ]):
                tag.decompose()

            # --------------------------------------------------
            # FIND MAIN ARTICLE
            # --------------------------------------------------

            article = None

            # Wikipedia
            article = soup.select_one(
                "#mw-content-text .mw-parser-output"
            )

            # Generic article containers
            if article is None:
                article = soup.find("article")

            if article is None:
                article = soup.find(
                    "main"
                )

            # Fallback
            if article is None:
                article = soup.body

            if article is None:
                return {
                    "success": False,
                    "error": "No readable page content found."
                }

            # --------------------------------------------------
            # REMOVE ARTICLE-SPECIFIC NOISE
            # --------------------------------------------------

            for tag in article([
                "script",
                "style",
                "noscript",
                "nav",
                "footer",
                "form",
                "table",
                "aside"
            ]):
                tag.decompose()

            # Remove common Wikipedia interface elements
            for selector in [
                ".mw-editsection",
                ".reference",
                ".reflist",
                ".navbox",
                ".vertical-navbox",
                ".metadata",
                ".ambox",
                ".hatnote",
                ".shortdescription",
                ".portal",
                ".catlinks",
                "#toc"
            ]:
                for tag in article.select(selector):
                    tag.decompose()

            # --------------------------------------------------
            # EXTRACT TEXT
            # --------------------------------------------------

            text = article.get_text(
                separator=" ",
                strip=True
            )

            # Normalize whitespace
            text = " ".join(
                text.split()
            )

            # --------------------------------------------------
            # TITLE
            # --------------------------------------------------

            title = ""

            h1 = article.find("h1")

            if h1:
                title = h1.get_text(
                    " ",
                    strip=True
                )

            if not title and soup.title:
                title = soup.title.get_text(
                    " ",
                    strip=True
                )

            # --------------------------------------------------
            # VALIDATE CONTENT
            # --------------------------------------------------

            if not text or len(text) < 100:

                return {
                    "success": False,
                    "error": "Page contained too little readable content."
                }

            return {
                "success": True,
                "title": title,
                "content": text
            }

        except Exception as e:

            return {
                "success": False,
                "error": str(e)
            }


    def learn_url(self, topic, url):

        try:

            from brain.learner import learner

        except ImportError:

            from learner import learner

        result = self.fetch(url)

        if not result.get("success"):

            return result

        entry = learner.learn(
            topic,
            url,
            result
        )

        return {
            "success": True,
            "topic": topic,
            "url": url,
            "entry": entry
        }


reader = WebReader()
