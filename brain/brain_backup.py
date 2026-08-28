"""
Nitron Brain
Main controller for Nitron's intelligence.
"""

from brain.reasoning import reasoning

try:
    from brain.learning_manager import learning_manager
except ImportError:
    learning_manager = None


class Brain:

    def __init__(self):
        self.name = "Nitron Brain"

    def think(self, message):
        """
        Think about a message and respond.
        """
        return reasoning.answer(message)

    def analyze(self, message):
        """
        Determine the intent of a message.
        """
        return reasoning.analyze(message)

    def learn(self, topic, url):
        """
        Learn from a documentation website.
        """
        if learning_manager is None:
            return "Learning Manager is unavailable."

        return learning_manager.learn(topic, url)

    def learn_site(self, topic, url, limit=10):
        """
        Learn multiple pages from a documentation website.
        """
        if learning_manager is None:
            return "Learning Manager is unavailable."

        return learning_manager.learn_site(
            topic,
            url,
            limit
        )

    def remember(self, key, value):
        """
        Store a fact.
        """
        return reasoning.remember_fact(key, value)

    def recall(self, key):
        """
       Recall a stored fact.
        """
        return reasoning.recall_fact(key)

    def status(self):
        """
       Brain status.
        """
        return reasoning.status()


brain = Brain()
