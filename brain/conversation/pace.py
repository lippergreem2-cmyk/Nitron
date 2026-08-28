"""
Nitron Conversation Pace Control
Controls response speed and pauses.
"""


class ConversationPace:

    def __init__(self):
        self.speed = "normal"
        self.pause_time = 0.5


    def slow(self):
        """
        Slow explanations for learning.
        """
        self.speed = "slow"
        self.pause_time = 1.2


    def normal(self):
        """
        Normal conversation speed.
        """
        self.speed = "normal"
        self.pause_time = 0.5


    def fast(self):
        """
        Faster short responses.
        """
        self.speed = "fast"
        self.pause_time = 0.2


    def settings(self):
        return {
            "speed": self.speed,
            "pause": self.pause_time
        }


pace = ConversationPace()
