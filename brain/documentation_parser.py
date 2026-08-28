"""
Nitron Documentation Parser
"""

from bs4 import BeautifulSoup


class DocumentationParser:

    def __init__(self):
        self.name = "Nitron Documentation Parser"

    def parse(self, html):

        soup = BeautifulSoup(html, "html.parser")

        for tag in soup([
            "script",
            "style",
            "noscript",
            "header",
            "footer",
            "nav",
            "aside"
        ]):
            tag.decompose()

        title = ""

        if soup.title:
            title = soup.title.get_text(strip=True)

        sections = []

        current = None

        for element in soup.find_all([
            "h1",
            "h2",
            "h3",
            "h4",
            "p",
            "pre",
            "code",
            "ul",
            "ol"
        ]):

            if element.name in [
                "h1",
                "h2",
                "h3",
                "h4"
            ]:

                if current:
                    sections.append(current)

                current = {
                    "heading": element.get_text(" ", strip=True),
                    "text": "",
                    "code": [],
                    "lists": []
                }

            elif current:

                if element.name == "p":

                    current["text"] += (
                        element.get_text(" ", strip=True)
                        + "\n"
                    )

                elif element.name in [
                    "pre",
                    "code"
                ]:

                    code = element.get_text("\n", strip=True)

                    if code:
                        current["code"].append(code)

                elif element.name in [
                    "ul",
                    "ol"
                ]:

                    items = []

                    for li in element.find_all("li"):
                        items.append(
                            li.get_text(
                                " ",
                                strip=True
                            )
                        )

                    if items:
                        current["lists"].append(items)

        if current:
            sections.append(current)

        return {
            "title": title,
            "sections": sections
        }


parser = DocumentationParser()
