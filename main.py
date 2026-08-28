# ==========================================================
# NITRON AI ASSISTANT
# main.py
# Version 9.0
# Conversation + Smart Interrupt Edition
# ==========================================================

import os
import time
import traceback
import threading
from datetime import datetime


# ==========================================================
# VOICE SYSTEM
# ==========================================================

try:

    from speech import (
        speech_state,
        listen,
        speak,
        stop_speaking,
        user_started_talking,
        is_speaking,
        interrupt_monitor
    )


except Exception as error:

    print(
        "Speech loading error:",
        error
    )


    speech_state = {

        "ignore_input": False,

        "speaking": False

    }


    def listen():

        return input("You: ")



    def speak(text):

        print(
            "Nitron:",
            text
        )



    def stop_speaking():

        pass



    def user_started_talking():

        pass



    def is_speaking():

        return False



    def interrupt_monitor():

        pass



# ==========================================================
# COMMAND SYSTEM
# ==========================================================

try:

    from commands import execute


except Exception as error:

    print(
        "Command loading error:",
        error
    )


    def execute(command):

        return None



# ==========================================================
# BRAIN SYSTEM
# ==========================================================

try:

    from brain import think


except Exception:


    def think(command):

        return "Brain unavailable."# ==========================================================
# DAILY DEVOTION
# ==========================================================

try:

    from daily.devotion import get_devotion


except Exception:


    def get_devotion():

        return "Daily devotion unavailable."



# ==========================================================
# CONVERSATION MEMORY
# ==========================================================

conversation = {

    "last_user": "",

    "last_reply": "",

    "active": True

}



def remember_chat(user, reply):

    conversation["last_user"] = user

    conversation["last_reply"] = reply



# ==========================================================
# DISPLAY SYSTEM
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


    print("=" * 50)

    print(
        "              N I T R O N"
    )

    print("=" * 50)

    print(
        "Status:",
        status
    )

    print(
        "Wake: Hey Nitron"
    )

    print(
        datetime.now().strftime("%H:%M:%S")
    )

    print("=" * 50)



# ==========================================================
# DAILY DEVOTION SYSTEM
# ==========================================================

def daily_devotion():

    while True:

        try:

            now = datetime.now()


            if (
                now.hour == 3
                and now.minute == 0
            ):

                message = get_devotion()


                print(
                    message
                )


                speak(
                    message
                )


                time.sleep(3600)



        except Exception as error:

            print(
                "Devotion error:",
                error
            )


        time.sleep(30)



def start_daily_system():

    threading.Thread(

        target=daily_devotion,

        daemon=True

    ).start()# ==========================================================
# COMMAND CLEANER
# ==========================================================

def clean_command(command):

    if not command:

        return ""


    command = command.lower().strip()


    replacements = {

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


    return replacements.get(

        command,

        command

    )



# ==========================================================
# EXIT COMMANDS
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
# COMMAND HANDLER
# ==========================================================

def handle_commands(command):

    try:

        result = execute(command)


        if result:

            return result


    except Exception as error:

        print(
            "Command error:",
            error
        )


    return None



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


    keywords = [

        "analyze",

        "analyse",

        "trade",

        "buy",

        "sell",

        "market",

        "xauusd",

        "btcusd"

    ]


    if not any(

        word in command

        for word in keywords

    ):

        return None


    try:

        return advise(command)


    except Exception as error:

        return (

            f"Trading error: {error}"

        )



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


    if command.startswith(

        "create python project"

    ):


        try:

            name = command.replace(

                "create python project",

                "",

                1

            ).strip()


            if not name:

                name = "python_project"



            return builder.python.create_program(

                name

            )


        except Exception as error:

            return (

                f"Builder error: {error}"

            )


    return None



# ==========================================================
# CONVERSATION HANDLER
# ==========================================================

def handle_conversation(command):

    try:

        reply = think(command)


        if reply:

            remember_chat(

                command,

                reply

            )


            return reply


    except Exception as error:

        print(

            "Conversation error:",

            error

        )


    return None



# ==========================================================
# MAIN ROUTER
# ==========================================================

def process_command(command):


    handlers = [

        handle_commands,

        handle_trading,

        handle_builder,

        handle_conversation

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

        "I am still learning that."

    )# ==========================================================
# STARTUP
# ==========================================================

def startup():

    banner(
        "STARTING"
    )


    print(
        "Loading Nitron systems..."
    )


    print(
        "[ OK ] Brain"
    )

    print(
        "[ OK ] Commands"
    )

    print(
        "[ OK ] Voice"
    )

    print(
        "[ OK ] Conversation"
    )

    print(
        "[ OK ] Interrupt System"
    )

    print(
        "[ OK ] Daily Devotion"
    )


    # Start interrupt listener

    threading.Thread(

        target=interrupt_monitor,

        daemon=True

    ).start()



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


            banner(

                "LISTENING"

            )


            command = listen()



            if not command:

                time.sleep(1)

                continue



            # Ignore words captured while stopping speech

            if speech_state.get(

                "ignore_input",

                False

            ):


                speech_state["ignore_input"] = False

                continue



            command = clean_command(

                command

            )



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



            remember_chat(

                command,

                response

            )



            speak(

                str(response)

            )



        except KeyboardInterrupt:


            print(

                "Nitron stopped."

            )


            break



        except Exception as error:


            print(

                "SYSTEM ERROR:",

                error

            )


            traceback.print_exc()


            time.sleep(2)



# ==========================================================
# STATUS SYSTEM
# ==========================================================

def nitron_status():

    return {

        "name":

            "Nitron",


        "version":

            "9.0",


        "time":

            datetime.now().strftime(

                "%Y-%m-%d %H:%M:%S"

            ),


        "systems":

        {

            "Brain":

                "online",


            "Commands":

                "online",


            "Voice":

                "online",


            "Conversation":

                "online",


            "Interrupt":

                "online"

        }

    }



# ==========================================================
# START PROGRAM
# ==========================================================

if __name__ == "__main__":

    run()
