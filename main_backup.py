# ==========================================================
# NITRON AI ASSISTANT
# Version 5.0
# Part 1/5
# ==========================================================

import os
import time
import traceback
import threading
from datetime import datetime


# ==========================================================
# VOICE
# ==========================================================

try:
    from speech import listen, speak

except Exception:

    def listen():
        return input("You: ")


    def speak(text):
        print("Nitron:", text)



# ==========================================================
# COMMANDS
# ==========================================================

try:
    from commands import execute

except Exception:

    def execute(command):
        return None



# ==========================================================
# BRAIN
# ==========================================================

try:
    from brain import think

except Exception:

    def think(command):
        return None



# ==========================================================
# CODE AI
# ==========================================================

try:
    from developer.code_ai import CodeAI

    code_ai = CodeAI()

except Exception:

    code_ai = None



# ==========================================================
# DAILY DEVOTION
# ==========================================================

try:

    from daily.devotion import get_devotion

except Exception:

    def get_devotion():

        return """
Daily Devotion unavailable.
"""



# ==========================================================
# MEMORY
# ==========================================================

try:

    from memory_manager import memory

except Exception:

    memory = None



# ==========================================================
# DISPLAY
# ==========================================================

FRAMES = [

"""
        ◇
     ◇◇◇◇◇
   ◇◇ N ◇◇
     ◇◇◇◇◇
        ◇
""",

"""
        ◆
     ◆◆◆◆◆
   ◆◆ N ◆◆
     ◆◆◆◆◆
        ◆
"""

]


frame = 0


def clear():

    os.system("clear")



def banner(status):

    global frame

    clear()

    print(
        FRAMES[frame]
    )

    frame = (
        frame + 1
    ) % len(FRAMES)


    print("="*50)
    print("             N I T R O N")
    print("="*50)
    print("Status:", status)
    print("Wake: Hey Nitron")
    print(
        datetime.now().strftime("%H:%M:%S")
    )
    print("="*50)# ==========================================================
# DAILY DEVOTION SYSTEM
# Runs every day at 3:00 AM
# ==========================================================

def daily_devotion():

    while True:

        now = datetime.now()

        if (
            now.hour == 3
            and now.minute == 0
        ):

            try:

                message = get_devotion()

                print(message)

                speak(message)

            except Exception as error:

                print(
                    "Devotion error:",
                    error
                )


            # Wait one hour to avoid repeating

            time.sleep(3600)


        time.sleep(30)



def start_daily_system():

    thread = threading.Thread(
        target=daily_devotion,
        daemon=True
    )

    thread.start()



# ==========================================================
# COMMAND CLEANER
# ==========================================================

def clean_command(command):

    if not command:

        return ""


    command = command.lower().strip()


    fixes = {

        "you tube":
            "youtube",

        "face book":
            "facebook",

        "insta":
            "instagram",

        "meta trader":
            "mt5",

        "x au usd":
            "xauusd",

        "btc usd":
            "btcusd"

    }


    return fixes.get(
        command,
        command
    )



# ==========================================================
# EXIT
# ==========================================================

EXIT_COMMANDS = [

    "exit",
    "quit",
    "goodbye",
    "shutdown",
    "stop nitron"

]


def should_exit(command):

    return command in EXIT_COMMANDS



# ==========================================================
# APP HANDLER
# ==========================================================

def handle_apps(command):

    try:

        result = execute(command)

        if result:

            return result


    except Exception as error:

        print(
            "App error:",
            error
        )


    return None



# ==========================================================
# BRAIN HANDLER
# ==========================================================

def handle_brain(command):

    try:

        result = think(command)

        if result:

            return result


    except Exception as error:

        print(
            "Brain error:",
            error
        )


    return None# ==========================================================
# CODE AI SYSTEM
# ==========================================================

def handle_code_ai(command):

    if not code_ai:

        return None


    if (
        command.startswith("create ")
        or command.startswith("build ")
        or command.startswith("check project")
    ):

        try:

            return code_ai.process(command)


        except Exception as error:

            return f"Code AI error: {error}"


    return None



# ==========================================================
# ACADEMY SYSTEM
# ==========================================================

try:

    from academy.academy import teach

except Exception:

    def teach(topic):

        return "Academy unavailable."



def handle_academy(command):

    if not command.startswith("teach"):

        return None


    topic = command.replace(
        "teach",
        "",
        1
    ).strip()


    try:

        return teach(topic)


    except Exception as error:

        return f"Academy error: {error}"



# ==========================================================
# TRADING SYSTEM
# ==========================================================

try:

    from trade_advisor import advise

except Exception:

    advise = None



def handle_trading(command):

    if not advise:

        return None


    words = [

        "analyze",
        "trade",
        "buy",
        "sell"

    ]


    if not any(
        word in command
        for word in words
    ):

        return None


    try:

        return advise(command)


    except Exception as error:

        return f"Trading error: {error}"



# ==========================================================
# BUILDER SYSTEM
# ==========================================================

try:

    from developer.builder_manager import BuilderManager

    builder = BuilderManager()

except Exception:

    builder = None



def handle_builder(command):

    if not builder:

        return None


    try:

        if command.startswith(
            "create python project"
        ):

            name = command.replace(
                "create python project",
                "",
                1
            ).strip()


            if not name:

                name = "python_project"


            return builder.projects.create_python_project(
                name
            )


    except Exception as error:

        return f"Builder error: {error}"


    return None# ==========================================================
# COMMAND PIPELINE
# ==========================================================

def process_command(command):

    handlers = [

        # Code generator first
        handle_code_ai,

        # Apps
        handle_apps,

        # Academy
        handle_academy,

        # Trading
        handle_trading,

        # Builder
        handle_builder,

        # Brain last
        handle_brain

    ]


    for handler in handlers:

        try:

            result = handler(command)


            if result:

                return result


        except Exception as error:

            print(
                handler.__name__,
                error
            )


    return (
        "Sorry Boss, "
        "I don't know that command yet."
    )



# ==========================================================
# STARTUP
# ==========================================================

def startup():

    banner("STARTING")


    print(
        "Loading Nitron systems..."
    )


    if code_ai:

        print(
            "[ OK ] Code AI"
        )

    else:

        print(
            "[ -- ] Code AI"
        )


    print(
        "[ OK ] Brain"
    )

    print(
        "[ OK ] Daily Devotion"
    )


    speak(
        "Nitron is online. Welcome back Boss."
    )



# ==========================================================
# MAIN LOOP
# ==========================================================

def run():

    startup()

    start_daily_system()


    while True:

        try:

            banner("LISTENING")


            command = listen()


            if not command:

                time.sleep(1)

                continue



            command = clean_command(command)



            print(
                "You:",
                command
            )



            if should_exit(command):

                speak(
                    "Goodbye Boss. Nitron shutting down."
                )

                break



            response = process_command(
                command
            )


            print(
                "Nitron:",
                response
            )


            speak(
                str(response)
            )



        except KeyboardInterrupt:


            speak(
                "Nitron stopped."
            )


            break



        except Exception as error:


            print(
                "SYSTEM ERROR:",
                error
            )


            traceback.print_exc()


            time.sleep(2)# ==========================================================
# NITRON STATUS
# ==========================================================

def nitron_status():

    return {

        "name": "Nitron",

        "version": "5.0",

        "time":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

        "systems": {

            "Brain":
                "online",

            "Code AI":
                "online"
                if code_ai
                else "offline",

            "Speech":
                "online"
                if speak
                else "offline",

            "Daily Devotion":
                "online"

        }

    }



# ==========================================================
# SELF TEST
# ==========================================================

def self_test():

    results = {}


    systems = {

        "Voice Input":
            listen,

        "Voice Output":
            speak,

        "Command System":
            execute,

        "Brain":
            think,

        "Code AI":
            code_ai

    }


    for name, system in systems.items():

        if system:

            results[name] = "OK"

        else:

            results[name] = "FAILED"


    return results



# ==========================================================
# SYSTEM COMMANDS
# ==========================================================

old_process_command = process_command



def process_command(command):

    if command == "nitron status":

        return nitron_status()


    if command == "self test":

        return self_test()


    if command == "daily devotion":

        return get_devotion()


    if command == "hello nitron":

        return "Hello Boss. Nitron is online."


    return old_process_command(command)



# ==========================================================
# START PROGRAM
# ==========================================================

if __name__ == "__main__":

    run()
