import re


class KnowledgeExtractor:

    def clean(self, text):

        text = re.sub(r"\s+", " ", text)

        return text.strip()


    def summarize(self, text, max_length=5000):

        text = self.clean(text)

        if len(text) > max_length:
            text = text[:max_length]

        return text


    def extract(self, page):

        title = page.get("title", "")

        content = page.get("content", "")

        return {
            "title": title,
            "summary": self.summarize(content)
        }


extractor = KnowledgeExtractor()
