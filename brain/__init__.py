# ==========================================================
# NITRON BRAIN
# brain/__init__.py
# ==========================================================

import datetime
import random


# ==========================================================
# CODE AI BUILDER
# ==========================================================

try:
    from developer.code_ai import CodeAI
    code_ai = CodeAI()

except Exception as e:
    code_ai = None



# ==========================================================
# OTHER MODULES
# ==========================================================

try:
    from music import play_song

except Exception:
    play_song = None



try:
    from physics import ask_physics

except Exception:
    ask_physics = None



try:
    from academy.academy import ask_academy

except Exception:
    ask_academy = None



try:
    from developer.builder_manager import BuilderManager
    builder = BuilderManager()

except Exception:
    builder = None



try:
    from trade_advisor import advise

except Exception:
    advise = None



# ==========================================================
# ENTRY
# ==========================================================

def ask(command):

    return think(command)



# ==========================================================
# THINK ENGINE
# ==========================================================

def think(command):

    command = command.strip()

    text = command.lower()


    if not command:

        return "Please enter a command."

    if text in ("start guide", "guide me", "let's build something", "teach me"):
        import ai_brain
        ai_brain.set_mode("guide")
        return "Guide mode on. Tell me what you want to build."

    if text in ("end guide", "stop guide", "guide off"):
        import ai_brain
        ai_brain.set_mode("normal")
        return "Guide mode off."



    # ==================================================
    # CODE AI (FIRST PRIORITY)
    # ==================================================

    if (
        text.startswith("create website")
        or text.startswith("create fullstack")
        or text.startswith("create web app")
        or text.startswith("create chatbot")
        or text.startswith("create api")
        or text.startswith("create ai")
    ):

        if code_ai:

            try:
                return code_ai.process(command)

            except Exception as e:

                return f"Code AI error: {e}"


        return "Code AI unavailable."    # ==================================================
    # OPEN APPS
    # ==================================================

    if text.startswith("open "):

        app = text.replace(
            "open ",
            "",
            1
        ).strip()


        try:

            from commands import open_app

            return open_app(app)


        except Exception as e:

            return f"App error: {e}"



    # ==================================================
    # MUSIC
    # ==================================================

    if text.startswith("play "):

        if play_song:

            try:

                return play_song(command)


            except Exception as e:

                return f"Music error: {e}"


        return "Music system unavailable."



    # ==================================================
    # PHYSICS
    # ==================================================

    if text.startswith("teach physics"):

        topic = text.replace(
            "teach physics",
            "",
            1
        ).strip()


        if ask_physics:

            try:

                return ask_physics(topic)


            except Exception as e:

                return f"Physics error: {e}"


        return "Physics unavailable."



    # ==================================================
    # ACADEMY
    # ==================================================

    if ask_academy:

        try:

            result = ask_academy(command)


            if result:

                return result


        except Exception:

            pass    # ==================================================
    # PYTHON PROJECT BUILDER
    # ==================================================

    if text.startswith("create python"):


        if not builder:

            return "Builder unavailable."


        try:

            name = (
                command
                .replace("create python", "", 1)
                .replace("project", "", 1)
                .strip()
            )


            if not name:

                return "Please provide a project name."


            return builder.python.create_program(name)


        except Exception as e:

            return f"Builder error: {e}"



    # ==================================================
    # TRADING
    # ==================================================

    if (
        text.startswith("analyze ")
        or text.startswith("trade ")
        or text.startswith("buy ")
        or text.startswith("sell ")
    ):


        if advise:

            try:

                symbol = (
                    text
                    .replace("analyze ", "")
                    .replace("trade ", "")
                    .replace("buy ", "")
                    .replace("sell ", "")
                    .strip()
                    .upper()
                )


                return str(advise(symbol))


            except Exception as e:

                return f"Trading error: {e}"


        return "Trading unavailable."



    # ==================================================
    # SYMBOLS
    # ==================================================

    if text == "gold":

        return "Gold trading symbol is XAUUSD."


    if text == "bitcoin":

        return "Bitcoin trading symbol is BTCUSD."    # ==================================================
    # GREETINGS
    # ==================================================

    if text in [
        "hello",
        "hi",
        "hey",
        "good morning",
        "good afternoon",
        "good evening"
    ]:

        return "Hello Boss Nimrod."



    # ==================================================
    # IDENTITY
    # ==================================================

    if text == "who are you":

        return (
            "I am Nitron, your personal AI assistant. "
            "I can build websites, web apps, AI projects, "
            "teach, and help with coding."
        )



    # ==================================================
    # TIME
    # ==================================================

    if text == "time":

        return datetime.datetime.now().strftime(
            "%I:%M %p"
        )



    if text == "date":

        return datetime.datetime.now().strftime(
            "%d %B %Y"
        )



    # ==================================================
    # HELP
    # ==================================================

    if text == "help":

        return """

NITRON COMMANDS

BUILD PROJECTS
--------------
create website MySite
create fullstack website StoreAI
create web app Dashboard
create chatbot TutorBot
create api ShopAPI
create ai VisionAI

PYTHON
------
create python project Test

TRADING
-------
analyze xauusd
analyze btcusd

SYSTEM
------
open youtube
play song
time
date
help

"""



    # ==================================================
    # DEFAULT -> AI BRAIN (Groq) + GUIDE MODE
    # ==================================================

    try:
        import ai_brain
        return ai_brain.chat(command)
    except Exception as e:
        return f"AI brain error: {e}"
