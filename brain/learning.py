"""
Nitron Learning Engine
"""

from brain.memory import memory
from brain.knowledge import knowledge


class LearningEngine:
    def __init__(self):
        self.enabled = True

    def learn(self, topic, information):
        """
        Store new knowledge.
        """
        topic = topic.strip().lower()
        information = information.strip()

        knowledge.add(topic, information)
        memory.remember(f"learned:{topic}", information)

        return f"I have learned about '{topic}'."

    def recall(self, topic):
        """
        Recall stored knowledge.
        """
        topic = topic.strip().lower()

        info = knowledge.get(topic)

        if info:
            return info

        return "I don't know that yet."

    def update(self, topic, information):
        """
        Update existing knowledge.
        """
        topic = topic.strip().lower()

        knowledge.add(topic, information)
        memory.remember(f"learned:{topic}", information)

        return f"Knowledge updated for '{topic}'."

    def forget(self, topic):
        """
        Remove knowledge.
        """
        topic = topic.strip().lower()

        knowledge.remove(topic)
        memory.forget(f"learned:{topic}")

        return f"I forgot '{topic}'."

    def topics(self):
        """
        Return all known topics.
        """
        return knowledge.topics()

    def search(self, keyword):
        """
        Search the knowledge base.
        """
        return knowledge.search(keyword)


learning = LearningEngine()
