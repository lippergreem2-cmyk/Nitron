"""
Nitron Command Router
"""

from nitron_core import nitron
import ai_brain


class CommandRouter:

    def route(self, command):

        command = command.lower().strip()

        # ----------------------------
        # IMAGE
        # ----------------------------
        if command.startswith("generate image"):

            prompt = command.replace(
                "generate image",
                "",
                1
            ).strip()

            return nitron.generate_image(prompt)

        # ----------------------------
        # VIDEO
        # ----------------------------
        if command.startswith("generate video"):

            prompt = command.replace(
                "generate video",
                "",
                1
            ).strip()

            return nitron.generate_video(prompt)

        # ----------------------------
        # GAME
        # ----------------------------
        if command.startswith("create game"):

            name = command.replace(
                "create game",
                "",
                1
            ).strip()

            return nitron.create_game(name)

        # ----------------------------
        # WEBSITE
        # ----------------------------
        if command.startswith("create website"):

            name = command.replace(
                "create website",
                "",
                1
            ).strip()

            return nitron.create_website(name)

        # ----------------------------
        # CHATBOT
        # ----------------------------
        if command.startswith("create chatbot"):

            name = command.replace(
                "create chatbot",
                "",
                1
            ).strip()

            return nitron.create_chatbot(name)

        # ----------------------------
        # API
        # ----------------------------
        if command.startswith("create api"):

            name = command.replace(
                "create api",
                "",
                1
            ).strip()

            return nitron.create_api(name)

        # ----------------------------
        # CODE
        # ----------------------------
        if command.startswith("generate code"):

            prompt = command.replace(
                "generate code",
                "",
                1
            ).strip()

            return nitron.generate_code(prompt)

        # ----------------------------
        # GUIDE MODE
        # ----------------------------
        if command in ("start guide", "guide me", "let's build something", "teach me"):
            ai_brain.set_mode("guide")
            ai_brain.new_project()
            return ai_brain.chat(
                "The user just asked to start a guided build session. "
                "Ask them what they want to build and their experience level."
            )

        if command in ("end guide", "stop guide", "guide off"):
            ai_brain.set_mode("normal")
            return "Guide mode off, Boss."

        # ----------------------------
        # FALLBACK -- real AI reply instead of a canned error
        # ----------------------------
        return ai_brain.chat(command)


router = CommandRouter()
