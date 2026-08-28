"""
Nitron Internet Learning System
"""

from urllib.parse import urlparse

try:
    from brain.learning_manager import learning_manager
except ImportError:
    from learning_manager import learning_manager

try:
    from brain.source_manager import source_manager
except ImportError:
    from source_manager import source_manager


class InternetLearning:

    def __init__(self):
        self.name = "Nitron Internet Learning"

    def add_source(self, url):
        """
        Add a learning source.
        """
        return source_manager.add(url)

    def remove_source(self, url):
        """
        Remove a learning source.
        """
        return source_manager.remove(url)

    def list_sources(self):
        """
        List all learning sources.
        """
        return source_manager.list()

    def learn_source(self, url, limit=20):
        """
        Learn from one documentation website.
        """

        topic = urlparse(url).netloc

        return learning_manager.learn_site(
            topic,
            url,
            limit
        )

    def learn_all(self, limit=20):
        """
        Learn from all registered sources.
        """

        results = []

        sources = source_manager.list()

        for url in sources:

            topic = urlparse(url).netloc

            try:

                result = learning_manager.learn_site(
                    topic,
                    url,
                    limit
                )

                results.append({
                    "source": url,
                    "status": "success",
                    "result": result
                })

            except Exception as e:

                results.append({
                    "source": url,
                    "status": "failed",
                    "error": str(e)
                })

        return results

    def status(self):
        """
        Internet learning status.
        """

        return {
            "system": self.name,
            "sources": len(source_manager.list()),
            "source_list": source_manager.list()
        }


internet_learning = InternetLearning()
