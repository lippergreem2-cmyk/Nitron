"""
Nitron Conversation Context
"""

from datetime import datetime


class Context:
    def __init__(self):
        self.reset()

    def reset(self):
        self.current_command = ""
        self.previous_command = ""
        self.current_topic = ""
        self.previous_topic = ""
        self.last_response = ""
        self.timestamp = None

    def update(self, command, topic="", response=""):
        self.previous_command = self.current_command
        self.previous_topic = self.current_topic

        self.current_command = command
        self.current_topic = topic
        self.last_response = response
        self.timestamp = datetime.now()

    def get_command(self):
        return self.current_command

    def get_topic(self):
        return self.current_topic

    def get_response(self):
        return self.last_response

    def get_previous_command(self):
        return self.previous_command

    def get_previous_topic(self):
        return self.previous_topic

    def summary(self):
        return {
            "command": self.current_command,
            "topic": self.current_topic,
            "response": self.last_response,
            "timestamp": str(self.timestamp)
        }


context = Context()
