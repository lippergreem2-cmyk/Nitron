cd ~/Nitron
cat > developer/project_builder.py <<'PY'
# ==========================================================
# NITRON UNIVERSAL PROJECT BUILDER v1.0
# Web + App + AI + General Projects
# ==========================================================

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
PROJECTS_DIR = ROOT / "GeneratedProjects"


# ==========================================================
# PROJECT TYPES
# ==========================================================

PROJECT_TYPES = {
    "web": "web",
    "website": "web",
    "web app": "web",

    "app": "app",
    "application": "app",
    "mobile app": "app",

    "ai": "ai",
    "artificial intelligence": "ai",
    "ai app": "ai",

    "game": "game",
    "software": "software",
    "project": "software",
}


# ==========================================================
# NAME CLEANING
# ==========================================================

def clean_name(text):

    text = text.strip()

    text = re.sub(
        r"[^a-zA-Z0-9_\- ]+",
        "",
        text
    )

    text = re.sub(
        r"\s+",
        "_",
        text
    )

    return text.strip("_") or "NitronProject"


# ==========================================================
# TYPE DETECTION
# ==========================================================

def detect_type(command):

    command = command.lower().strip()

    for keyword, project_type in sorted(
        PROJECT_TYPES.items(),
        key=lambda item: len(item[0]),
        reverse=True
    ):

        if command.startswith("build " + keyword):
            return project_type

        if command.startswith("create " + keyword):
            return project_type

        if command.startswith("make " + keyword):
            return project_type

    return "software"


# ==========================================================
# REQUEST EXTRACTION
# ==========================================================

def extract_request(command):

    command = command.strip()

    patterns = [
        r"^build\s+",
        r"^create\s+",
        r"^make\s+",
    ]

    result = command

    for pattern in patterns:

        result = re.sub(
            pattern,
            "",
            result,
            count=1,
            flags=re.IGNORECASE
        )

        break

    return result.strip()


# ==========================================================
# PROJECT NAME
# ==========================================================

def make_project_name(request, project_type):

    words = request.split()

    if not words:

        return "NitronProject"

    ignored = {
        "a",
        "an",
        "the",
        "for",
        "with",
        "using",
        "in",
        "on"
    }

    words = [
        word
        for word in words
        if word.lower() not in ignored
    ]

    name = " ".join(words[:5])

    name = clean_name(name)

    if not name:

        name = "NitronProject"

    return name


# ==========================================================
# FOLDER STRUCTURE
# ==========================================================

def create_structure(
    project_path,
    project_type
):

    folders = []

    if project_type == "web":

        folders = [
            "frontend",
            "frontend/src",
            "frontend/src/components",
            "frontend/src/pages",
            "frontend/src/assets",
            "frontend/public",

            "backend",
            "backend/api",
            "backend/routes",
            "backend/services",
            "backend/models",
            "backend/database",
            "backend/config",

            "database",
            "docs",
            "tests"
        ]

    elif project_type == "app":

        folders = [
            "app",
            "app/src",
            "app/src/components",
            "app/src/screens",
            "app/src/services",
            "app/src/models",
            "app/src/utils",
            "app/assets",

            "backend",
            "backend/api",
            "backend/services",
            "backend/database",

            "tests",
            "docs"
        ]

    elif project_type == "ai":

        folders = [
            "ai",
            "ai/models",
            "ai/prompts",
            "ai/agents",
            "ai/tools",
            "ai/memory",
            "ai/services",

            "backend",
            "backend/api",
            "backend/routes",
            "backend/services",
            "backend/database",
            "backend/config",

            "data",
            "tests",
            "docs"
        ]

    elif project_type == "game":

        folders = [
            "src",
            "src/assets",
            "src/scenes",
            "src/entities",
            "src/systems",
            "src/ui",

            "config",
            "tests",
            "docs"
        ]

    else:

        folders = [
            "src",
            "src/core",
            "src/services",
            "src/utils",

            "config",
            "data",
            "tests",
            "docs"
        ]

    for folder in folders:

        path = project_path / folder

        path.mkdir(
            parents=True,
            exist_ok=True
        )

    return folders


# ==========================================================
# README
# ==========================================================

def create_readme(
    project_path,
    project_name,
    project_type,
    request
):

    readme = f"""# {project_name}

Generated by Nitron Universal Project Builder.

## Type

{project_type}

## Request

{request}

## Structure

This project was initialized by Nitron.

The AI code generator will create the implementation
inside the appropriate folders.

## Project

{project_name}
"""

    path = project_path / "README.md"

    path.write_text(
        readme,
        encoding="utf-8"
    )

    return str(path)


# ==========================================================
# UNIVERSAL BUILDER
# ==========================================================

class UniversalProjectBuilder:

    def __init__(self):

        PROJECTS_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

    # ======================================================
    # CREATE EMPTY STRUCTURE
    # ======================================================

    def create_project(
        self,
        request,
        project_type=None,
        project_name=None
    ):

        if not request:

            raise ValueError(
                "Project request cannot be empty."
            )

        if project_type is None:

            project_type = detect_type(
                request
            )

        if project_name is None:

            project_name = make_project_name(
                request,
                project_type
            )

        project_name = clean_name(
            project_name
        )

        project_path = (
            PROJECTS_DIR /
            project_name
        )

        project_path.mkdir(
            parents=True,
            exist_ok=True
        )

        folders = create_structure(
            project_path,
            project_type
        )

        readme = create_readme(
            project_path,
            project_name,
            project_type,
            request
        )

        return {
            "success": True,
            "project": project_name,
            "type": project_type,
            "request": request,
            "path": str(project_path),
            "folders": folders,
            "readme": readme
        }

    # ======================================================
    # CREATE + AI GENERATE
    # ======================================================

    def build(
        self,
        request,
        project_type=None,
        project_name=None
    ):

        structure = self.create_project(
            request,
            project_type,
            project_name
        )

        try:

            from developer.ai_code_generator import (
                AICodeGenerator
            )

            ai = AICodeGenerator()

        except Exception as error:

            structure["ai_error"] = str(error)

            return structure

        try:

            result = ai.generate(
                request=request,
                project_name=structure["project"],
                existing_project=structure["path"]
            )

            structure["generation"] = result

            return structure

        except Exception as error:

            structure["ai_error"] = str(error)

            return structure


# ==========================================================
# COMMAND HELPER
# ==========================================================

def build_project(command):

    project_type = detect_type(
        command
    )

    request = extract_request(
        command
    )

    builder = UniversalProjectBuilder()

    return builder.build(
        request=request,
        project_type=project_type
    )


# ==========================================================
# DIRECT TEST
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("NITRON UNIVERSAL PROJECT BUILDER v1.0")
    print("=" * 60)

    builder = UniversalProjectBuilder()

    examples = [
        "build web ecommerce store",
        "build app calculator",
        "build ai assistant",
        "build game racing game"
    ]

    for example in examples:

        print()
        print("Example:", example)

        project_type = detect_type(
            example
        )

        request = extract_request(
            example
        )

        print("Type:", project_type)
        print("Request:", request)

    print()
    print("=" * 60)
PY
