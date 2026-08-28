"""
Nitron Study Engine
"""

try:
    from brain.web_reader import reader
    from brain.knowledge_processor import processor
    from brain.learner import learner
    from brain.knowledge_graph import graph

except ImportError:

    from web_reader import reader
    from knowledge_processor import processor
    from learner import learner
    from knowledge_graph import graph


class StudyEngine:

    def __init__(self):

        self.name = "Nitron Study Engine"


    def study(self, topic, url):

        """
        Learn information from a website,
        process it, store it, and connect it
        to Nitron's knowledge graph.
        """

        print("=" * 50)
        print("NITRON LEARNING")
        print("=" * 50)
        print(f"Topic : {topic.lower()}")
        print(f"Source: {url}")
        print()


        # Read webpage

        page = reader.fetch(url)


        if not page.get("success", False):

            return {
                "status": "failed",
                "error": page.get(
                    "error",
                    "Unknown error"
                )
            }


        # Process information

        knowledge = processor.process(
            page.get("title", ""),
            page.get("content", "")
        )


        # Save to Nitron memory

        learner.learn(
            topic=topic.lower(),
            source=url,
            content=knowledge
        )


        # Add to knowledge graph

        graph.add_topic(
            topic.lower(),
            knowledge
        )


        return {

            "status": "success",

            "topic": topic.lower(),

            "source": url,

            "title": knowledge.get(
                "title",
                ""
            ),

            "keywords": knowledge.get(
                "keywords",
                []
            ),

            "summary": knowledge.get(
                "summary",
                ""
            )

        }


    def recall(self, topic):

        """
        Recall learned knowledge.
        """

        return learner.recall(
            topic
        )


    def topics(self):

        """
        List all learned topics.
        """

        return learner.topics()


    def search(self, keyword):

        """
        Search Nitron's learned topics.
        """

        keyword = keyword.lower()

        results = []

        for topic in learner.topics():

            if keyword in topic.lower():

                results.append(topic)

        return results



study_engine = StudyEngine()
