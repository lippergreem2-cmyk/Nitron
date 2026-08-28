"""
Nitron Project Analyzer
"""

class ProjectAnalyzer:

    def analyze(self, request):

        request = request.lower()

        result = {
            "type": "general",
            "language": "python",
            "framework": None,
            "features": []
        }

        # Project types
        if "game" in request:
            result["type"] = "game"

        elif "website" in request:
            result["type"] = "website"

        elif "api" in request:
            result["type"] = "api"

        elif "chatbot" in request:
            result["type"] = "chatbot"

        elif "android" in request or "app" in request:
            result["type"] = "app"

        # Languages

        if "python" in request:
            result["language"] = "python"

        elif "javascript" in request:
            result["language"] = "javascript"

        elif "java" in request:
            result["language"] = "java"

        elif "kotlin" in request:
            result["language"] = "kotlin"

        # Frameworks

        if "flask" in request:
            result["framework"] = "Flask"

        elif "fastapi" in request:
            result["framework"] = "FastAPI"

        elif "django" in request:
            result["framework"] = "Django"

        elif "react" in request:
            result["framework"] = "React"

        # Features

        keywords = [
            "login",
            "database",
            "authentication",
            "dark mode",
            "admin",
            "chat",
            "ai",
            "voice",
            "camera",
            "music",
            "video",
            "payment",
            "search",
            "notifications"
        ]

        for keyword in keywords:

            if keyword in request:
                result["features"].append(keyword)

        return result


analyzer = ProjectAnalyzer()
