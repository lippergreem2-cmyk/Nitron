"""
Nitron Project Repair Engine

Attempts safe, local repairs on generated projects after verification.
"""

from pathlib import Path
import re


class ProjectRepair:

    def __init__(self):
        self.name = "Nitron Project Repair Engine"

    def repair(self, project, verification):
        """
        Attempt safe repairs based on verifier errors.

        Returns:
            {
                "repaired": bool,
                "changes": [...],
                "errors": [...]
            }
        """

        result = {
            "repaired": False,
            "changes": [],
            "errors": [],
        }

        if not isinstance(project, dict):
            result["errors"].append(
                "Invalid project data."
            )
            return result

        directory = project.get("directory")

        if not directory:
            result["errors"].append(
                "Project directory is missing."
            )
            return result

        root = Path(directory)

        if not root.exists():
            result["errors"].append(
                f"Project directory does not exist: {root}"
            )
            return result

        if not isinstance(verification, dict):
            result["errors"].append(
                "Invalid verification result."
            )
            return result

        # --------------------------------------------------
        # COLLECT VERIFICATION + TESTING ERRORS
        # --------------------------------------------------

        errors = list(
            verification.get("errors", [])
        )

        testing = verification.get(
            "testing",
            {}
        )

        if isinstance(testing, dict):
            errors.extend(
                testing.get("errors", [])
            )

        if not errors:
            return result

        # Group related errors so one repair is attempted only once.
        repaired_error_types = set()

        for error in errors:

            error_text = str(error)
            lower = error_text.lower()

            if (
                "html tag" in lower
                or "mismatched html" in lower
                or "unclosed html" in lower
                or "unexpected closing html" in lower
            ):
                if "html" in repaired_error_types:
                    continue

                repaired_error_types.add("html")

            self._repair_error(
                root,
                error_text,
                result
            )

        return result

    # --------------------------------------------------
    # ERROR DISPATCH
    # --------------------------------------------------

    def _repair_error(self, root, error, result):

        lower = error.lower()

        # Python syntax errors
        if "python syntax" in lower:
            self._repair_python_syntax(
                root,
                error,
                result
            )
            return

        # HTML structure errors
        if (
            "html tag" in lower
            or "mismatched html" in lower
            or "unclosed html" in lower
            or "unexpected closing html" in lower
        ):
            self._repair_html(
                root,
                error,
                result
            )
            return

        # Missing generated files
        if (
            "file exists" in lower
            or "missing generated file" in lower
            or "no main.py found" in lower
            or "no index.js found" in lower
            or "no index.html" in lower
        ):
            self._repair_missing_file(
                root,
                error,
                result
            )
            return

        result["errors"].append(
            f"Unsupported repair: {error}"
        )

    # --------------------------------------------------
    # PYTHON REPAIR
    # --------------------------------------------------

    def _repair_python_syntax(self, root, error, result):
        """
        Perform conservative Python syntax repairs.

        Currently supports safe repairs such as:
        - missing colon after control statements
        - trailing whitespace normalization
        - final newline normalization
        """

        matches = re.findall(
            r"([A-Za-z0-9_./-]+\.py)\b",
            error
        )

        if not matches:
            result["errors"].append(
                f"Could not identify Python file: {error}"
            )
            return

        filename = matches[0]
        path = root / filename

        if not path.exists():
            result["errors"].append(
                f"Python file not found: {filename}"
            )
            return

        try:
            original = path.read_text(
                encoding="utf-8"
            )

            lines = original.splitlines()
            fixed_lines = []
            changed = False

            # --------------------------------------------------
            # FIX: missing colon after Python statements
            # --------------------------------------------------

            control_pattern = re.compile(
                r"^(\s*)(if|elif|else|for|while|def|class|try|except|finally|with|match|case)\b.*[^: ]$"
            )

            for line in lines:

                stripped = line.strip()

                if (
                    stripped
                    and not stripped.startswith("#")
                    and control_pattern.match(line)
                    and not stripped.endswith(":")
                ):
                    line = line.rstrip() + ":"
                    changed = True

                fixed_lines.append(line)

            # IMPORTANT:
            # Use a REAL newline character here.
            text = "\n".join(
                line.rstrip()
                for line in fixed_lines
            )

            text = text.rstrip() + "\n"

            if text != original:
                changed = True

            if changed:

                path.write_text(
                    text,
                    encoding="utf-8"
                )

                result["repaired"] = True

                result["changes"].append(
                    f"Applied safe Python syntax repair: {filename}"
                )

            else:

                result["errors"].append(
                    f"Could not safely repair Python syntax: {filename}"
                )

        except Exception as exc:

            result["errors"].append(
                f"Python repair failed for {filename}: {exc}"
            )

    # --------------------------------------------------
    # HTML REPAIR
    # --------------------------------------------------

    def _repair_html(self, root, error, result):
        """
        Perform conservative HTML nesting repairs.

        Handles common generated HTML where closing tags
        are missing or appear in the wrong order.
        """

        path = root / "index.html"

        if not path.exists():
            result["errors"].append(
                "HTML file not found: index.html"
            )
            return

        try:
            text = path.read_text(
                encoding="utf-8"
            )

            original = text

            # --------------------------------------------------
            # Repair common missing closing tags.
            # --------------------------------------------------

            replacements = [
                (
                    r"(<p[^>]*>[^<]*?)"
                    r"(</body>)",
                    r"\1</p>\2"
                ),
                (
                    r"(<div[^>]*>[^<]*?)"
                    r"(</body>)",
                    r"\1</div>\2"
                ),
            ]

            for pattern, replacement in replacements:

                text = re.sub(
                    pattern,
                    replacement,
                    text,
                    flags=re.IGNORECASE
                )

            # --------------------------------------------------
            # Normalize final newline.
            # --------------------------------------------------

            text = text.rstrip() + "\n"

            if text != original:

                path.write_text(
                    text,
                    encoding="utf-8"
                )

                result["repaired"] = True

                result["changes"].append(
                    "Applied safe HTML nesting repair: index.html"
                )

            else:

                result["errors"].append(
                    "Could not safely repair HTML: index.html"
                )

        except Exception as exc:

            result["errors"].append(
                f"HTML repair failed: {exc}"
            )

    # --------------------------------------------------
    # MISSING FILE REPAIR
    # --------------------------------------------------

    def _repair_missing_file(self, root, error, result):
        """
        Missing-file repair is intentionally conservative.

        The generator should normally create required files.
        We report the problem rather than inventing source code.
        """

        result["errors"].append(
            f"Missing generated file requires regeneration: {error}"
        )


repair_engine = ProjectRepair()
