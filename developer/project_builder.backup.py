# ==========================================================
# NITRON UNIVERSAL PROJECT BUILDER v1.0
# ==========================================================

from pathlib import Path
import re


class ProjectBuilder:

    def __init__(self):

        self.root = (
            Path.home()
            / "Nitron"
            / "GeneratedProjects"
        )

        self.root.mkdir(
            parents=True,
            exist_ok=True
        )

    # ======================================================
    # PROJECT TYPE DETECTION
    # ======================================================

    def detect_type(self, request):

        text = request.lower()

        if any(x in text for x in [
            "website",
            "web",
            "frontend",
            "backend",
            "full stack",
            "fullstack"
        ]):
            return "Web"

        if any(x in text for x in [
            "android",
            "apk",
            "android app"
        ]):
            return "Android"

        if any(x in text for x in [
            "ai",
            "artificial intelligence",
            "machine learning",
            "chatbot",
            "assistant"
        ]):
            return "AI"

        if any(x in text for x in [
            "game",
            "gaming"
        ]):
            return "Games"

        if any(x in text for x in [
            "api",
            "rest api",
            "backend api"
        ]):
            return "APIs"

        if any(x in text for x in [
            "javascript",
            "js"
        ]):
            return "JavaScript"

        if any(x in text for x in [
            "typescript",
            "ts"
        ]):
            return "TypeScript"

        if any(x in text for x in [
            "python",
            "calculator",
            "script"
        ]):
            return "Python"

        if any(x in text for x in [
            "desktop",
            "pc",
            "computer app"
        ]):
            return "Desktop"

        if any(x in text for x in [
            "mobile",
            "phone app"
        ]):
            return "Mobile"

        return "Other"

    # ======================================================
    # PROJECT NAME
    # ======================================================

    def project_name(self, request):

        text = request.lower()

        patterns = [
            r"build (.+)",
            r"create (.+)",
            r"make (.+)",
            r"develop (.+)"
        ]

        name = None

        for pattern in patterns:

            match = re.search(
                pattern,
                text
            )

            if match:

                name = match.group(1)
                break

        if not name:
            name = "NitronProject"

        name = re.sub(
            r"[^a-zA-Z0-9_-]+",
            "_",
            name
        )

        name = name.strip("_")

        if not name:
            name = "NitronProject"

        return name[:80]

    # ======================================================
    # CREATE DIRECTORY
    # ======================================================

    def create_directory(
        self,
        request
    ):

        project_type = self.detect_type(
            request
        )

        name = self.project_name(
            request
        )

        project_path = (
            self.root
            / project_type
            / name
        )

        project_path.mkdir(
            parents=True,
            exist_ok=True
        )

        return {
            "success": True,
            "type": project_type,
            "name": name,
            "path": str(project_path)
        }

    # ======================================================
    # WEB STRUCTURE
    # ======================================================

    def create_web_structure(
        self,
        project_path
    ):

        folders = [
            "frontend",
            "frontend/src",
            "frontend/public",
            "frontend/components",
            "frontend/pages",
            "frontend/assets",
            "backend",
            "backend/api",
            "backend/routes",
            "backend/models",
            "backend/services",
            "backend/database",
            "backend/config",
            "docs",
            "tests"
        ]

        self._folders(
            project_path,
            folders
        )

    # ======================================================
    # AI STRUCTURE
    # ======================================================

    def create_ai_structure(
        self,
        project_path
    ):

        folders = [
            "app",
            "app/models",
            "app/agents",
            "app/tools",
            "app/memory",
            "app/api",
            "app/config",
            "data",
            "models",
            "prompts",
            "tests",
            "docs"
        ]

        self._folders(
            project_path,
            folders
        )

    # ======================================================
    # ANDROID STRUCTURE
    # ======================================================

    def create_android_structure(
        self,
        project_path
    ):

        folders = [
            "app",
            "app/src",
            "app/src/main",
            "app/src/main/java",
            "app/src/main/res",
            "app/src/main/res/drawable",
            "app/src/main/res/layout",
            "app/src/main/res/values",
            "app/src/test",
            "gradle"
        ]

        self._folders(
            project_path,
            folders
        )

    # ======================================================
    # PYTHON STRUCTURE
    # ======================================================

    def create_python_structure(
        self,
        project_path
    ):

        folders = [
            "src",
            "tests",
            "config",
            "data",
            "docs"
        ]

        self._folders(
            project_path,
            folders
        )

    # ======================================================
    # GAME STRUCTURE
    # ======================================================

    def create_game_structure(
        self,
        project_path
    ):

        folders = [
            "assets",
            "assets/images",
            "assets/audio",
            "assets/fonts",
            "src",
            "src/entities",
            "src/scenes",
            "src/systems",
            "tests",
            "docs"
        ]

        self._folders(
            project_path,
            folders
        )

    # ======================================================
    # GENERIC STRUCTURE
    # ======================================================

    def create_generic_structure(
        self,
        project_path
    ):

        folders = [
            "src",
            "tests",
            "config",
            "data",
            "docs"
        ]

        self._folders(
            project_path,
            folders
        )

    # ======================================================
    # INTERNAL FOLDER CREATOR
    # ======================================================

    def _folders(
        self,
        project_path,
        folders
    ):

        for folder in folders:

            (
                Path(project_path)
                / folder
            ).mkdir(
                parents=True,
                exist_ok=True
            )

    # ======================================================
    # BUILD
    # ======================================================

    def build(
        self,
        request
    ):

        result = self.create_directory(
            request
        )

        project_path = Path(
            result["path"]
        )

        project_type = result["type"]

        if project_type == "Web":

            self.create_web_structure(
                project_path
            )

        elif project_type == "AI":

            self.create_ai_structure(
                project_path
            )

        elif project_type == "Android":

            self.create_android_structure(
                project_path
            )

        elif project_type == "Python":

            self.create_python_structure(
                project_path
            )

        elif project_type == "Games":

            self.create_game_structure(
                project_path
            )

        else:

            self.create_generic_structure(
                project_path
            )

        return result


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("NITRON UNIVERSAL PROJECT BUILDER v1.0")
    print("=" * 60)

    builder = ProjectBuilder()

    examples = [
        "build web store",
        "build AI assistant",
        "build Android app",
        "build Python calculator",
        "build game"
    ]

    for request in examples:

        result = builder.build(
            request
        )

        print()
        print("Request:", request)
        print("Type:", result["type"])
        print("Project:", result["name"])
        print("Path:", result["path"])

    print()
    print("=" * 60)
