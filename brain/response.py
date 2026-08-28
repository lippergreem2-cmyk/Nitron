"""
Nitron Response Engine
"""

from datetime import datetime


class ResponseEngine:
    def __init__(self):
        self.name = "Nitron"

    def success(self, message):
        return {
            "status": "success",
            "message": message,
            "time": self.time()
        }

    def error(self, message):
        return {
            "status": "error",
            "message": message,
            "time": self.time()
        }

    def warning(self, message):
        return {
            "status": "warning",
            "message": message,
            "time": self.time()
        }

    def info(self, message):
        return {
            "status": "info",
            "message": message,
            "time": self.time()
        }

    def speak(self, message):
        """
        Return a response that can be spoken by Nitron.
        """
        return {
            "status": "speak",
            "text": message,
            "time": self.time()
        }

    def greet(self):
        hour = datetime.now().hour

        if hour < 12:
            greeting = "Good morning."
        elif hour < 18:
            greeting = "Good afternoon."
        else:
            greeting = "Good evening."

        return self.speak(f"{greeting} I am Nitron. How can I help you?")

    def goodbye(self):
        return self.speak("Goodbye. Have a great day.")

    def time(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


response = ResponseEngine()
