# ==========================================================
# NITRON COMMAND SYSTEM v8.0
# PART 1 - CORE FOUNDATION
# ==========================================================

import os
import subprocess


# ==========================================================
# BRAIN CONNECTION
# ==========================================================

try:
    from brain.brain import brain

except Exception as e:

    print("Brain connection error:", e)

    brain = None



# ==========================================================
# MARKET AI CONNECTION
# ==========================================================

try:
    from market_parser import extract_symbol

except Exception:

    extract_symbol = None



try:
    from asset_detector import market_profile

except Exception:

    market_profile = None



try:
    from trade_advisor import advise

except Exception:

    advise = None



# ==========================================================
# APPLICATION SYSTEM
# ==========================================================

APPS = {

    "youtube":
    "com.google.android.youtube",

    "chrome":
    "com.android.chrome",

    "chatgpt":
    "com.openai.chatgpt",

    "whatsapp":
    "com.whatsapp",

    "telegram":
    "org.telegram.messenger",

    "tradingview":
    "com.tradingview.tradingviewapp",

    "metatrader":
    "net.metaquotes.metatrader5"

}



def open_app(name):

    name = name.lower().strip()


    if name not in APPS:

        return f"I don't know the app {name}"


    package = APPS[name]


    try:

        subprocess.run(
            [
                "monkey",
                "-p",
                package,
                "-c",
                "android.intent.category.LAUNCHER",
                "1"
            ],
            capture_output=True
        )


        return f"Opening {name}"


    except Exception as e:

        return f"Cannot open {name}: {e}"



# ==========================================================
# TRADING SYSTEM
# ==========================================================

def analyze_market(command):

    if extract_symbol is None:

        return "Market parser unavailable."


    symbol = extract_symbol(command)


    if symbol is None:

        return (
            "I cannot identify the market. "
            "Try Bitcoin, Ethereum, Gold, Apple, Tesla."
        )


    if advise is None:

        return "Trading advisor unavailable."


    try:

        analysis = advise(symbol)


        profile = None


        if market_profile:

            profile = market_profile(symbol)



        return {

            "symbol": symbol,

            "market_profile": profile,

            "analysis": analysis

        }


    except Exception as e:

        return f"Trading error: {e}"



# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    print(
        "Nitron Command System Part 1 Online"
    )# ==========================================================
# PART 2 - PHONE AND MEDIA SYSTEMS
# ==========================================================


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



def lock_screen():

    os.system(
        "input keyevent 26"
    )

    return "Locking screen."



def notifications():

    os.system(
        "cmd statusbar expand-notifications"
    )

    return "Opening notifications."



def screenshot():

    path = os.path.expanduser(
        "~/Nitron/screenshot.png"
    )


    os.system(
        f"screencap -p {path}"
    )


    return f"Screenshot saved: {path}"



# ==========================================================
# MUSIC
# ==========================================================

try:

    from music import play_song

except Exception:

    play_song = None



def play_music(song=""):


    if play_song:

        try:

            return play_song(song)


        except Exception as e:

            return f"Music error: {e}"


    return "Music system unavailable."



# ==========================================================
# SEARCH
# ==========================================================

try:

    from search import web_search

except Exception:

    web_search = None



def search(query):


    if web_search:

        try:

            return web_search(query)


        except Exception as e:

            return f"Search error: {e}"


    return "Search system unavailable."



# ==========================================================
# WEATHER
# ==========================================================

try:

    from weather import get_weather

except Exception:

    get_weather = None



def weather_report():


    if get_weather:

        try:

            return get_weather()


        except Exception as e:

            return f"Weather error: {e}"


    return "Weather system unavailable."# ==========================================================
# PART 3 - DEVELOPER AND LEARNING SYSTEMS
# ==========================================================


# ==========================================================
# DEVELOPER MODULES
# ==========================================================

try:

    from developer.code_generator import python_project

except Exception:

    python_project = None



try:

    from developer.builder_manager import BuilderManager

    builder = BuilderManager()

except Exception:

    builder = None



# ==========================================================
# GAME BUILDERS
# ==========================================================

try:

    from developer.game_generator import (
        snake,
        racing,
        shooter,
        platformer
    )

except Exception:

    snake = None
    racing = None
    shooter = None
    platformer = None



# ==========================================================
# WEBSITE BUILDERS
# ==========================================================

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



# ==========================================================
# ACADEMY SYSTEM
# ==========================================================

try:

    from academy.python_teacher import ask_python

except Exception:

    ask_python = None



try:

    from physics import ask_physics

except Exception:

    ask_physics = None



# ==========================================================
# DEVELOPER COMMAND HANDLER
# ==========================================================

def developer_command(command):


    if command.startswith(
        "create python project "
    ):

        name = command.replace(
            "create python project ",
            "",
            1
        )


        if python_project:

            return python_project(name)


        return "Python builder unavailable."



    if command == "create snake game":

        if snake:

            return snake()



    if command == "create racing game":

        if racing:

            return racing()



    if command == "create shooter game":

        if shooter:

            return shooter()



    if command == "create platformer game":

        if platformer:

            return platformer()



    if command == "create ecommerce website":

        if ecommerce:

            return ecommerce()



    if command == "create portfolio website":

        if portfolio:

            return portfolio()



    if builder:

        try:

            return builder.handle(command)

        except Exception as e:

            return f"Builder error: {e}"



    return None



# ==========================================================
# LEARNING HANDLER
# ==========================================================

def learning_command(command):


    if command in [
        "teach me python",
        "learn python"
    ]:


        if ask_python:

            return ask_python("topics")


        return "Python teacher unavailable."



    if command.startswith("python "):


        topic = command.replace(
            "python ",
            "",
            1
        )


        if ask_python:

            return ask_python(topic)



    if command == "teach me physics":


        if ask_physics:

            return ask_physics("topics")



    return None# ==========================================================
# PART 4 - MAIN COMMAND ROUTER
# ==========================================================


def execute(command):

    if not command:

        return "Please enter a command."


    command = command.lower().strip()



    # ======================================================
    # OPEN APPS
    # ======================================================

    if command.startswith("open "):

        app = command.replace(
            "open ",
            "",
            1
        )

        return open_app(app)



    # ======================================================
    # PHONE
    # ======================================================

    if command == "home":

        return go_home()


    if command == "back":

        return go_back()


    if command == "lock screen":

        return lock_screen()


    if command == "notifications":

        return notifications()


    if command == "take screenshot":

        return screenshot()



    # ======================================================
    # TRADING
    # ======================================================

    if any(word in command for word in [
        "analyze",
        "analyse",
        "trade",
        "check market"
    ]):

        return analyze_market(command)



    # ======================================================
    # MUSIC
    # ======================================================

    if command == "play music":

        return play_music()



    if command.startswith("play "):

        song = command.replace(
            "play ",
            "",
            1
        )

        return play_music(song)



    # ======================================================
    # SEARCH
    # ======================================================

    if command.startswith("search "):

        query = command.replace(
            "search ",
            "",
            1
        )

        return search(query)



    # ======================================================
    # WEATHER
    # ======================================================

    if "weather" in command:

        return weather_report()



    # ======================================================
    # DEVELOPER
    # ======================================================

    developer = developer_command(command)

    if developer:

        return developer



    # ======================================================
    # LEARNING
    # ======================================================

    learning = learning_command(command)

    if learning:

        return learning



    # ======================================================
    # BRAIN FALLBACK
    # ======================================================

    if brain:

        try:

            return brain.think(command)

        except Exception as e:

            return f"Brain error: {e}"



    return "Sorry Boss, I am still learning that."



# ==========================================================
# TEST MODE
# ==========================================================

if __name__ == "__main__":

    print(
        "Nitron Command System v8.0 Online"
    )


    while True:

        command = input(
            ">>> "
        )


        if command.lower() in [
            "exit",
            "quit"
        ]:

            break


        print(
            execute(command)
        )
