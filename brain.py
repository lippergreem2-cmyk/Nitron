# ==========================================================
# NITRON BRAIN 2.0
# brain.py
# ==========================================================

import datetime
import random


# ==========================================================
# OPTIONAL MODULES
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
    from startup.startup_engine import ask_startup
except Exception:
    ask_startup = None


try:
    from developer.builder_manager import BuilderManager
    builder = BuilderManager()
except Exception:
    builder = None



# ==========================================================
# CODE AI
# ==========================================================

from developer.code_ai import CodeAI
code_ai = CodeAI()



# ==========================================================
# ENTRY POINT
# ==========================================================

def ask(command):

    return think(command)# ==========================================================
# MAIN BRAIN
# ==========================================================

def think(command):

    command = command.strip()

    lower_command = command.lower()



    if not command:

        return "Please enter a command."



    # ==================================================
    # CODE AI BUILDER (HIGHEST PRIORITY)
    # ==================================================

    if (
        lower_command.startswith("create website")
        or lower_command.startswith("create fullstack")
        or lower_command.startswith("create web app")
        or lower_command.startswith("create chatbot")
        or lower_command.startswith("create api")
        or lower_command.startswith("create ai")
    ):

        if code_ai:

            try:

                return code_ai.process(command)


            except Exception as e:

                return f"Code AI error: {e}"


        return "Code AI unavailable."



    # ==================================================
    # OPEN APPS
    # ==================================================

    if lower_command.startswith("open "):

        app = lower_command.replace(
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

    if lower_command.startswith("play "):

        if play_song:

            try:

                return play_song(command)


            except Exception as e:

                return f"Music error: {e}"


        return "Music system unavailable."    # ==================================================
    # PHYSICS
    # ==================================================

    if lower_command.startswith("teach physics"):

        topic = lower_command.replace(
            "teach physics",
            "",
            1
        ).strip()


        if ask_physics:

            try:

                return ask_physics(topic)


            except Exception as e:

                return f"Physics error: {e}"


        return "Physics system unavailable."



    # ==================================================
    # ACADEMY
    # ==================================================

    if ask_academy:

        try:

            result = ask_academy(command)


            if result:

                return result


        except Exception:

            pass



    # ==================================================
    # MEMORY
    # ==================================================

    if remember:

        try:

            result = remember(command)


            if result:

                return result


        except Exception:

            pass



    if recall:

        try:

            result = recall(command)


            if result:

                return result


        except Exception:

            pass



    # ==================================================
    # STARTUP ENGINE
    # ==================================================

    if ask_startup:

        try:

            result = ask_startup(command)


            if result:

                return result


        except Exception:

            pass    # ==================================================
    # PYTHON LESSONS
    # ==================================================

    if lower_command in (
        "learn python",
        "teach me python"
    ):

        try:

            from academy.python_teacher import ask_python

            return ask_python("topics")


        except Exception:

            return "Python teacher unavailable."



    if lower_command.startswith("python "):

        try:

            from academy.python_teacher import ask_python

            topic = command.replace(
                "python ",
                "",
                1
            ).strip()


            return ask_python(topic)


        except Exception:

            return "Python teacher unavailable."



    # ==================================================
    # C++ LESSONS
    # ==================================================

    if lower_command in (
        "learn c++",
        "teach me c++"
    ):

        try:

            from academy.cpp_teacher import ask_cpp

            return ask_cpp("topics")


        except Exception:

            return "C++ teacher unavailable."



    # ==================================================
    # JAPANESE
    # ==================================================

    if lower_command in (
        "learn japanese",
        "teach me japanese"
    ):

        try:

            from academy.japanese import teach

            return teach()


        except Exception:

            return "Japanese teacher unavailable."



    # ==================================================
    # PYTHON PROJECT BUILDER
    # ==================================================

    if lower_command.startswith("create python"):


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

            return f"Builder error: {e}"    # ==================================================
    # TRADING
    # ==================================================

    if (
        lower_command.startswith("analyze ")
        or lower_command.startswith("trade ")
        or lower_command.startswith("buy ")
        or lower_command.startswith("sell ")
    ):

        if advise:

            try:

                symbol = (
                    lower_command
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


        return "Trading module unavailable."



    # ==================================================
    # SYMBOLS
    # ==================================================

    if lower_command == "gold":

        return "Gold trading symbol is XAUUSD."


    if lower_command == "bitcoin":

        return "Bitcoin trading symbol is BTCUSD."


    if lower_command == "ethereum":

        return "Ethereum trading symbol is ETHUSD."



    # ==================================================
    # GREETINGS
    # ==================================================

    if lower_command in [
        "hello",
        "hi",
        "hey",
        "good morning",
        "good afternoon",
        "good evening"
    ]:

        return "Hello Boss Nimrod."



    if lower_command == "who are you":

        return (
            "I am Nitron, your personal AI assistant. "
            "I can teach, build software, open apps, "
            "and create real projects."
        )



    # ==================================================
    # TIME AND DATE
    # ==================================================

    if lower_command == "time":

        return datetime.datetime.now().strftime(
            "%I:%M %p"
        )


    if lower_command == "date":

        return datetime.datetime.now().strftime(
            "%d %B %Y"
        )



    # ==================================================
    # HELP
    # ==================================================

    if lower_command == "help":

        return """

NITRON COMMANDS

BUILD:
create website MySite
create fullstack website StoreAI
create web app Dashboard
create chatbot TutorBot
create api ShopAPI
create ai VisionAI

LEARN:
teach me python
teach physics motion
teach me japanese
teach me c++

PYTHON:
create python project Test

TRADING:
analyze xauusd
analyze btcusd

SYSTEM:
open youtube
play song
time
date
help

"""



    # ==================================================
    # DEFAULT
    # ==================================================

    return "I am still learning that command."
