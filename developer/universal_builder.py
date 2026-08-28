# ==========================================================
# NITRON UNIVERSAL BUILDER v1.0
# APP + WEB + AI + CHATBOT + GAME + API PROJECT STRUCTURES
# ==========================================================

import re
from pathlib import Path


class UniversalBuilder:

    def __init__(self, root=None):

        if root is None:
            root = (
                Path(__file__).resolve().parent.parent
                / "GeneratedProjects"
            )

        self.root = Path(root)
        self.root.mkdir(
            parents=True,
            exist_ok=True
        )

    # ======================================================
    # NAME CLEANING
    # ======================================================

    def clean_name(self, name):

        name = str(name).strip()

        name = re.sub(
            r"[^a-zA-Z0-9_-]+",
            "_",
            name
        )

        name = name.strip("_-")

        if not name:
            name = "NitronProject"

        return name

    # ======================================================
    # PROJECT TYPE DETECTION
    # ======================================================

    def detect_type(self, request):

        text = request.lower()

        if any(word in text for word in [
            "chatbot",
            "chat bot",
            "assistant",
            "ai assistant"
        ]):
            return "chatbot"

        if any(word in text for word in [
            "artificial intelligence",
            "machine learning",
            " ai ",
            "ai app",
            "ai system",
            "ai model"
        ]):
            return "ai"

        if any(word in text for word in [
            "website",
            "web",
            "web app",
            "online store",
            "ecommerce",
            "e-commerce"
        ]):
            return "web"

        if any(word in text for word in [
            "android",
            "android app",
            "mobile app",
            "phone app"
        ]):
            return "android"

        if any(word in text for word in [
            "game",
            "gaming"
        ]):
            return "game"

        if any(word in text for word in [
            "api",
            "backend",
            "server"
        ]):
            return "api"

        if any(word in text for word in [
            "python",
            "python program",
            "python application"
        ]):
            return "python"

        return "general"

    # ======================================================
    # PROJECT NAME
    # ======================================================

    def detect_name(self, request):

        text = request.strip()

        patterns = [
            r"build\s+(?:a|an)?\s*(.+)",
            r"create\s+(?:a|an)?\s*(.+)",
            r"make\s+(?:a|an)?\s*(.+)",
            r"generate\s+(?:a|an)?\s*(.+)"
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                name = match.group(1).strip()

                # Remove common project-type words
                name = re.sub(
                    r"\b(website|web|app|application|"
                    r"project|system)\b",
                    "",
                    name,
                    flags=re.IGNORECASE
                )

                name = name.strip()

                if name:
                    return self.clean_name(name)

        return "NitronProject"

    # ======================================================
    # STRUCTURE DEFINITIONS
    # ======================================================

    def structure(self, project_type):

        structures = {

            # ------------------------------------------------
            # WEB
            # ------------------------------------------------

            "web": [
                "frontend/",
                "frontend/index.html",
                "frontend/css/",
                "frontend/css/style.css",
                "frontend/js/",
                "frontend/js/app.js",
                "frontend/assets/",
                "backend/",
                "backend/app.py",
                "backend/routes/",
                "backend/models/",
                "backend/services/",
                "backend/config/",
                "database/",
                "database/schema.sql",
                "tests/",
                "docs/",
                "README.md"
            ],

            # ------------------------------------------------
            # ANDROID
            # ------------------------------------------------

            "android": [
                "app/",
                "app/src/",
                "app/src/main/",
                "app/src/main/java/",
                "app/src/main/res/",
                "app/src/main/res/layout/",
                "app/src/main/res/drawable/",
                "app/src/main/res/values/",
                "app/src/main/AndroidManifest.xml",
                "gradle/",
                "build.gradle",
                "settings.gradle",
                "README.md"
            ],

            # ------------------------------------------------
            # AI
            # ------------------------------------------------

            "ai": [
                "models/",
                "data/",
                "data/raw/",
                "data/processed/",
                "training/",
                "inference/",
                "api/",
                "config/",
                "utils/",
                "tests/",
                "docs/",
                "requirements.txt",
                "README.md"
            ],

            # ------------------------------------------------
            # CHATBOT
            # ------------------------------------------------

            "chatbot": [
                "app/",
                "app/main.py",
                "app/chat/",
                "app/chat/engine.py",
                "app/chat/memory.py",
                "app/chat/prompts.py",
                "models/",
                "data/",
                "api/",
                "api/routes/",
                "config/",
                "tests/",
                "docs/",
                "requirements.txt",
                "README.md"
            ],

            # ------------------------------------------------
            # GAME
            # ------------------------------------------------

            "game": [
                "src/",
                "src/main.py",
                "src/player/",
                "src/enemies/",
                "src/world/",
                "src/ui/",
                "assets/",
                "assets/images/",
                "assets/audio/",
                "config/",
                "tests/",
                "docs/",
                "requirements.txt",
                "README.md"
            ],

            # ------------------------------------------------
            # API
            # ------------------------------------------------

            "api": [
                "app/",
                "app/main.py",
                "app/routes/",
                "app/models/",
                "app/services/",
                "app/database/",
                "config/",
                "tests/",
                "docs/",
                "requirements.txt",
                "README.md"
            ],

            # ------------------------------------------------
            # PYTHON
            # ------------------------------------------------

            "python": [
                "src/",
                "src/main.py",
                "src/modules/",
                "config/",
                "data/",
                "tests/",
                "docs/",
                "requirements.txt",
                "README.md"
            ],

            # ------------------------------------------------
            # GENERAL
            # ------------------------------------------------

            "general": [
                "src/",
                "src/main.py",
                "config/",
                "data/",
                "tests/",
                "docs/",
                "README.md"
            ]
        }

        return structures.get(
            project_type,
            structures["general"]
        )

    # ======================================================
    # FILE CONTENT
    # ======================================================

    def default_content(
        self,
        relative_path,
        project_name,
        project_type
    ):

        path = relative_path.lower()

        if path.endswith("readme.md"):

            return (
                f"# {project_name}\n\n"
                f"Nitron generated project.\n\n"
                f"Project type: {project_type}\n"
            )

        if path.endswith("requirements.txt"):
            return ""

        if path.endswith("schema.sql"):

            return (
                "-- Nitron database schema\n"
            )

        if path.endswith("androidmanifest.xml"):

            return """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <application
        android:label="Nitron App">

    </application>

</manifest>
"""

        if path.endswith("index.html"):

            return f"""<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">

    <title>{project_name}</title>

    <link rel="stylesheet"
          href="css/style.css">
</head>

<body>

    <main id="app">
        <h1>{project_name}</h1>
    </main>

    <script src="js/app.js"></script>

</body>
</html>
"""

        if path.endswith("style.css"):

            return """* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, sans-serif;
}

main {
    padding: 30px;
}
"""

        if path.endswith("app.js"):

            return """console.log("Nitron project started.");
"""

        if path.endswith("main.py"):

            return f'''"""
{project_name}
Generated by Nitron.
Project type: {project_type}
"""


def main():
    print("{project_name} is ready.")


if __name__ == "__main__":
    main()
'''

        if path.endswith(".py"):

            return (
                '"""Nitron generated Python module."""\n'
            )

        if path.endswith(".gradle"):

            return (
                "// Nitron Android project configuration\n"
            )

        return ""

    # ======================================================
    # CREATE PROJECT
    # ======================================================

    def create_structure(
        self,
        request,
        project_name=None
    ):

        project_type = self.detect_type(
            request
        )

        if not project_name:

            project_name = self.detect_name(
                request
            )

        project_name = self.clean_name(
            project_name
        )

        project_path = (
            self.root / project_name
        )

        project_path.mkdir(
            parents=True,
            exist_ok=True
        )

        created = []

        files = self.structure(
            project_type
        )

        for relative in files:

            target = (
                project_path / relative
            )

            # Directory
            if relative.endswith("/"):

                target.mkdir(
                    parents=True,
                    exist_ok=True
                )

                created.append(
                    relative
                )

                continue

            target.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            if not target.exists():

                content = self.default_content(
                    relative,
                    project_name,
                    project_type
                )

                target.write_text(
                    content,
                    encoding="utf-8"
                )

            created.append(
                relative
            )

        return {
            "success": True,
            "project": project_name,
            "type": project_type,
            "path": str(project_path),
            "files": created
        }

    # ======================================================
    # BUILD
    # ======================================================

    def build(
        self,
        request,
        project_name=None
    ):

        return self.create_structure(
            request,
            project_name
        )


# ==========================================================
# DIRECT TEST
# ==========================================================

if __name__ == "__main__":

    builder = UniversalBuilder()

    print("=" * 60)
    print("NITRON UNIVERSAL BUILDER")
    print("=" * 60)

    tests = [
        "build web online store",
        "build android calculator app",
        "build ai chatbot",
        "build game",
        "build python program"
    ]

    for request in tests:

        result = builder.build(request)

        print()
        print(
            request
        )
        print(
            "Type:",
            result["type"]
        )
        print(
            "Project:",
            result["project"]
        )
        print(
            "Location:",
            result["path"]
        )
