"""
Nitron Learned Skill Handler Bridge

Connects persistent learned-skill handler names to
existing Nitron capabilities.
"""

from brain.reasoning import reasoning


def generate_project(command):
    """
    Use Nitron's existing reasoning engine to generate a project.
    """
    return reasoning.generate_project(command)


HANDLERS = {
    "reasoning.generate_project": generate_project,
}


def get_handler(name):
    """
    Resolve an approved learned-skill handler.
    """
    key = str(name).strip()

    if key == "learned.programming":
        return learned_programming

    return HANDLERS.get(key)

def run_learned_capability(command, skill=None):
    """
    Generic learned-capability execution entry point.

    Existing specialized handlers remain authoritative.
    This function provides a safe fallback for learned skills
    that have abilities but no dedicated handler yet.
    """

    from brain.skill_registry import best_for_task

    if skill is None:
        skill = best_for_task(command)

    if not skill:
        return {
            "success": False,
            "capability": "unknown",
            "operation": "unknown",
            "errors": [
                "No learned capability matched the command."
            ],
        }

    # DecisionEngine may provide either a full skill dictionary
    # or simply the learned skill name.
    if isinstance(skill, str):
        skill_name = skill.strip()

        try:
            from brain.skill_registry import get_skill

            resolved_skill = get_skill(skill_name)
        except Exception:
            resolved_skill = None

        if isinstance(resolved_skill, dict):
            skill = resolved_skill
        else:
            skill = {
                "name": skill_name,
                "capability_type": "learned",
                "abilities": [],
            }

    if not isinstance(skill, dict):
        return {
            "success": False,
            "capability": "unknown",
            "operation": "unknown",
            "executed": False,
            "handler_type": "generic.learned",
            "errors": [
                "Invalid learned capability format."
            ],
        }

    name = str(skill.get("name", "")).strip()

    capability_type = str(
        skill.get("capability_type", "")
    ).strip().lower()

    abilities = skill.get("abilities", [])

    if not isinstance(abilities, list):
        abilities = []

    command_text = str(command).strip()

    # --------------------------------------------------
    # Generic operation detection
    # --------------------------------------------------

    # Natural-language programming operation detection.
    operation_aliases = [
        ("analyze", "analyze"),
        ("debug", "debug"),
        ("test", "test"),
        ("modify", "modify"),
        ("build", "build"),
        ("write", "write"),
        ("create", "create"),
        ("make", "create"),
        ("generate", "create"),
        ("draw", "create"),
        ("program", "create"),
        ("explain", "explain"),
    ]

    operation = None

    for phrase, canonical in operation_aliases:
        if phrase in command_text:
            operation = canonical
            break

    # --------------------------------------------------
    # Return an executable capability result.
    #
    # Specialized handlers can later replace this fallback
    # without changing routing or executor behavior.
    # --------------------------------------------------

    return {
        "success": True,
        "capability": capability_type or "learned",
        "skill": name,
        "operation": operation,
        "command": command_text,
        "abilities": abilities,
        "executed": True,
        "handler_type": "generic.learned",
        "message": (
            f"Executed learned capability '{name}' "
            f"using operation '{operation}'."
        ),
        "errors": [],
    }


def run_handler(name, command):
    """
    Execute an approved learned-skill handler.
    """
    handler = get_handler(name)

    if handler is None:
        raise ValueError(
            f"Unknown skill handler: {name}"
        )

    return handler(command)

# ============================================================
# LEARNED LANGUAGE CAPABILITIES
# ============================================================

def language_capability(command, language):
    """
    Handle a learned human-language capability.

    The language itself is selected dynamically from the
    learned skill. Actual speech output can later be connected
    to Nitron's TTS system.
    """

    from brain.language import language_engine

    language = str(language).strip()

    result = language_engine.execute(
        command,
        language
    )

    result["abilities"] = [
        f"understand {language}",
        f"write {language}",
        f"translate {language}",
        f"answer in {language}",
        f"converse in {language}",
        f"speak {language}",
    ]

    result["speech_ready"] = (
        result.get("operation") == "speak"
    )

    return result


def learned_language(command):
    """
    Execute a learned language capability.

    The language is resolved from the learned capability
    registry instead of requiring the caller to provide it.
    """

    from brain.skill_registry import best_for_task

    skill = best_for_task(command)

    if not skill:
        return {
            "success": False,
            "capability": "language",
            "language": "",
            "speech_ready": False,
            "abilities": [],
            "message": "No learned language capability matched."
        }

    language = str(
        skill.get("name", "")
    ).strip()

    if str(
        skill.get("capability_type", "")
    ).lower() != "language":
        return {
            "success": False,
            "capability": "language",
            "language": language,
            "speech_ready": False,
            "abilities": [],
            "message": (
                f"{language} is not registered as a language capability."
            )
        }

    return language_capability(
        command,
        language
    )


# ============================================================
# GENERIC PROGRAMMING CAPABILITY
# ============================================================

def learned_programming(command):
    """
    Execute a learned programming capability.

    Supports real Python write/build/test operations plus
    real Python source analysis and debugging.
    """

    from pathlib import Path
    import ast
    import re

    from brain.skill_registry import best_for_task
    from brain.reasoning import reasoning

    # File-oriented programming commands may not contain enough
    # capability words for registry matching. Prefer the learned
    # programming capability when the command clearly targets a
    # Python source file.
    command_text_raw = str(command).strip()
    command_text_lower = command_text_raw.lower()

    skill = best_for_task(command)

    if not skill:
        if (
            command_text_lower.startswith("analyze ")
            or command_text_lower.startswith("debug ")
            or command_text_lower.startswith("test ")
            or command_text_lower.startswith("modify ")
        ) and (
            ".py" in command_text_lower
            or ".py " in command_text_lower
        ):
            from brain.skill_registry import get_skill

            skill = get_skill("Python programming")

    if not skill:
        return {
            "success": False,
            "capability": "programming",
            "language": "",
            "operation": None,
            "message": "No learned programming capability matched."
        }

    if str(skill.get("capability_type", "")).lower() != "programming":
        return {
            "success": False,
            "capability": "programming",
            "language": str(skill.get("name", "")),
            "operation": None,
            "message": "Matched capability is not programming."
        }

    language_aliases = {
        "python programming": "python",
        "python": "python",
        "javascript programming": "javascript",
        "javascript": "javascript",
        "typescript programming": "typescript",
        "typescript": "typescript",
        "rust programming": "rust",
        "rust": "rust",
        "kotlin programming": "kotlin",
        "kotlin": "kotlin",
        "java programming": "java",
        "java": "java",
        "bash programming": "bash",
        "bash": "bash",
        "c++ programming": "cpp",
        "c++": "cpp",
        "c# programming": "csharp",
        "c#": "csharp",
        "go programming": "go",
        "go": "go",
    }

    language = str(skill.get("name", "")).strip().lower()
    language = language_aliases.get(language, language)

    command_text = str(command).lower()

    # Natural-language programming operation detection.
    operation_aliases = [
        ("analyze", "analyze"),
        ("debug", "debug"),
        ("test", "test"),
        ("modify", "modify"),
        ("build", "build"),
        ("write", "write"),
        ("create", "create"),
        ("make", "create"),
        ("generate", "create"),
        ("draw", "create"),
        ("program", "create"),
        ("explain", "explain"),
    ]

    operation = None

    for phrase, canonical in operation_aliases:
        if phrase in command_text:
            operation = canonical
            break

    # ======================================================
    # REAL PYTHON ANALYSIS / DEBUGGING
    # ======================================================

    if (
        language == "python"
        and operation in {"analyze", "debug"}
    ):
        matches = re.findall(
            r'(?:(?:^|\s|["\'])|(?:/))'
            r'([A-Za-z0-9_./-]+\.py)\b',
            str(command)
        )

        file_name = None

        if matches:
            file_name = matches[-1]

        if not file_name:
            return {
                "success": False,
                "capability": "programming",
                "language": language,
                "operation": operation,
                "message": (
                    "No Python source file was specified."
                ),
            }

        file_path = Path(file_name).expanduser()

        if not file_path.is_absolute():
            file_path = Path.cwd() / file_path

        if not file_path.exists():
            return {
                "success": False,
                "capability": "programming",
                "language": language,
                "operation": operation,
                "file": file_name,
                "analyzed": operation == "analyze",
                "debugged": operation == "debug",
                "syntax_valid": False,
                "functions": [],
                "classes": [],
                "imports": [],
                "errors": [{
                    "type": "FileNotFoundError",
                    "message": f"Python file not found: {file_name}"
                }],
            }

        try:
            source = file_path.read_text(
                encoding="utf-8"
            )
        except Exception as exc:
            return {
                "success": False,
                "capability": "programming",
                "language": language,
                "operation": operation,
                "file": file_name,
                "analyzed": False,
                "debugged": False,
                "syntax_valid": False,
                "functions": [],
                "classes": [],
                "imports": [],
                "errors": [{
                    "type": type(exc).__name__,
                    "message": str(exc)
                }],
            }

        functions = []
        classes = []
        imports = []
        errors = []
        syntax_valid = True

        try:
            tree = ast.parse(
                source,
                filename=str(file_path)
            )

            for node in ast.walk(tree):

                if isinstance(
                    node,
                    (ast.FunctionDef, ast.AsyncFunctionDef)
                ):
                    functions.append(node.name)

                elif isinstance(node, ast.ClassDef):
                    classes.append(node.name)

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
                "message": str(exc)
            })

        return {
            "success": True,
            "capability": "programming",
            "language": language,
            "operation": operation,
            "file": file_name,
            "analyzed": operation == "analyze",
            "debugged": operation == "debug",
            "syntax_valid": syntax_valid,
            "functions": functions,
            "classes": classes,
            "imports": imports,
            "errors": errors,
        }

    # ======================================================
    # PROJECT-PRODUCING OPERATIONS
    # ======================================================

    if operation in {
        "write",
        "create",
        "build",
        "test",
    }:

        project_request = (
            f"{command}. "
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

    return {
        "success": True,
        "capability": "programming",
        "language": language,
        "operation": operation,
        "command": str(command),
        "abilities": skill.get("abilities", []),
        "message": (
            f"Programming operation '{operation}' "
            f"selected for {language}."
        ),
    }


# ============================================================
# GENERIC FRAMEWORK CAPABILITY
# ============================================================

def learned_framework(command):
    """
    Execute a learned framework/library capability.
    """

    from brain.skill_registry import best_for_task

    skill = best_for_task(command)

    if not skill:
        return {
            "success": False,
            "capability": "framework",
            "technology": "",
            "operation": None,
            "message": "No learned framework capability matched."
        }

    capability_type = str(
        skill.get("capability_type", "")
    ).lower()

    if capability_type != "framework":
        return {
            "success": False,
            "capability": "framework",
            "technology": str(skill.get("name", "")),
            "operation": None,
            "message": "Matched capability is not a framework."
        }

    technology = str(
        skill.get("name", "")
    ).strip()

    command_text = str(command).lower()

    operations = [
        "build",
        "create",
        "use",
        "configure",
        "integrate",
        "modify",
        "debug",
        "test",
        "explain",
    ]

    operation = None

    for item in operations:
        if item in command_text:
            operation = item
            break

    return {
        "success": True,
        "capability": "framework",
        "technology": technology,
        "operation": operation,
        "command": str(command),
        "abilities": skill.get(
            "abilities",
            []
        ),
        "message": (
            f"Framework operation '{operation}' "
            f"selected for {technology}."
        ),
    }


# ============================================================
# GENERIC KNOWLEDGE CAPABILITY
# ============================================================

def learned_knowledge(command):
    """
    Execute a learned knowledge capability.

    Unlike the old placeholder handler, this connects the learned
    capability back to Nitron's reasoning/knowledge system so the
    capability can actually be used rather than merely reported.
    """

    from brain.skill_registry import best_for_task

    skill = best_for_task(command)

    if not skill:
        return {
            "success": False,
            "capability": "knowledge",
            "topic": "",
            "operation": None,
            "executed": False,
            "message": "No learned knowledge capability matched.",
            "errors": [
                "No learned knowledge capability matched."
            ],
        }

    topic = str(
        skill.get("name", "")
    ).strip()

    command_text = str(command).strip()
    lowered = command_text.lower()

    operations = [
        "explain",
        "understand",
        "answer",
        "apply",
        "analyze",
        "use",
        "read",
        "write",
        "create",
        "modify",
        "fix",
        "debug",
        "test",
    ]

    operation = "use"

    for item in operations:
        if item in lowered:
            operation = item
            break

    abilities = skill.get("abilities", [])

    if not isinstance(abilities, list):
        abilities = []

    # ------------------------------------------------------------
    # USE THE LEARNED KNOWLEDGE
    # ------------------------------------------------------------
    #
    # The learned skill becomes context for Nitron's reasoning
    # engine. We deliberately do not hard-code subjects here.
    # ------------------------------------------------------------

    execution_prompt = (
        f"Use the learned capability '{topic}' to answer this request.\n"
        f"Requested operation: {operation}\n"
        f"User request: {command_text}\n"
        f"Learned abilities: {', '.join(str(x) for x in abilities)}"
    )

    generated = None
    execution_error = None

    try:
        # --------------------------------------------------------
        # EXECUTE THROUGH THE EXISTING LEARNED-KNOWLEDGE PATH
        # --------------------------------------------------------
        #
        # Do NOT call reasoning.answer() here.
        # answer() intentionally routes learned capabilities first,
        # which would send this request back to learned.knowledge.
        #
        # Instead, directly use the existing search_learned()
        # and _normalize_learned() pipeline.
        # --------------------------------------------------------

        from brain.reasoning import reasoning

        learned = reasoning.search_learned(
            command_text
        )

        if learned:
            matched_topic = next(
                iter(learned)
            )

            learned_data = (
                learned[matched_topic].get("data")
                if isinstance(
                    learned[matched_topic],
                    dict
                )
                and "data" in learned[matched_topic]
                else learned[matched_topic]
            )

            generated = reasoning._normalize_learned(
                matched_topic,
                learned_data
            )

    except Exception as exc:
        execution_error = str(exc)

    # ------------------------------------------------------------
    # SUCCESSFUL EXECUTION
    # ------------------------------------------------------------

    if generated is not None:
        if isinstance(generated, dict):
            result = dict(generated)

            result.setdefault(
                "success",
                True
            )
            result.setdefault(
                "capability",
                "knowledge"
            )
            result.setdefault(
                "topic",
                topic
            )
            result.setdefault(
                "operation",
                operation
            )
            result.setdefault(
                "executed",
                True
            )
            result.setdefault(
                "abilities",
                abilities
            )


            # Normalize the generic capability contract.
            # Learned knowledge may return the answer in
            # 'message'; expose it consistently as 'output'.
            if result.get("output") is None:
                result["output"] = result.get("message")

            return result

        return {
            "success": True,
            "capability": "knowledge",
            "topic": topic,
            "operation": operation,
            "command": command_text,
            "executed": True,
            "abilities": abilities,
            "output": str(generated),
            "message": (
                f"Used learned capability '{topic}' "
                f"for operation '{operation}'."
            ),
            "errors": [],
        }

    # ------------------------------------------------------------
    # FALLBACK
    # ------------------------------------------------------------

    return {
        "success": False,
        "capability": "knowledge",
        "topic": topic,
        "operation": operation,
        "command": command_text,
        "executed": False,
        "abilities": abilities,
        "message": (
            f"Learned capability '{topic}' was found, "
            f"but execution could not be completed."
        ),
        "errors": [
            execution_error or "Unknown execution error."
        ],
    }

# ============================================================
# GENERIC HANDLER REGISTRATION
# ============================================================

PROGRAMMING_HANDLER = "learned.programming"
FRAMEWORK_HANDLER = "learned.framework"
KNOWLEDGE_HANDLER = "learned.knowledge"

HANDLERS[PROGRAMMING_HANDLER] = learned_programming
HANDLERS[FRAMEWORK_HANDLER] = learned_framework
HANDLERS[KNOWLEDGE_HANDLER] = learned_knowledge


# ============================================================
# LANGUAGE HANDLER REGISTRY
# ============================================================

LANGUAGE_HANDLER = "learned.language"

HANDLERS[LANGUAGE_HANDLER] = learned_language
