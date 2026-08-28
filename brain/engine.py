"""
Nitron Brain Engine

Central bridge between the command system and Nitron's
reasoning/generation system.
"""

from core.state import State
from core.logger import Logger
from core.router import Router

try:
    from brain.reasoning import reasoning
except Exception:
    reasoning = None


class BrainEngine:

    def __init__(self):
        self.state = State()
        self.logger = Logger()
        self.router = Router()

    def think(self, command):
        """
        Process a user command.

        Primary path:
            command -> reasoning.answer()

        Fallback:
            command -> core router

        The reasoning engine contains Nitron's higher-level
        answer, learning, and project-generation logic.
        """

        self.state.set(State.THINKING)

        try:
            command = str(command).strip()

            if not command:
                return {
                    "message": "Tell me what you want Nitron to do.",
                    "generated": False,
                }

            self.logger.info(
                f"Received command: {command}"
            )

            # --------------------------------------------------
            # PRIMARY INTELLIGENCE PATH
            # --------------------------------------------------

            if reasoning is not None:

                try:

                    result = reasoning.answer(
                        command
                    )

                    if result is not None:

                        if isinstance(
                            result,
                            dict
                        ):
                            result.setdefault(
                                "route",
                                "reasoning"
                            )

                            return result

                        return {
                            "message": str(result),
                            "route": "reasoning"
                        }

                except Exception as error:

                    self.logger.info(
                        f"Reasoning error: {error}"
                    )

            # --------------------------------------------------
            # FALLBACK ROUTING
            # --------------------------------------------------

            module = self.router.route(
                command
            )

            self.logger.info(
                f"Fallback routing to: {module}"
            )

            return {
                "message": (
                    f"Routed to {module} module."
                ),
                "module": module,
                "route": "core_router",
                "generated": False,
            }

        finally:

            self.state.reset()

    def status(self):
        return {
            "state": self.state.get(),
            "engine": "BrainEngine",
            "online": True,
            "reasoning_available": (
                reasoning is not None
            ),
        }


brain = BrainEngine()
