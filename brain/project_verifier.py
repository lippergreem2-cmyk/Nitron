"""
Nitron Project Verifier

Checks generated projects after creation and reports
whether their generated files pass basic validation.
"""

from pathlib import Path
import ast
import re


class ProjectVerifier:

    def verify(self, project):

        if not isinstance(project, dict):
            return {
                "verified": False,
                "checks": [],
                "errors": ["Invalid project result."]
            }

        directory = project.get("directory")

        if not directory:
            return {
                "verified": False,
                "checks": [],
                "errors": ["Project directory is missing."]
            }

        root = Path(directory)

        if not root.exists():
            return {
                "verified": False,
                "checks": [],
                "errors": [
                    f"Project directory does not exist: {root}"
                ]
            }

        project_type = (
            project.get("project_type")
            or project.get("type")
        )

        language = project.get("language")

        checks = []
        errors = []

        # ==================================================
        # FILE EXISTENCE
        # ==================================================

        files = project.get("files", [])

        for item in files:

            if not isinstance(item, dict):
                continue

            relative = item.get("path")

            if not relative:
                continue

            path = root / relative

            if path.exists():
                checks.append(
                    f"file exists: {relative}"
                )
            else:
                errors.append(
                    f"missing generated file: {relative}"
                )

        # ==================================================
        # PYTHON
        # ==================================================

        if language == "python":

            python_files = list(root.rglob("*.py"))

            for path in python_files:

                try:
                    source = path.read_text(
                        encoding="utf-8"
                    )

                    ast.parse(source)

                    checks.append(
                        f"python syntax valid: {path.name}"
                    )

                except Exception as error:

                    errors.append(
                        f"python syntax error in "
                        f"{path.name}: {error}"
                    )

        # ==================================================
        # HTML / WEBSITE
        # ==================================================

        if (
            language == "html"
            or project_type == "website"
        ):

            index = root / "index.html"

            if not index.exists():

                errors.append(
                    "Website has no index.html."
                )

            else:

                try:

                    html = index.read_text(
                        encoding="utf-8"
                    )

                    # --------------------------------------------------
                    # BASIC DOCUMENT STRUCTURE
                    # --------------------------------------------------

                    if re.search(
                        r"<html\b",
                        html,
                        re.IGNORECASE
                    ):
                        checks.append(
                            "HTML document structure detected"
                        )
                    else:
                        errors.append(
                            "index.html has no <html> element."
                        )

                    if re.search(
                        r"<body\b",
                        html,
                        re.IGNORECASE
                    ):
                        checks.append(
                            "HTML body detected"
                        )
                    else:
                        errors.append(
                            "index.html has no <body> element."
                        )

                    # --------------------------------------------------
                    # BASIC TAG BALANCE
                    # --------------------------------------------------

                    void_tags = {
                        "area",
                        "base",
                        "br",
                        "col",
                        "embed",
                        "hr",
                        "img",
                        "input",
                        "link",
                        "meta",
                        "param",
                        "source",
                        "track",
                        "wbr",
                    }

                    tags = re.findall(
                        r"<(/?)([A-Za-z][A-Za-z0-9]*)\b[^>]*>",
                        html,
                    )

                    stack = []

                    for closing, tag_name in tags:

                        tag = tag_name.lower()

                        if tag in void_tags:
                            continue

                        if closing:

                            if not stack:

                                errors.append(
                                    f"Unexpected closing HTML tag: </{tag}>"
                                )

                                continue

                            expected = stack.pop()

                            if expected != tag:

                                errors.append(
                                    f"Mismatched HTML tags: "
                                    f"expected </{expected}> "
                                    f"but found </{tag}>"
                                )

                        else:

                            stack.append(tag)

                    if stack:

                        errors.append(
                            "Unclosed HTML tag(s): "
                            + ", ".join(stack)
                        )

                    elif not any(
                        "Unexpected closing HTML tag" in error
                        or "Mismatched HTML tags" in error
                        or "Unclosed HTML tag(s)" in error
                        for error in errors
                    ):

                        checks.append(
                            "HTML tag balance passed"
                        )

                except Exception as error:

                    errors.append(
                        f"HTML verification error: {error}"
                    )

        # ==================================================
        # ANDROID / KOTLIN
        # ==================================================

        if (
            language == "kotlin"
            or project_type == "android_app"
        ):

            kotlin_files = list(
                root.rglob("*.kt")
            )

            if kotlin_files:

                checks.append(
                    f"Kotlin source detected: "
                    f"{len(kotlin_files)} file(s)"
                )

            else:

                errors.append(
                    "No Kotlin source files found."
                )

        # ==================================================
        # FINAL RESULT
        # ==================================================

        return {
            "verified": len(errors) == 0,
            "checks": checks,
            "errors": errors,
        }


verifier = ProjectVerifier()
