"""
Nitron Conversation Manager
"""

from datetime import datetime


class Conversation:
    def __init__(self):
        self.history = []

    def add(self, user_message, nitron_response):
        self.history.append({
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user": user_message,
            "nitron": nitron_response
        })

    def last(self):
        if self.history:
            return self.history[-1]
        return None

    def all(self):
        return self.history

    def clear(self):
        self.history = []

    def count(self):
        return len(self.history)

    def last_user_message(self):
        if self.history:
            return self.history[-1]["user"]
        return ""

    def last_response(self):
        if self.history:
            return self.history[-1]["nitron"]
        return ""

    def search(self, keyword):
        keyword = keyword.lower()
        results = []

        for chat in self.history:
            if (
                keyword in chat["user"].lower()
                or keyword in chat["nitron"].lower()
            ):
                results.append(chat)

        return results


conversation = Conversation()
