import os
import sys
import json
import time
import random
import datetime
import threading
import subprocess
from pathlib import Path

from speech import speak, listen
from commands import execute
from phone import call_contact, message_contact
from trade_advisor import advise, print_advice

from developer.builder_manager import BuilderManager

from academy.japanese import teach

builder = BuilderManager()

VERSION = "2.0"

AUTHOR = "Boss Nimrod"

PROJECT = "Nitron"

HOME = Path.home()

NITRON = HOME / "Nitron"

ACADEMY = NITRON / "academy"

DEVELOPER = NITRON / "developer"

PROJECTS = NITRON / "projects"

DATABASE = NITRON / "database"

MEMORY = NITRON / "memory"

LOGS = NITRON / "logs"

DOWNLOADS = HOME / "storage" / "downloads"

MUSIC = HOME / "storage" / "music"

PICTURES = HOME / "storage" / "pictures"

VIDEOS = HOME / "storage" / "movies"

DOCUMENTS = HOME / "storage" / "documents"

for folder in [

    PROJECTS,
    DATABASE,
    MEMORY,
    LOGS

]:

    os.makedirs(folder, exist_ok=True)


def log(text):

    with open(LOGS / "nitron.log", "a") as f:

        now = datetime.datetime.now()

        f.write(f"[{now}] {text}\n")


def startup():

    log("Nitron started")

    print("=" * 60)

    print("NITRON AI ASSISTANT")

    print("=" * 60)

    print("Version :", VERSION)

    print("Owner   :", AUTHOR)

    print("Project :", PROJECT)

    print("=" * 60)

    speak("Nitron is online Boss Nimrod.")



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
      ◆◆◆◇◇◇◆◆◆
        ◆◆◆◆◆◆◆
          ◆◆◆◆◆
             ◆
""",

"""
             ◈
          ◈◈◈◈◈
        ◈◈◈◈◈◈◈
      ◈◈◈◆◆◆◈◈◈
        ◈◈◈◈◈◈◈
          ◈◈◈◈◈
             ◈
""",

"""
             ♦
          ♦♦♦♦♦
        ♦♦♦♦♦♦♦
      ♦♦♦◈◈◈♦♦♦
        ♦♦♦♦♦♦♦
          ♦♦♦♦♦
             ♦
"""

]

frame = 0


def screen(status):

    global frame

    os.system("clear")

    print(frames[frame])

    frame = (frame + 1) % len(frames)

    print("=" * 60)
    print("               N I T R O N")
    print("=" * 60)
    print("Status :", status)
    print("Version:", VERSION)
    print("Owner  :", AUTHOR)
    print("Wake   : Hey Nitron")
    print("=" * 60)


while True:

    screen("LISTENING")

    command = listen()

    if not command:

        time.sleep(1)

        continue

    command = command.lower().strip()

    log(command)

    corrections = {

        "by gold": "buy gold",
        "bye gold": "buy gold",
        "by bitcoin": "buy bitcoin",
        "bye bitcoin": "buy bitcoin",
        "by btc": "buy btc",
        "bye btc": "buy btc",
        "by apple": "buy apple",
        "bye apple": "buy apple",
        "face book": "facebook",
        "you tube": "youtube",
        "chat gpt": "chatgpt",
        "meta trader": "metatrader",
        "x au usd": "xauusd",
        "btc usd": "btcusd",
        "good by": "goodbye",
        "good bye": "goodbye",
        "quit nitron": "quit",
        "close nitron": "quit"

    }

    for wrong, correct in corrections.items():

        command = command.replace(wrong, correct)

    print("You:", command)    # ------------------------------
    # Trading Analysis
    # ------------------------------

    if command.startswith("analyze"):

        parts = command.split()

        if len(parts) < 2:

            speak("Please tell me which market to analyze.")

            continue

        symbol = parts[1].upper()

        try:

            advice = advise(symbol)

            print_advice(advice)

            speech = f"{advice['symbol']}. "

            speech += f"Recommendation {advice['action']}. "

            if "confidence" in advice:
                speech += f"Confidence {advice['confidence']} percent. "

            if "entry" in advice:
                speech += f"Entry {advice['entry']}. "

            if "stop_loss" in advice:
                speech += f"Stop loss {advice['stop_loss']}. "

            if "take_profit" in advice:
                speech += f"Take profit {advice['take_profit']}. "

            if "risk_reward" in advice:
                speech += f"Risk reward {advice['risk_reward']}. "

            if "reason" in advice:
                speech += advice["reason"]

            speak(speech)

        except Exception as e:

            print(e)

            speak("Analysis failed.")

        continue


    if command in ["analyze gold", "gold analysis"]:

        advice = advise("XAUUSD")

        print_advice(advice)

        speak(advice["action"])

        continue


    if command in ["analyze bitcoin", "bitcoin analysis"]:

        advice = advise("BTCUSD")

        print_advice(advice)

        speak(advice["action"])

        continue


    if command in ["analyze apple", "apple analysis"]:

        advice = advise("AAPL")

        print_advice(advice)

        speak(advice["action"])

        continue


    if command.startswith("buy "):

        symbol = command.replace("buy", "").strip().upper()

        speak(f"Buy signal received for {symbol}")

        continue


    if command.startswith("sell "):

        symbol = command.replace("sell", "").strip().upper()

        speak(f"Sell signal received for {symbol}")

        continue


    if command == "market summary":

        speak("Market summary is not available yet.")

        continue


    if command == "trading tips":

        speak("Trade with discipline, use stop losses, and manage your risk.")

        continue


    if command == "risk management":

        speak("Never risk more than two percent of your account on one trade.")

        continue


    if command == "forex pairs":

        speak("Popular pairs include Euro Dollar, Pound Dollar, Dollar Yen, and Dollar Swiss Franc.")

        continue


    if command == "crypto markets":

        speak("Popular crypto markets include Bitcoin, Ethereum, Solana, XRP, and BNB.")

        continue


    if command == "stock markets":

        speak("Popular stocks include Apple, Microsoft, NVIDIA, Amazon, Tesla, and Google.")

        continue


    if command == "what can you trade":

        speak("I can analyze forex, stocks, cryptocurrencies, commodities, and indices.")

        continue    # ------------------------------
    # Developer Commands
    # ------------------------------

    if command.startswith("create python project"):

        name = command.replace("create python project", "").strip()

        if not name:
            name = "python_project"

        speak(builder.projects.create_python_project(name))

        continue


    if command.startswith("create website"):

        name = command.replace("create website", "").strip()

        if not name:
            name = "website"

        speak(builder.projects.create_website(name))

        continue


    if command.startswith("create flask app"):

        name = command.replace("create flask app", "").strip()

        if not name:
            name = "flask_app"

        speak(builder.projects.create_flask(name))

        continue


    if command.startswith("create fastapi app"):

        name = command.replace("create fastapi app", "").strip()

        if not name:
            name = "fastapi_app"

        speak(builder.projects.create_fastapi(name))

        continue


    if command.startswith("create django project"):

        name = command.replace("create django project", "").strip()

        if not name:
            name = "django_project"

        speak(builder.projects.create_django(name))

        continue


    if command.startswith("create react app"):

        name = command.replace("create react app", "").strip()

        if not name:
            name = "react_app"

        speak(builder.projects.create_react(name))

        continue


    if command.startswith("create node project"):

        name = command.replace("create node project", "").strip()

        if not name:
            name = "node_project"

        speak(builder.projects.create_node(name))

        continue


    if command.startswith("create api project"):

        name = command.replace("create api project", "").strip()

        if not name:
            name = "api_project"

        speak(builder.projects.create_api(name))

        continue


    if command.startswith("create ai project"):

        name = command.replace("create ai project", "").strip()

        if not name:
            name = "ai_project"

        speak(builder.projects.create_ai(name))

        continue


    if command.startswith("create game"):

        name = command.replace("create game", "").strip()

        if not name:
            name = "game"

        speak(builder.projects.create_game(name))

        continue


    if command.startswith("create desktop app"):

        name = command.replace("create desktop app", "").strip()

        if not name:
            name = "desktop_app"

        speak(builder.projects.create_desktop(name))

        continue


    if command.startswith("create mobile app"):

        name = command.replace("create mobile app", "").strip()

        if not name:
            name = "mobile_app"

        speak(builder.projects.create_mobile(name))

        continue


    if command == "list builders":

        names = builder.list_builders()

        print("\nInstalled Builders:\n")

        for item in names:

            print("-", item)

        speak(f"There are {len(names)} builders available.")

        continue    # ------------------------------
    # Learning Commands
    # ------------------------------

    if command == "teach me japanese":

        lesson = teach()

        print(lesson)

        speak(lesson)

        continue


    if command == "japanese lesson one":

        lesson = teach()

        print(lesson)

        speak(lesson)

        continue


    if command == "teach me python":

        speak(
            "Python is a powerful programming language. "
            "Let's begin with variables, data types, loops, functions, and classes."
        )

        continue


    if command == "teach me html":

        speak(
            "HTML is used to build the structure of web pages. "
            "The main tags are html, head, body, h1, p, img, and a."
        )

        continue


    if command == "teach me css":

        speak(
            "CSS controls colors, layouts, fonts, spacing, animations, and responsive design."
        )

        continue


    if command == "teach me javascript":

        speak(
            "JavaScript makes websites interactive. "
            "It can respond to clicks, keyboard input, and communicate with servers."
        )

        continue


    if command == "teach me programming":

        speak(
            "Programming is the process of writing instructions that computers follow to solve problems."
        )

        continue


    if command == "teach me mathematics":

        speak(
            "I can teach arithmetic, algebra, geometry, trigonometry, calculus, and statistics."
        )

        continue


    if command == "teach me physics":

        speak(
            "I can teach mechanics, electricity, magnetism, waves, optics, and modern physics."
        )

        continue


    if command == "teach me chemistry":

        speak(
            "I can teach atoms, molecules, reactions, acids, bases, salts, and organic chemistry."
        )

        continue


    if command == "teach me biology":

        speak(
            "I can teach cells, genetics, human anatomy, plants, animals, and ecosystems."
        )

        continue


    if command == "teach me history":

        speak(
            "I can teach ancient civilizations, world wars, African history, and modern history."
        )

        continue


    if command == "teach me geography":

        speak(
            "I can teach continents, countries, climates, rivers, mountains, and maps."
        )

        continue


    if command == "start quiz":

        speak(
            "Quiz mode will be available soon."
        )

        continue    # ------------------------------
    # AI Assistant Commands
    # ------------------------------

    if command == "who are you":

        speak(
            "I am Nitron, your artificial intelligence assistant. "
            "I can help you learn, build software, analyze markets, and manage projects."
        )

        continue


    if command == "what can you do":

        speak(
            "I can teach subjects, create software projects, analyze financial markets, "
            "help with programming, manage files, and answer questions."
        )

        continue


    if command == "help":

        speak(
            "You can ask me to create websites, games, Python projects, "
            "mobile apps, AI projects, databases, and much more."
        )

        continue


    if command == "system status":

        speak("All systems are online.")

        print("=" * 60)
        print("NITRON STATUS")
        print("=" * 60)
        print("Version :", VERSION)
        print("Owner   :", AUTHOR)
        print("Project :", PROJECT)
        print("Directory:", os.getcwd())
        print("=" * 60)

        continue


    if command == "version":

        speak(f"Nitron version {VERSION}")

        continue


    if command == "current directory":

        speak(os.getcwd())

        continue


    if command == "list folders":

        folders = []

        for item in os.listdir("."):

            if os.path.isdir(item):

                folders.append(item)

        for folder in folders:

            print(folder)

        speak(f"I found {len(folders)} folders.")

        continue


    if command == "list files":

        files = os.listdir(".")

        for file in files:

            print(file)

        speak("The files are displayed on the screen.")

        continue


    if command.startswith("make folder"):

        name = command.replace("make folder", "").strip()

        if not name:

            name = "NewFolder"

        os.makedirs(name, exist_ok=True)

        speak(f"{name} created successfully.")

        continue


    if command == "time":

        now = datetime.datetime.now()

        speak(now.strftime("%I:%M %p"))

        continue


    if command == "date":

        today = datetime.datetime.now()

        speak(today.strftime("%d %B %Y"))

        continue


    if command in [

        "exit",
        "quit",
        "shutdown nitron",
        "stop nitron",
        "goodbye"

    ]:

        speak("Goodbye Boss Nimrod.")

        break    # ------------------------------
    # Phone Commands
    # ------------------------------

    reply = call_contact(command)

    if reply:

        speak(reply)

        continue


    reply = message_contact(command)

    if reply:

        speak(reply)

        continue


    # ------------------------------
    # General Commands
    # ------------------------------

    reply = execute(command)

    if reply:

        print("Nitron:", reply)

        speak(reply)

        continue


    # ------------------------------
    # AI Conversation
    # ------------------------------

    if command in [

        "hello",
        "hi",
        "hey"

    ]:

        speak("Hello Boss Nimrod. How can I help you today?")

        continue


    if command == "good morning":

        speak("Good morning Boss Nimrod. I hope you have a productive day.")

        continue


    if command == "good afternoon":

        speak("Good afternoon Boss Nimrod.")

        continue


    if command == "good evening":

        speak("Good evening Boss Nimrod.")

        continue


    if command == "thank you":

        speak("You're welcome Boss Nimrod.")

        continue


    if command == "how are you":

        speak("I am functioning perfectly and ready to assist you.")

        continue


    if command == "tell me a joke":

        jokes = [

            "Why do programmers prefer dark mode? Because light attracts bugs.",

            "I would tell you a UDP joke, but you might not get it.",

            "There are ten kinds of people. Those who understand binary and those who don't."

        ]

        speak(random.choice(jokes))

        continue


    if command == "motivate me":

        speak(
            "Success comes from learning, practicing, and never giving up. Keep building Nitron."
        )

        continue


    if command == "open projects":

        if PROJECTS.exists():

            print("\nProjects\n")

            for project in os.listdir(PROJECTS):

                print("-", project)

            speak("Projects displayed on the screen.")

        else:

            speak("Projects folder not found.")

        continue


    if command == "clear screen":

        os.system("clear")

        continue


    if command == "restart nitron":

        speak("Restarting Nitron.")

        os.execv(sys.executable, [sys.executable] + sys.argv)

        continue


    # ------------------------------
    # Unknown Command
    # ------------------------------

    print("Unknown command:", command)

    speak(
        "Sorry Boss Nimrod. "
        "I do not understand that command yet."
    )
