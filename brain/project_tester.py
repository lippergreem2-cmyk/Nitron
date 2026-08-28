"""
Nitron Project Tester

Runs safe, bounded tests against generated projects.
"""

from pathlib import Path
import subprocess
import sys


class ProjectTester:

    def test(self, project):

        if not isinstance(project, dict):
            return {
                "tested": False,
                "passed": False,
                "checks": [],
                "errors": ["Invalid project result."]
            }

        directory = project.get("directory")

        if not directory:
            return {
                "tested": False,
                "passed": False,
                "checks": [],
                "errors": ["Project directory is missing."]
            }

        root = Path(directory)

        if not root.exists():
            return {
                "tested": False,
                "passed": False,
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
        # PYTHON
        # ==================================================

        if language == "python":

            main = root / "main.py"

            if not main.exists():
                errors.append(
                    "No main.py found for Python project."
                )

            else:
                try:
                    result = subprocess.run(
                        [
                            sys.executable,
                            "-m",
                            "py_compile",
                            main.name,
                        ],
                        cwd=str(root),
                        capture_output=True,
                        text=True,
                        timeout=10,
                    )

                    if result.returncode == 0:
                        checks.append(
                            "Python main.py compiled successfully"
                        )
                    else:
                        errors.append(
                            "Python compilation failed: "
                            + (
                                result.stderr.strip()
                                or "unknown error"
                            )
                        )

                except subprocess.TimeoutExpired:
                    errors.append(
                        "Python compilation timed out."
                    )

                except Exception as error:
                    errors.append(
                        f"Python test error: {error}"
                    )

        # ==================================================
        # JAVASCRIPT / NODE.JS
        # ==================================================

        elif language == "javascript":

            main = root / "index.js"

            if not main.exists():
                errors.append(
                    "No index.js found for JavaScript project."
                )

            else:
                try:
                    result = subprocess.run(
                        [
                            "node",
                            main.name,
                        ],
                        cwd=str(root),
                        capture_output=True,
                        text=True,
                        timeout=10,
                    )

                    if result.returncode == 0:
                        checks.append(
                            "JavaScript index.js executed successfully"
                        )
                    else:
                        errors.append(
                            "JavaScript execution failed: "
                            + (
                                result.stderr.strip()
                                or "unknown error"
                            )
                        )

                except FileNotFoundError:
                    errors.append(
                        "Node.js runtime is not installed."
                    )

                except subprocess.TimeoutExpired:
                    errors.append(
                        "JavaScript execution timed out."
                    )

                except Exception as error:
                    errors.append(
                        f"JavaScript test error: {error}"
                    )

        # ==================================================
        # RUST
        # ==================================================

        elif language == "rust":

            main = root / "main.rs"

            if not main.exists():
                errors.append(
                    "No main.rs found for Rust project."
                )

            else:
                try:
                    output = root / ".nitron_rust_test"

                    result = subprocess.run(
                        [
                            "rustc",
                            main.name,
                            "-o",
                            str(output),
                        ],
                        cwd=str(root),
                        capture_output=True,
                        text=True,
                        timeout=15,
                    )

                    if result.returncode != 0:
                        errors.append(
                            "Rust compilation failed: "
                            + (
                                result.stderr.strip()
                                or "unknown error"
                            )
                        )
                    else:
                        checks.append(
                            "Rust main.rs compiled successfully"
                        )

                        try:
                            run_result = subprocess.run(
                                [str(output)],
                                cwd=str(root),
                                capture_output=True,
                                text=True,
                                timeout=10,
                            )

                            if run_result.returncode == 0:
                                checks.append(
                                    "Rust program executed successfully"
                                )
                            else:
                                errors.append(
                                    "Rust program execution failed: "
                                    + (
                                        run_result.stderr.strip()
                                        or "unknown error"
                                    )
                                )

                        except subprocess.TimeoutExpired:
                            errors.append(
                                "Rust program execution timed out."
                            )

                        except Exception as error:
                            errors.append(
                                f"Rust execution error: {error}"
                            )

                        finally:
                            try:
                                if output.exists():
                                    output.unlink()
                            except Exception:
                                pass

                except FileNotFoundError:
                    errors.append(
                        "Rust compiler (rustc) is not installed."
                    )

                except subprocess.TimeoutExpired:
                    errors.append(
                        "Rust compilation timed out."
                    )

                except Exception as error:
                    errors.append(
                        f"Rust test error: {error}"
                    )

        # ==================================================
        # WEBSITE
        # ==================================================

        elif (
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

                    required = [
                        "<html",
                        "<head",
                        "<body",
                        "</html>",
                    ]

                    missing = [
                        item
                        for item in required
                        if item.lower() not in html.lower()
                    ]

                    if missing:
                        errors.append(
                            "Website missing required "
                            f"HTML elements: {missing}"
                        )
                    else:
                        checks.append(
                            "Website HTML structure passed"
                        )

                except Exception as error:
                    errors.append(
                        f"Website test error: {error}"
                    )

        # ==================================================
        # KOTLIN / ANDROID
        # ==================================================

        elif (
            language == "kotlin"
            or project_type == "android_app"
        ):

            kotlin_files = list(
                root.rglob("*.kt")
            )

            if not kotlin_files:
                errors.append(
                    "No Kotlin source files found."
                )
            else:
                checks.append(
                    f"Kotlin test source detected: "
                    f"{len(kotlin_files)} file(s)"
                )

                # Do not attempt a full Android build here.
                # A generated project may not contain a complete
                # Gradle environment yet.
                checks.append(
                    "Android build execution deferred"
                )

        # ==================================================
        # UNKNOWN PROJECT
        # ==================================================

        else:

            checks.append(
                "No executable test defined for this project type"
            )

        return {
            "tested": True,
            "passed": len(errors) == 0,
            "checks": checks,
            "errors": errors,
        }


tester = ProjectTester()
