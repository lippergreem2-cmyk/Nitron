"""
Nitron Project Planner
"""

class ProjectPlanner:

    def plan(self, request):

        request = request.lower()

        if "game" in request:
            return {
                "type": "game",
                "folders": [
                    "assets",
                    "images",
                    "sounds",
                    "levels",
                    "src"
                ],
                "files": [
                    "main.py",
                    "player.py",
                    "enemy.py",
                    "settings.py"
                ]
            }

        elif "website" in request:
            return {
                "type": "website",
                "folders": [
                    "templates",
                    "static",
                    "css",
                    "js",
                    "images"
                ],
                "files": [
                    "app.py",
                    "index.html",
                    "style.css",
                    "script.js"
                ]
            }

        elif "chatbot" in request:
            return {
                "type": "chatbot",
                "folders": [
                    "brain",
                    "memory",
                    "voice",
                    "skills"
                ],
                "files": [
                    "main.py",
                    "brain.py",
                    "memory.py",
                    "speech.py"
                ]
            }

        elif "api" in request:
            return {
                "type": "api",
                "folders": [
                    "routes",
                    "models",
                    "config"
                ],
                "files": [
                    "app.py",
                    "requirements.txt"
                ]
            }

        return {
            "type": "general",
            "folders": [
                "src",
                "docs"
            ],
            "files": [
                "main.py",
                "README.md"
            ]
        }


planner = ProjectPlanner()
