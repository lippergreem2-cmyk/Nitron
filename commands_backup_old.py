# ==========================================================
# NITRON COMMAND SYSTEM v4
# Part 1/4
# ==========================================================

import os
import subprocess


# ==========================================================
# BRAIN
# ==========================================================

try:
    from brain import ask
except Exception as e:
    print("Brain error:", e)

    def ask(command):
        return None



# ==========================================================
# TRADING MODULES
# ==========================================================

try:
    from trade_controller import (
        analyze_trade,
        place_trade,
        show_trades,
        close_trade_by_ticket
    )

except Exception as e:

    print("Trading controller error:", e)

    analyze_trade = None
    place_trade = None
    show_trades = None
    close_trade_by_ticket = None



# ==========================================================
# MEDIA
# ==========================================================

try:
    from media.image_generator import generate_image
except Exception:
    generate_image = None


try:
    from media.video_generator import generate_video
except Exception:
    generate_video = None



# ==========================================================
# DEVELOPER TOOLS
# ==========================================================

try:
    from developer.code_generator import python_project
except Exception:
    python_project = None


try:
    from developer.game_generator import (
        snake,
        platformer,
        racing,
        shooter
    )

except Exception:

    snake = None
    platformer = None
    racing = None
    shooter = None



try:
    from developer.website_generator import (
        portfolio,
        landing_page,
        ecommerce
    )

except Exception:

    portfolio = None
    landing_page = None
    ecommerce = None



try:
    from developer.chatbot_generator import (
        ai_assistant,
        discord_bot,
        telegram_bot,
        whatsapp_bot
    )

except Exception:

    ai_assistant = None
    discord_bot = None
    telegram_bot = None
    whatsapp_bot = None



try:
    from developer.app_generator import (
        calculator,
        weather,
        notes,
        media_player
    )

except Exception:

    calculator = None
    weather = None
    notes = None
    media_player = None



# ==========================================================
# OPTIONAL MODULES
# ==========================================================

try:
    from phone import (
        call_contact,
        message_contact
    )

except Exception:

    call_contact = None
    message_contact = None



try:
    from weather import get_weather
except Exception:

    get_weather = None



try:
    from music import play_song
except Exception:

    play_song = None



try:
    from search import web_search
except Exception:

    web_search = None



try:
    from academy.python_teacher import ask_python
except Exception:

    ask_python = None



try:
    from academy.cpp_teacher import ask_cpp
except Exception:

    ask_cpp = None



try:
    from academy.japanese import teach
except Exception:

    teach = None



try:
    from physics import ask_physics
except Exception:

    ask_physics = None



try:
    from developer.builder_manager import BuilderManager

    builder = BuilderManager()

except Exception:

    builder = None# ==========================================================
# APPLICATIONS
# ==========================================================

APPS = {

    "camera": "com.sec.android.app.camera",
    "gallery": "com.sec.android.gallery3d",
    "settings": "com.android.settings",

    "phone": "com.samsung.android.dialer",
    "contacts": "com.samsung.android.contacts",
    "messages": "com.samsung.android.messaging",

    "calculator": "com.sec.android.app.popupcalculator",
    "calendar": "com.samsung.android.calendar",
    "clock": "com.sec.android.app.clockpackage",
    "files": "com.sec.android.app.myfiles",

    "chrome": "com.android.chrome",
    "google": "com.google.android.googlequicksearchbox",
    "gmail": "com.google.android.gm",
    "maps": "com.google.android.apps.maps",

    "youtube": "com.google.android.youtube",
    "play store": "com.android.vending",

    "chatgpt": "com.openai.chatgpt",

    "whatsapp": "com.whatsapp",
    "telegram": "org.telegram.messenger",

    "facebook": "com.facebook.katana",
    "messenger": "com.facebook.orca",

    "instagram": "com.instagram.android",
    "instagram lite": "com.instagram.lite",

    "spotify": "com.spotify.music",
    "audiomack": "com.audiomack",

    "tradingview": "com.tradingview.tradingviewapp",
    "metatrader": "net.metaquotes.metatrader5"

}



# ==========================================================
# OPEN APPLICATION
# ==========================================================

def open_app(app):

    app = app.lower().strip()


    if app not in APPS:

        return (
            f"I don't know the app {app}"
        )


    package = APPS[app]


    commands = [

        [
            "monkey",
            "-p",
            package,
            "-c",
            "android.intent.category.LAUNCHER",
            "1"
        ],


        [
            "am",
            "start",
            "-a",
            "android.intent.action.MAIN",
            "-c",
            "android.intent.category.LAUNCHER",
            "-p",
            package
        ]

    ]


    for cmd in commands:

        try:

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True
            )


            output = (
                result.stdout +
                result.stderr
            )


            if (
                result.returncode == 0
                and "Error" not in output
            ):

                return (
                    f"Opening {app}."
                )


        except Exception:

            pass



    return (
        f"Could not open {app}."
    )



# ==========================================================
# PHONE CONTROLS
# ==========================================================

def go_home():

    os.system(
        "input keyevent 3"
    )

    return "Going home."



def go_back():

    os.system(
        "input keyevent 4"
    )

    return "Going back."



def recent_apps():

    os.system(
        "input keyevent KEYCODE_APP_SWITCH"
    )

    return "Opening recent apps."



def notifications():

    os.system(
        "cmd statusbar expand-notifications"
    )

    return "Opening notifications."



def quick_settings():

    os.system(
        "cmd statusbar expand-settings"
    )

    return "Opening quick settings."



def lock_screen():

    os.system(
        "input keyevent 26"
    )

    return "Locking screen."



def screenshot():

    path = os.path.expanduser(
        "~/Nitron/screenshot.png"
    )


    os.system(
        f"screencap -p {path}"
    )


    return (
        f"Screenshot saved: {path}"
    )



# ==========================================================
# MEDIA FUNCTIONS
# ==========================================================

def play_music(song=""):

    if play_song:

        try:

            return play_song(song)

        except Exception as e:

            return (
                f"Music error: {e}"
            )


    return "Music module unavailable."



def search(query):

    if web_search:

        try:

            return web_search(query)

        except Exception as e:

            return (
                f"Search error: {e}"
            )


    return "Search module unavailable."



def weather_report():

    if get_weather:

        try:

            return get_weather()

        except Exception as e:

            return (
                f"Weather error: {e}"
            )


    return "Weather module unavailable."# ==========================================================
# HELP SYSTEM
# ==========================================================

def help_menu():

    return """

==============================
        NITRON AI v4
==============================

PHONE
-----
open youtube
open chrome
home
back
recent apps
notifications
quick settings
lock screen
take screenshot


TRADING
--------
analyze xauusd
analyze btcusd
trade xauusd
place trade
show trades
close trade 123456


LEARNING
--------
teach me python
teach me c++
teach me physics
teach me japanese


MEDIA
-----
play music
search something
weather


DEVELOPER
---------
create python project test
create snake game
create website
create ai assistant


==============================

"""


# ==========================================================
# MAIN TEST LOOP
# ==========================================================

if __name__ == "__main__":

    print(
        "Nitron Command System Online"
    )


    while True:

        command = input(
            ">>> "
        )


        if command.lower() in (
            "exit",
            "quit"
        ):

            print(
                "Nitron shutting down."
            )

            break


        result = execute(
            command
        )


        print(
            result
        )# ==========================================================
# HELP SYSTEM
# ==========================================================

def help_menu():

    return """

==============================
          NITRON AI
==============================

GENERAL
-------
help
hello
who are you


PHONE
-----
open youtube
open chrome
home
back
recent apps
notifications
quick settings
lock screen
take screenshot


TRADING
--------
analyze xauusd
analyze btcusd
trade xauusd
place trade
show trades
close trade 123456


LEARNING
--------
teach me python
teach me c++
teach me physics
teach me japanese


MEDIA
-----
play music
search python
weather


DEVELOPER
---------
create python project test
create snake game
create website
create ai assistant


==============================

"""


# ==========================================================
# MAIN TEST
# ==========================================================

if __name__ == "__main__":

    print(
        "Nitron Command System Online"
    )


    while True:

        command = input(
            ">>> "
        )


        if command.lower() in (
            "exit",
            "quit"
        ):

            break


        try:

            response = execute(
                command
            )

            print(response)


        except Exception as e:

            print(
                "Command error:",
                e
            )
