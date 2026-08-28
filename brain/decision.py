"""
Nitron Decision Engine
"""

from brain.context import context
from brain.memory import memory

try:
    from brain.skill_registry import best_for_task
except Exception:
    best_for_task = None


class DecisionEngine:
    """
    Decides what Nitron should do.

    Priority:
        1. Explicit system intents
        2. Specific learned capabilities
        3. Built-in modules
        4. General chat
    """

    def decide(self, command):

        command = str(command).lower().strip()

        context.update(command)

        # --------------------------------------------------
        # EXPLICIT LEARNING / TEACHING
        # --------------------------------------------------

        if any(word in command for word in [
            "teach",
            "lesson",
            "academy",
            "learn",
            "study"
        ]):
            return {
                "module": "academy",
                "action": "teach"
            }

        # --------------------------------------------------
        # LEARNED PROGRAMMING FILE OPERATIONS
        #
        # Explicit Python source-file operations such as
        # analyze/debug/test should use the learned Python
        # programming capability even when best_for_task()
        # cannot score the file path highly enough.
        # --------------------------------------------------

        programming_operations = (
            "analyze",
            "debug",
            "test",
            "modify",
            "fix",
        )

        python_file_markers = (
            ".py",
            "python code",
            "python file",
            "python program",
        )

        if (
            any(op in command for op in programming_operations)
            and any(marker in command for marker in python_file_markers)
        ):
            try:
                python_skill = best_for_task(
                    "Python programming"
                )

                if python_skill:
                    confidence = float(
                        python_skill.get(
                            "confidence",
                            0
                        )
                    )

                    return {
                        "module": "learned",
                        "action": "capability",
                        "skill": python_skill.get(
                            "name",
                            "Python programming"
                        ),
                        "confidence": confidence,
                        "abilities": python_skill.get(
                            "abilities",
                            []
                        ),
                        "handlers": python_skill.get(
                            "handlers",
                            ["learned.programming"]
                        ),
                    }

            except Exception:
                pass

        # --------------------------------------------------
        # LEARNED CAPABILITY ROUTING
        #
        # Check this BEFORE generic developer routing so
        # specific learned capabilities can win.
        # --------------------------------------------------

        if best_for_task is not None:

            try:

                skill = best_for_task(command)

                if skill:

                    confidence = float(
                        skill.get(
                            "confidence",
                            0
                        )
                    )

                    if confidence >= 0.5:

                        skill_name = skill.get(
                            "name",
                            ""
                        )

                        memory.remember(
                            "last_learned_capability",
                            skill_name
                        )

                        return {
                            "module": "learned",
                            "action": "capability",
                            "skill": skill_name,
                            "confidence": confidence,
                            "abilities": skill.get(
                                "abilities",
                                []
                            ),
                            "handlers": skill.get(
                                "handlers",
                                []
                            )
                        }

            except Exception:
                pass

        # --------------------------------------------------
        # BUILT-IN PROJECT / DEVELOPMENT
        # --------------------------------------------------

        if any(word in command for word in [
            "create",
            "build",
            "generate",
            "project"
        ]):
            return {
                "module": "developer",
                "action": "build"
            }

        # --------------------------------------------------
        # BUILT-IN TRADING
        # --------------------------------------------------

        if any(word in command for word in [
            "trade",
            "gold",
            "forex",
            "bitcoin",
            "btc"
        ]):
            return {
                "module": "trading",
                "action": "analyze"
            }

        # --------------------------------------------------
        # BUILT-IN WEATHER
        # --------------------------------------------------

        if any(word in command for word in [
            "weather",
            "temperature",
            "forecast"
        ]):
            return {
                "module": "weather",
                "action": "forecast"
            }

        # --------------------------------------------------
        # BUILT-IN MUSIC
        # --------------------------------------------------

        if any(word in command for word in [
            "music",
            "song",
            "play"
        ]):
            return {
                "module": "music",
                "action": "play"
            }

        # --------------------------------------------------
        # BUILT-IN TIME / DATE
        # --------------------------------------------------

        if any(word in command for word in [
            "time",
            "date"
        ]):
            return {
                "module": "system",
                "action": "clock"
            }

        # --------------------------------------------------
        # GENERAL CHAT
        # --------------------------------------------------

        memory.remember(
            "last_command",
            command
        )

        return {
            "module": "chat",
            "action": "respond"
        }


decision = DecisionEngine()
