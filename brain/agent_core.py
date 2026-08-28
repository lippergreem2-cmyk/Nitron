"""
Nitron Agent Core
Advanced orchestration layer.

Flow:
UNDERSTAND -> CONTEXT -> PLAN -> ACT -> VERIFY -> RESPOND
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import time


@dataclass
class AgentStep:
    name: str
    description: str
    status: str = "pending"
    result: Any = None
    error: Optional[str] = None


@dataclass
class AgentTask:
    request: str
    intent: str = "general"
    steps: List[AgentStep] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)
    status: str = "created"
    result: Any = None


class NitronAgent:
    """
    Central intelligence/orchestration layer for Nitron.

    The agent does not expose private chain-of-thought.
    It keeps only concise execution state needed for the task.
    """

    def __init__(self, reasoning=None, learner=None, skill_registry=None):
        self.reasoning = reasoning
        self.learner = learner
        self.skill_registry = skill_registry

        self.active_task = None
        self.history = []

    # ---------------------------------------------------------
    # PUBLIC ENTRY POINT
    # ---------------------------------------------------------

    def process(self, request: str) -> str:
        request = str(request).strip()

        if not request:
            return "I need a request to work on."

        task = self._understand(request)
        self.active_task = task

        try:
            self._build_plan(task)
            self._execute(task)
            self._verify(task)

            response = self._respond(task)

            task.status = "completed"
            task.result = response

            self.history.append(task)

            return response

        except Exception as exc:
            task.status = "failed"
            task.result = str(exc)

            self.history.append(task)

            return self._safe_error_response(task, exc)

    # ---------------------------------------------------------
    # UNDERSTANDING
    # ---------------------------------------------------------

    def _understand(self, request: str) -> AgentTask:
        lowered = request.lower()

        intent = "general"

        if any(x in lowered for x in (
            "create", "build", "make", "generate"
        )):
            intent = "creation"

        elif any(x in lowered for x in (
            "fix", "debug", "error", "broken"
        )):
            intent = "debugging"

        elif any(x in lowered for x in (
            "learn", "teach", "explain"
        )):
            intent = "learning"

        elif any(x in lowered for x in (
            "search", "find", "look up"
        )):
            intent = "research"

        elif any(x in lowered for x in (
            "scan", "security", "secure"
        )):
            intent = "security"

        task = AgentTask(
            request=request,
            intent=intent,
            status="understood"
        )

        task.context["request_length"] = len(request)
        task.context["timestamp"] = time.time()

        return task

    # ---------------------------------------------------------
    # PLANNING
    # ---------------------------------------------------------

    def _build_plan(self, task: AgentTask):
        task.status = "planning"

        task.steps.clear()

        task.steps.append(
            AgentStep(
                "understand",
                "Understand the user's request and intent."
            )
        )

        task.steps.append(
            AgentStep(
                "context",
                "Gather relevant Nitron context, skills and knowledge."
            )
        )

        if task.intent in ("creation", "debugging"):
            task.steps.append(
                AgentStep(
                    "analyze",
                    "Analyze the technical requirements."
                )
            )

        if task.intent == "research":
            task.steps.append(
                AgentStep(
                    "research",
                    "Gather relevant information."
                )
            )

        if task.intent == "learning":
            task.steps.append(
                AgentStep(
                    "learn",
                    "Process and organize the requested knowledge."
                )
            )

        task.steps.append(
            AgentStep(
                "execute",
                "Perform the appropriate operation."
            )
        )

        task.steps.append(
            AgentStep(
                "verify",
                "Check whether the result is valid."
            )
        )

        task.steps.append(
            AgentStep(
                "respond",
                "Produce the final useful response."
            )
        )

        task.status = "planned"

    # ---------------------------------------------------------
    # EXECUTION
    # ---------------------------------------------------------

    def _execute(self, task: AgentTask):
        task.status = "executing"

        for step in task.steps:

            if step.name in ("understand", "respond"):
                continue

            step.status = "running"

            try:
                if step.name == "context":
                    step.result = self._get_context(task)

                elif step.name == "analyze":
                    step.result = self._analyze(task)

                elif step.name == "research":
                    step.result = {
                        "required": True,
                        "handled_by": "tool_router"
                    }

                elif step.name == "learn":
                    step.result = self._learning_context(task)

                elif step.name == "execute":
                    step.result = self._execute_request(task)
                    task.result = step.result

                step.status = "completed"

            except Exception as exc:
                step.status = "failed"
                step.error = str(exc)
                raise

    # ---------------------------------------------------------
    # CONTEXT
    # ---------------------------------------------------------

    def _get_context(self, task: AgentTask) -> Dict[str, Any]:
        context = {}

        if self.skill_registry is not None:
            try:
                matches = self.skill_registry.find_for_task(task.request)
                context["skills"] = matches
            except Exception:
                context["skills"] = []

        return context

    # ---------------------------------------------------------
    # ANALYSIS
    # ---------------------------------------------------------

    def _analyze(self, task: AgentTask) -> Dict[str, Any]:
        return {
            "intent": task.intent,
            "request": task.request,
            "requires_multi_step": True
        }

    # ---------------------------------------------------------
    # LEARNING
    # ---------------------------------------------------------

    def _learning_context(self, task: AgentTask) -> Dict[str, Any]:
        return {
            "learning_requested": True,
            "topic": task.request
        }

    # ---------------------------------------------------------
    # REQUEST EXECUTION
    # ---------------------------------------------------------

    def _execute_request(self, task: AgentTask):
        """
        Delegate actual intelligence to the existing reasoning engine.
        """

        if self.reasoning is None:
            return {
                "type": "unhandled",
                "message": "Reasoning engine is not connected yet."
            }

        if hasattr(self.reasoning, "answer"):
            return self.reasoning.answer(task.request)

        if hasattr(self.reasoning, "analyze"):
            return self.reasoning.analyze(task.request)

        return {
            "type": "unhandled",
            "message": "No compatible reasoning method found."
        }

    # ---------------------------------------------------------
    # VERIFICATION
    # ---------------------------------------------------------

    def _verify(self, task: AgentTask):
        task.status = "verifying"

        for step in task.steps:
            if step.name == "verify":
                step.status = "running"

                if task.result is not None:
                    step.result = {
                        "valid": True,
                        "has_result": True
                    }
                    step.status = "completed"
                else:
                    step.result = {
                        "valid": False,
                        "has_result": False
                    }
                    step.status = "failed"

    # ---------------------------------------------------------
    # RESPONSE
    # ---------------------------------------------------------

    def _respond(self, task: AgentTask) -> str:
        """
        Convert the verified result into the user-facing response.
        """

        if task.result is None:
            return "I couldn't produce a result."

        if isinstance(task.result, str):
            return task.result

        if isinstance(task.result, dict):
            if "message" in task.result:
                return str(task.result["message"])

        return str(task.result)

    # ---------------------------------------------------------
    # ERROR HANDLING
    # ---------------------------------------------------------

    def _safe_error_response(self, task: AgentTask, exc: Exception) -> str:
        return (
            "I couldn't complete that task yet.\n\n"
            f"Stage: {task.status}\n"
            f"Reason: {exc}"
        )

    # ---------------------------------------------------------
    # STATUS
    # ---------------------------------------------------------

    def status(self) -> Dict[str, Any]:
        if self.active_task is None:
            return {
                "active": False,
                "status": "idle"
            }

        return {
            "active": True,
            "status": self.active_task.status,
            "request": self.active_task.request,
            "intent": self.active_task.intent,
            "steps": [
                {
                    "name": step.name,
                    "status": step.status
                }
                for step in self.active_task.steps
            ]
        }


__all__ = [
    "NitronAgent",
    "AgentTask",
    "AgentStep"
]
