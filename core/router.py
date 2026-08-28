"""
Nitron Command Router
"""

class Router:
    def __init__(self):
        self.routes = {
            "academy": [
                "teach",
                "learn",
                "lesson",
                "study",
                "academy",
                "quiz"
            ],
            "developer": [
                "create",
                "build",
                "project",
                "code",
                "app",
                "website"
            ],
            "trading": [
                "trade",
                "market",
                "buy",
                "sell",
                "gold",
                "bitcoin",
                "forex"
            ],
            "voice": [
                "speak",
                "listen",
                "voice"
            ],
            "system": [
                "shutdown",
                "restart",
                "exit",
                "quit"
            ]
        }

    def route(self, command):
        command = command.lower()

        for module, keywords in self.routes.items():
            for keyword in keywords:
                if keyword in command:
                    return module

        return "brain"

    def add_route(self, module, keywords):
        self.routes[module] = keywords

    def list_routes(self):
        return self.routes
