"""
Nitron Learning Manager
"""

from datetime import datetime

try:
    from brain.study import study_engine
    from brain.crawler import crawler
except ImportError:
    from study import study_engine
    from crawler import crawler


class LearningManager:

    def __init__(self):
        self.history = []

    def learn(self, topic, url):

        result = study_engine.study(topic, url)

        self.history.append({
            "topic": topic,
            "url": url,
            "time": str(datetime.now()),
            "result": result
        })

        return result

    def learn_site(self, topic, start_url, limit=20):

        print(f"Starting learning: {start_url}")

        pages = crawler.crawl(
            start_url,
            limit=limit
        )

        results = []

        for page in pages:

            print(f"Studying {page}")

            result = study_engine.study(
                topic,
                page
            )

            results.append({
                "page": page,
                "result": result
            })

        self.history.append({
            "topic": topic,
            "url": start_url,
            "pages": len(results),
            "time": str(datetime.now())
        })

        return results

    def recent(self):

        return self.history

    def clear(self):

        self.history.clear()

        return "History cleared."


learning_manager = LearningManager()
