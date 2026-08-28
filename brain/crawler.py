"""
Nitron Documentation Crawler
"""

from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


class Crawler:

    def __init__(self):
        self.visited = set()

    def crawl(self, start_url, limit=20):

        pages = []

        domain = urlparse(start_url).netloc

        queue = [start_url]

        while queue and len(pages) < limit:

            url = queue.pop(0)

            if url in self.visited:
                continue

            self.visited.add(url)

            try:

                response = requests.get(
                    url,
                    timeout=15,
                    headers={
                        "User-Agent": "Nitron Learning Engine"
                    }
                )

                if response.status_code != 200:
                    continue

                pages.append(url)

                soup = BeautifulSoup(
                    response.text,
                    "html.parser"
                )

                for link in soup.find_all("a", href=True):

                    new_url = urljoin(
                        url,
                        link["href"]
                    )

                    parsed = urlparse(new_url)

                    if (
                        parsed.netloc == domain
                        and new_url not in self.visited
                    ):
                        queue.append(new_url)

            except Exception:
                pass

        return pages


crawler = Crawler()
