"""
Nitron HTML Parser
"""

import requests

try:
    from brain.documentation_parser import parser
except ImportError:
    from documentation_parser import parser


class HTMLParser:

    def __init__(self):
        self.name = "Nitron HTML Parser"

    def parse_url(self, url):

        headers = {
            "User-Agent": (
                "Mozilla/5.0 Nitron Learning Engine"
            )
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=30
        )

        response.raise_for_status()

        return parser.parse(response.text)

    def parse_html(self, html):

        return parser.parse(html)


html_parser = HTMLParser()
