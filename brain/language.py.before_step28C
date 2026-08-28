"""
Nitron Learned Language Engine

Provides the execution layer for languages learned by Nitron.

The engine is intentionally separate from the skill registry:
    skill_registry -> knows WHAT Nitron learned
    language engine -> performs language operations
    skill handler  -> connects the two
"""

import re


class LanguageEngine:

    def __init__(self):
        self.name = "Nitron Language Engine"

    def detect_operation(self, command):
        """
        Determine what the user wants to do with the language.
        """

        text = str(command).strip().lower()

        if any(word in text for word in [
            "translate",
            "translation"
        ]):
            return "translate"

        if any(word in text for word in [
            "speak",
            "speech",
            "say aloud",
            "read aloud"
        ]):
            return "speak"

        if any(word in text for word in [
            "write",
            "writing"
        ]):
            return "write"

        if any(word in text for word in [
            "converse",
            "conversation",
            "talk",
            "chat"
        ]):
            return "converse"

        if any(word in text for word in [
            "answer",
            "respond",
            "reply"
        ]):
            return "answer"

        return "use"

    def clean_language_name(self, language):
        return str(language).strip()

    def execute(self, command, language):
        """
        Execute a learned language capability.

        This layer does not pretend to generate audio.
        It returns the operation that the higher-level AI
        system should perform.
        """

        language = self.clean_language_name(language)

        if not language:
            return {
                "success": False,
                "capability": "language",
                "message": "No language was specified."
            }

        operation = self.detect_operation(command)

        return {
            "success": True,
            "capability": "language",
            "language": language,
            "operation": operation,
            "command": str(command),
            "speech_requested": operation == "speak",
            "speech_generated": False,
            "message": (
                f"Language operation '{operation}' selected "
                f"for {language}."
            )
        }


language_engine = LanguageEngine()
