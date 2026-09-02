def learned_programming(command):
    """
    Nitron generic programming capability.

    Supports:
      - analyze <file.py>
      - debug <file.py>
      - test <file.py>
      - build <file.py>
      - write/create/generate/program/code requests
      - explain programming requests

    Uses the learned skill registry to determine the programming
    capability/language.
    """

    from pathlib import Path
    import ast
    import py_compile
    import re
    import subprocess
    import sys
    import tempfile

    from brain.skill_registry import best_for_task
    from brain.reasoning import reasoning

    # ============================================================
    # INPUT NORMALIZATION
    # ============================================================

    command_text_raw = str(command).strip()
    command_text = command_text_raw.lower()

    if not command_text_raw:
        return {
            "success": False,
            "capability": "programming",
            "language": "",
            "operation": None,
            "message": "No programming command was provided.",
        }

    # ============================================================
    # FIND LEARNED PROGRAMMING CAPABILITY
    # ============================================================

    skill = best_for_task(command)

    # File-oriented commands may not contain enough capability
    # words for registry matching.
    if not skill:
        if (
            re.search(
                r"\b(analyze|analyse|debug|test|build|check|inspect|"
                r"compile|run)\b",
                command_text
            )
            and ".py" in command_text
        ):
            from brain.skill_registry import get_skill

            candidates = [
                "Python programming",
                "Python",
            ]

            for candidate in candidates:
                try:
                    skill = get_skill(candidate)
                except Exception:
                    skill = None

                if skill:
                    break

    if not skill:
        return {
            "success": False,
            "capability": "programming",
            "language": "",
            "operation": None,
            "message": "No learned programming capability matched.",
        }

    capability_type = str(
        skill.get("capability_type", "")
    ).strip().lower()

    if capability_type != "programming":
        return {
            "success": False,
            "capability": "programming",
            "language": str(skill.get("name", "")),
            "operation": None,
            "message": (
                "Matched capability is not a programming capability."
            ),
        }

    # ============================================================
    # LANGUAGE NORMALIZATION
    # ============================================================

    language_aliases = {
        "python programming": "python",
        "python": "python",

        "javascript programming": "javascript",
        "javascript": "javascript",
        "js": "javascript",

        "typescript programming": "typescript",
        "typescript": "typescript",
        "ts": "typescript",

        "rust programming": "rust",
        "rust": "rust",

        "kotlin programming": "kotlin",
        "kotlin": "kotlin",

        "java programming": "java",
        "java": "java",

        "bash programming": "bash",
        "bash": "bash",
        "shell": "bash",

        "c++ programming": "cpp",
        "c++": "cpp",
        "cpp": "cpp",

        "c# programming": "csharp",
        "c#": "csharp",
        "csharp": "csharp",

        "go programming": "go",
        "go": "go",
        "golang": "go",
    }

    language_name = str(
        skill.get("name", "")
    ).strip().lower()

    language = language_aliases.get(
        language_name,
        language_name
    )

    # ============================================================
    # OPERATION DETECTION
    # ============================================================

    operation = None

    operation_patterns = [
        (r"\b(analyze|analyse|inspect)\b", "analyze"),
        (r"\b(debug|diagnose)\b", "debug"),
        (r"\b(test|tests|testing)\b", "test"),
        (r"\b(build|compile|compilation)\b", "build"),
        (r"\b(write|writing)\b", "write"),
        (r"\b(create|make|generate|develop)\b", "create"),
        (r"\b(program|programming)\b", "create"),
        (r"\b(code|coding)\b", "create"),
        (r"\b(explain|describe|teach)\b", "explain"),
    ]

    for pattern, canonical in operation_patterns:
        if re.search(pattern, command_text):
            operation = canonical
            break

    # If no explicit operation exists, treat it as a programming
    # creation request rather than returning an unusable response.
    if operation is None:
        operation = "create"

    # ============================================================
    # PYTHON FILE EXTRACTION
    # ============================================================

    def extract_python_file(text):
        """
        Extract a likely Python filename/path from a command.
        """

        matches = re.findall(
            r"""(?:
                ["']([^"']+\.py)["']
                |
                (?<![\w.-])([~/A-Za-z0-9_./-]+\.py)
            )""",
            text,
            flags=re.IGNORECASE | re.VERBOSE,
        )

        candidates = []

        for quoted, unquoted in matches:
            candidate = quoted or unquoted

            if candidate:
                candidates.append(candidate)

        if not candidates:
            return None

        # Prefer an existing file.
        for candidate in reversed(candidates):
            path = Path(candidate).expanduser()

            if path.exists() and path.is_file():
                return candidate

        return candidates[-1]

    file_name = extract_python_file(command_text_raw)

    # ============================================================
    # RESOLVE FILE PATH
    # ============================================================

    def resolve_file(path_text):
        if not path_text:
            return None

        path = Path(path_text).expanduser()

        if not path.is_absolute():
            path = Path.cwd() / path

        try:
            return path.resolve()
        except Exception:
            return path

    file_path = resolve_file(file_name)

    # ============================================================
    # PYTHON SOURCE ANALYSIS
    # ============================================================

    if language == "python" and operation in {
        "analyze",
        "debug",
    }:

        if not file_name:
            return {
                "success": False,
                "capability": "programming",
                "language": "python",
                "operation": operation,
                "message": (
                    "No Python source file was specified. "
                    "Example: analyze brain/reasoning.py"
                ),
            }

        if not file_path or not file_path.exists():
            return {
                "success": False,
                "capability": "programming",
                "language": "python",
                "operation": operation,
                "file": file_name,
                "analyzed": operation == "analyze",
                "debugged": operation == "debug",
                "syntax_valid": False,
                "functions": [],
                "async_functions": [],
                "classes": [],
                "imports": [],
                "decorators": [],
                "lines": 0,
                "errors": [{
                    "type": "FileNotFoundError",
                    "message": f"Python file not found: {file_name}",
                }],
            }

        # --------------------------------------------------------
        # READ SOURCE
        # --------------------------------------------------------

        try:
            source = file_path.read_text(
                encoding="utf-8"
            )
        except Exception as exc:
            return {
                "success": False,
                "capability": "programming",
                "language": "python",
                "operation": operation,
                "file": file_name,
                "analyzed": False,
                "debugged": False,
                "syntax_valid": False,
                "functions": [],
                "async_functions": [],
                "classes": [],
                "imports": [],
                "decorators": [],
                "lines": 0,
                "errors": [{
                    "type": type(exc).__name__,
                    "message": str(exc),
                }],
            }

        # --------------------------------------------------------
        # BASIC SOURCE METRICS
        # --------------------------------------------------------

        lines = source.splitlines()

        non_empty_lines = [
            line for line in lines
            if line.strip()
        ]

        comments = [
            line for line in lines
            if line.strip().startswith("#")
        ]

        functions = []
        async_functions = []
        classes = []
        imports = []
        decorators = []

        syntax_valid = True
        errors = []

        # --------------------------------------------------------
        # AST ANALYSIS
        # --------------------------------------------------------

        try:
            tree = ast.parse(
                source,
                filename=str(file_path)
            )

            for node in ast.walk(tree):

                if isinstance(node, ast.FunctionDef):
                    functions.append(node.name)

                    for decorator in node.decorator_list:
                        try:
                            decorators.append(
                                ast.unparse(decorator)
                            )
                        except Exception:
                            decorators.append(
                                "<decorator>"
                            )

                elif isinstance(node, ast.AsyncFunctionDef):
                    async_functions.append(node.name)

                    for decorator in node.decorator_list:
                        try:
                            decorators.append(
                                ast.unparse(decorator)
                            )
                        except Exception:
                            decorators.append(
                                "<decorator>"
                            )

                elif isinstance(node, ast.ClassDef):
                    classes.append(node.name)

                    for decorator in node.decorator_list:
                        try:
                            decorators.append(
                                ast.unparse(decorator)
                            )
                        except Exception:
                            decorators.append(
                                "<decorator>"
                            )

                elif isinstance(node, ast.Import):
                    for item in node.names:
                        imports.append(item.name)

                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)

        except SyntaxError as exc:
            syntax_valid = False

            error = {
                "type": "SyntaxError",
                "message": exc.msg,
            }

            if exc.lineno is not None:
                error["line"] = exc.lineno

            if exc.offset is not None:
                error["column"] = exc.offset

            if exc.text:
                error["source"] = exc.text.rstrip()

            errors.append(error)

        except Exception as exc:
            syntax_valid = False

            errors.append({
                "type": type(exc).__name__,
                "message": str(exc),
            })

        # Remove duplicates while preserving order.
        functions = list(dict.fromkeys(functions))
        async_functions = list(dict.fromkeys(async_functions))
        classes = list(dict.fromkeys(classes))
        imports = list(dict.fromkeys(imports))
        decorators = list(dict.fromkeys(decorators))

        result = {
            "success": True,
            "capability": "programming",
            "language": "python",
            "operation": operation,
            "file": file_name,
            "path": str(file_path),
            "analyzed": operation == "analyze",
            "debugged": operation == "debug",
            "syntax_valid": syntax_valid,

            "lines": len(lines),
            "non_empty_lines": len(non_empty_lines),
            "comment_lines": len(comments),

            "functions": functions,
            "async_functions": async_functions,
            "classes": classes,
            "imports": imports,
            "decorators": decorators,

            "errors": errors,
        }

        # --------------------------------------------------------
        # DEBUG HINTS
        # --------------------------------------------------------

        if operation == "debug":

            hints = []

            if not syntax_valid:
                hints.append(
                    "Fix the reported syntax error before running the file."
                )

            if syntax_valid and not functions and not classes:
                hints.append(
                    "The file contains no top-level functions or classes."
                )

            if "except:" in source:
                hints.append(
                    "A bare 'except:' was detected; consider catching "
                    "a specific exception."
                )

            if re.search(
                r"\b(eval|exec)\s*\(",
                source
            ):
                hints.append(
                    "Dynamic eval/exec usage was detected; review it carefully."
                )

            result["debug_hints"] = hints

        return result

    # ============================================================
    # REAL PYTHON BUILD / COMPILE CHECK
    # ============================================================

    if language == "python" and operation == "build":

        if not file_name:
            return {
                "success": False,
                "capability": "programming",
                "language": "python",
                "operation": "build",
                "message": (
                    "No Python source file was specified. "
                    "Example: build brain/reasoning.py"
                ),
            }

        if not file_path or not file_path.exists():
            return {
                "success": False,
                "capability": "programming",
                "language": "python",
                "operation": "build",
                "file": file_name,
                "built": False,
                "message": f"Python file not found: {file_name}",
            }

        try:
            py_compile.compile(
                str(file_path),
                doraise=True,
            )

            return {
                "success": True,
                "capability": "programming",
                "language": "python",
                "operation": "build",
                "file": file_name,
                "built": True,
                "syntax_valid": True,
                "message": (
                    f"Python compilation check passed for {file_name}."
                ),
            }

        except py_compile.PyCompileError as exc:

            return {
                "success": False,
                "capability": "programming",
                "language": "python",
                "operation": "build",
                "file": file_name,
                "built": False,
                "syntax_valid": False,
                "errors": [{
                    "type": "PyCompileError",
                    "message": str(exc),
                }],
            }

        except Exception as exc:

            return {
                "success": False,
                "capability": "programming",
                "language": "python",
                "operation": "build",
                "file": file_name,
                "built": False,
                "errors": [{
                    "type": type(exc).__name__,
                    "message": str(exc),
                }],
            }

    # ============================================================
    # REAL PYTHON TESTING
    # ============================================================

    if language == "python" and operation == "test":

        if not file_name:
            return {
                "success": False,
                "capability": "programming",
                "language": "python",
                "operation": "test",
                "message": (
                    "No Python test file was specified. "
                    "Example: test tests/test_brain.py"
                ),
            }

        if not file_path or not file_path.exists():
            return {
                "success": False,
                "capability": "programming",
                "language": "python",
                "operation": "test",
                "file": file_name,
                "tested": False,
                "message": f"Python file not found: {file_name}",
            }

        # First perform a syntax check.
        try:
            ast.parse(
                file_path.read_text(
                    encoding="utf-8"
                ),
                filename=str(file_path)
            )
        except SyntaxError as exc:

            return {
                "success": False,
                "capability": "programming",
                "language": "python",
                "operation": "test",
                "file": file_name,
                "tested": False,
                "syntax_valid": False,
                "errors": [{
                    "type": "SyntaxError",
                    "message": exc.msg,
                    "line": exc.lineno,
                    "column": exc.offset,
                }],
            }

        # --------------------------------------------------------
        # RUN ONLY UNITTEST DISCOVERY.
        #
        # This does NOT blindly execute an arbitrary Python
        # command supplied by the user.
        # --------------------------------------------------------

        try:
            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "unittest",
                    file_name,
                    "-v",
                ],
                cwd=str(Path.cwd()),
                capture_output=True,
                text=True,
                timeout=30,
            )

            stdout = completed.stdout.strip()
            stderr = completed.stderr.strip()

            return {
                "success": completed.returncode == 0,
                "capability": "programming",
                "language": "python",
                "operation": "test",
                "file": file_name,
                "tested": True,
                "syntax_valid": True,
                "passed": completed.returncode == 0,
                "return_code": completed.returncode,
                "stdout": stdout,
                "stderr": stderr,
                "message": (
                    "Python tests passed."
                    if completed.returncode == 0
                    else "Python tests failed."
                ),
            }

        except subprocess.TimeoutExpired:

            return {
                "success": False,
                "capability": "programming",
                "language": "python",
                "operation": "test",
                "file": file_name,
                "tested": False,
                "syntax_valid": True,
                "timeout": True,
                "message": (
                    "Testing stopped because it exceeded "
                    "the 30-second limit."
                ),
            }

        except Exception as exc:

            return {
                "success": False,
                "capability": "programming",
                "language": "python",
                "operation": "test",
                "file": file_name,
                "tested": False,
                "errors": [{
                    "type": type(exc).__name__,
                    "message": str(exc),
                }],
            }

    # ============================================================
    # PROJECT GENERATION
    # ============================================================

    if operation in {
        "write",
        "create",
    }:

        project_request = (
            f"{command_text_raw}. "
            f"Use {language} programming. "
            f"Generate a complete working project."
        )

        try:
            generated = reasoning.generate_project(
                project_request
            )

            if isinstance(generated, dict):
                generated["capability"] = "programming"
                generated["language"] = language
                generated["operation"] = operation

                return generated

            return {
                "success": True,
                "capability": "programming",
                "language": language,
                "operation": operation,
                "result": generated,
            }

        except Exception as exc:

            return {
                "success": False,
                "capability": "programming",
                "language": language,
                "operation": operation,
                "message": str(exc),
            }

    # ============================================================
    # EXPLANATION
    # ============================================================

    if operation == "explain":

        return {
            "success": True,
            "capability": "programming",
            "language": language,
            "operation": "explain",
            "command": command_text_raw,
            "abilities": skill.get(
                "abilities",
                []
            ),
            "message": (
                f"Programming explanation selected for {language}."
            ),
        }

    # ============================================================
    # FALLBACK
    # ============================================================

    return {
        "success": True,
        "capability": "programming",
        "language": language,
        "operation": operation,
        "command": command_text_raw,
        "abilities": skill.get(
            "abilities",
            []
        ),
        "message": (
            f"Programming operation '{operation}' "
            f"selected for {language}."
        ),
    }
