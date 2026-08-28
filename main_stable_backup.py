# ~/Nitron/main.py

import os
import time
import datetime


# =========================
# CORE SYSTEM IMPORTS
# =========================

from speech import speak, listen


# =========================
# ACADEMY SYSTEM
# =========================

try:
    from academy.academy import teach

except Exception as e:
    print("Academy error:", e)

    def teach(topic):
        return "Academy system unavailable."



# =========================
# BRAIN SYSTEM
# =========================

try:
    from brain import think

except Exception as e:
    print("Brain error:", e)

    def think(command):
        return None



# =========================
# PHONE SYSTEM
# =========================

try:
    from phone import call_contact, message_contact

except Exception:

    call_contact = None
    message_contact = None



# =========================
# TRADING SYSTEM
# =========================

try:
    from trade_advisor import advise, print_advice

except Exception as e:

    print("Trading error:", e)

    advise = None
    print_advice = None



# =========================
# DEVELOPER BUILDER SYSTEM
# =========================

try:

    from developer.builder_manager import BuilderManager

    builder = BuilderManager()


except Exception as e:

    print("Builder error:", e)

    builder = None



# =========================
# ANDROID BUBBLE CONNECTION
# =========================

try:

    import bubble_service

    bubble = True


except Exception:

    bubble = False



# =========================
# NITRON DISPLAY
# =========================

frames = [

"""
             ◇
          ◇◇◇◇◇
        ◇◇◇◇◇◇◇
      ◇◇◇◆◆◆◇◇◇
        ◇◇◇◇◇◇◇
          ◇◇◇◇◇
             ◇
""",


"""
             ◆
          ◆◆◆◆◆
        ◆◆◆◆◆◆◆
      ◇◇◇◆◆◆◇◇◇
        ◆◆◆◆◆◆◆
          ◆◆◆◆◆
             ◆
"""

]


frame = 0


def screen(status):

    global frame

    os.system("clear")

    print(frames[frame])

    frame = (frame + 1) % len(frames)

    print("=" * 60)
    print("                 N I T R O N")
    print("=" * 60)
    print("Status :", status)
    print("Wake   : Hey Nitron")
    print("=" * 60)# =========================
# STARTUP SYSTEM
# =========================

def startup():

    screen("ONLINE")

    speak(
        "Nitron is online Boss Nimrod."
    )


    if bubble:

        try:

            bubble_service.start()

        except Exception as e:

            print(
                "Bubble error:",
                e
            )



# =========================
# COMMAND CLEANER
# =========================

def clean_command(command):

    command = command.lower().strip()


    corrections = {

        "by gold": "buy gold",
        "bye gold": "buy gold",

        "by bitcoin": "buy bitcoin",
        "bye bitcoin": "buy bitcoin",

        "by btc": "buy btc",
        "bye btc": "buy btc",

        "by apple": "buy apple",
        "bye apple": "buy apple",

        "x au usd": "xauusd",
        "btc usd": "btcusd",

        "face book": "facebook"

    }


    if command in corrections:

        command = corrections[command]


    return command



# =========================
# EXIT SYSTEM
# =========================

def check_exit(command):

    exits = [

        "exit",
        "quit",
        "goodbye",
        "shutdown nitron",
        "stop nitron"

    ]


    return command in exits



# =========================
# MAIN LOOP START
# =========================

def main():

    startup()


    while True:


        screen("LISTENING")


        command = listen()



        if not command:

            time.sleep(1)

            continue



        command = clean_command(command)



        if check_exit(command):

            speak(
                "Goodbye Boss Nimrod."
            )

            break        # =========================
        # AI BRAIN
        # =========================

        response = think(command)


        if response:

            speak(response)

            continue



        # =========================
        # ACADEMY / TEACHING
        # =========================

        if command.startswith("teach me"):

            topic = command.replace(
                "teach me",
                ""
            ).strip()


            if not topic:

                speak(
                    "Please tell me what you want to learn."
                )

                continue


            try:

                lesson = teach(topic)

                speak(lesson)


            except Exception as e:

                print(
                    "Teaching error:",
                    e
                )

                speak(
                    "Academy system error."
                )


            continue



        # =========================
        # TRADING ANALYSIS
        # =========================

        if command.startswith("analyze"):


            parts = command.split()


            if len(parts) < 2:

                speak(
                    "Please tell me the symbol to analyze."
                )

                continue



            symbol = parts[1].upper()



            if advise:

                try:

                    advice = advise(symbol)


                    if print_advice:

                        print_advice(advice)



                    message = (

                        f"{advice.get('symbol', symbol)}. "

                        f"Recommendation "

                        f"{advice.get('action', 'unknown')}."

                    )


                    if "confidence" in advice:

                        message += (

                            f" Confidence "

                            f"{advice['confidence']} percent."

                        )


                    if "reason" in advice:

                        message += (

                            " "

                            + advice["reason"]

                        )


                    speak(message)



                except Exception as e:

                    print(
                        "Trading error:",
                        e
                    )

                    speak(
                        "I could not analyze that market."
                    )


            else:

                speak(
                    "Trading system unavailable."
                )


            continue        # =========================
        # QUICK MARKET COMMANDS
        # =========================

        if command in [
            "analyze gold",
            "gold analysis"
        ]:


            if advise:

                advice = advise("XAUUSD")


                if print_advice:

                    print_advice(advice)


                speak(
                    advice.get(
                        "action",
                        "No signal"
                    )
                )


            continue




        if command in [
            "analyze bitcoin",
            "bitcoin analysis"
        ]:


            if advise:

                advice = advise("BTCUSD")


                if print_advice:

                    print_advice(advice)


                speak(
                    advice.get(
                        "action",
                        "No signal"
                    )
                )


            continue




        if command in [
            "analyze apple",
            "apple analysis"
        ]:


            if advise:

                advice = advise("AAPL")


                if print_advice:

                    print_advice(advice)


                speak(
                    advice.get(
                        "action",
                        "No signal"
                    )
                )


            continue




        # =========================
        # BUY SYSTEM
        # =========================

        if command.startswith("buy "):


            symbol = command.replace(
                "buy ",
                ""
            ).upper()



            speak(
                f"Buy signal received for {symbol}"
            )


            continue




        # =========================
        # SELL SYSTEM
        # =========================

        if command.startswith("sell "):


            symbol = command.replace(
                "sell ",
                ""
            ).upper()



            speak(
                f"Sell signal received for {symbol}"
            )


            continue        # =========================
        # DEVELOPER BUILDER SYSTEM
        # =========================

        if builder:


            if command.startswith("create python project"):


                name = command.replace(
                    "create python project",
                    ""
                ).strip()


                if not name:

                    name = "python_project"



                speak(
                    builder.projects.create_python_project(name)
                )


                continue




            if command.startswith("create website"):


                name = command.replace(
                    "create website",
                    ""
                ).strip()


                if not name:

                    name = "website"



                speak(
                    builder.projects.create_website(name)
                )


                continue




            if command.startswith("create flask app"):


                name = command.replace(
                    "create flask app",
                    ""
                ).strip()


                if not name:

                    name = "flask_app"



                speak(
                    builder.projects.create_flask(name)
                )


                continue




            if command.startswith("create fastapi app"):


                name = command.replace(
                    "create fastapi app",
                    ""
                ).strip()


                if not name:

                    name = "fastapi_app"



                speak(
                    builder.projects.create_fastapi(name)
                )


                continue




        # =========================
        # UNKNOWN COMMAND
        # =========================

        speak(
            "I did not understand that command."
        )



# =========================
# PROGRAM START
# =========================

if __name__ == "__main__":

    main()
