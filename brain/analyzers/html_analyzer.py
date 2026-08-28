"""
Nitron HTML Analyzer
Separates webpage structure
"""

from bs4 import BeautifulSoup


class HTMLAnalyzer:

    def __init__(self):
        self.name = "Nitron HTML Analyzer"


    def analyze(self, html):

        soup = BeautifulSoup(
            html,
            "html.parser"
        )


        sections = []


        for heading in soup.find_all(
            ["h1", "h2", "h3"]
        ):

            section = {

                "heading": heading.get_text(
                    " ",
                    strip=True
                ),

                "text": "",

                "code": [],

                "lists": []

            }


            content = []


            for element in heading.find_all_next():

                if element.name in [
                    "h1",
                    "h2",
                    "h3"
                ] and element != heading:

                    break


                if element.name == "p":

                    content.append(
                        element.get_text(
                            " ",
                            strip=True
                        )
                    )


                if element.name == "pre":

                    section["code"].append(
                        element.get_text(
                            "\n",
                            strip=True
                        )
                    )


                if element.name in [
                    "ul",
                    "ol"
                ]:

                    items = []

                    for li in element.find_all(
                        "li"
                    ):

                        items.append(
                            li.get_text(
                                " ",
                                strip=True
                            )
                        )

                    section["lists"].append(
                        items
                    )


            section["text"] = "\n".join(
                content
            )


            sections.append(
                section
            )


        return sections



analyzer = HTMLAnalyzer()
