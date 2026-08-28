# ==========================================================
# NITRON AI ASSISTANT
# Version 3.0
# main.py
# Part 1/8
# ==========================================================

import os
import sys
import time
import traceback
from datetime import datetime

from speech import listen, speak
from commands import execute

# ==========================================================
# OPTIONAL MODULES
# ==========================================================

try:
    from brain import think
except Exception:
    def think(command):
        return None

try:
    from academy.academy import teach
except Exception:
    def teach(topic):
        return "Academy unavailable."

try:
    from trade_advisor import advise
except Exception:
    advise = None

try:
    from developer.builder_manager import BuilderManager
    builder = BuilderManager()
except Exception:
    builder = None

try:
    from command_router import router
except Exception:
    router = None

try:
    from plugin_manager import plugin_manager
except Exception:
    plugin_manager = None

try:
    from nitron_core import nitron
except Exception:
    nitron = None

try:
    from memory_manager import memory
except Exception:
    memory = None

try:
    from workflow_manager import workflow
except Exception:
    workflow = None

try:
    from task_manager import tasks
except Exception:
    tasks = None

try:
    from automation_manager import automation
except Exception:
    automation = None

try:
    from job_manager import jobs
except Exception:
    jobs = None

# ==========================================================
# DISPLAY
# ==========================================================

FRAMES = [

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
"""

]

frame = 0


def clear():

    os.system("clear")


def banner(status):

    global frame

    clear()

    print(FRAMES[frame])

    frame = (frame + 1) % len(FRAMES)

    print("=" * 60)
    print("                     N I T R O N")
    print("=" * 60)
    print("Status :", status)
    print("Wake   : Hey Nitron")
    print("Time   :", datetime.now().strftime("%H:%M:%S"))
    print("=" * 60)


# ==========================================================
# STARTUP
# ==========================================================

def startup():

    banner("STARTING")

    print("Loading modules...\n")

    modules = [

        ("Brain", think),
        ("Academy", teach),
        ("Builder", builder),
        ("Command Router", router),
        ("Plugin Manager", plugin_manager),
        ("Nitron Core", nitron),
        ("Memory", memory),
        ("Workflow", workflow),
        ("Tasks", tasks),
        ("Automation", automation),
        ("Jobs", jobs)

    ]

    for name, module in modules:

        if module:

            print(f"[ OK ] {name}")

        else:

            print(f"[ -- ] {name} unavailable")

    print()

    speak("Nitron is online. Welcome back Boss.")# ==========================================================
# COMMAND CLEANER
# ==========================================================

def clean_command(command):

    if not command:

        return ""

    command = command.lower().strip()

    fixes = {

        "face book": "facebook",
        "you tube": "youtube",
        "insta": "instagram",

        "open insta": "open instagram",
        "open fb": "open facebook",
        "open you tube": "open youtube",

        "meta trader": "mt5",
        "meta trader five": "mt5",

        "x au usd": "xauusd",
        "btc usd": "btcusd",

        "bye gold": "buy gold",
        "by gold": "buy gold",

        "bye bitcoin": "buy bitcoin",
        "by bitcoin": "buy bitcoin"

    }

    return fixes.get(command, command)


# ==========================================================
# EXIT SYSTEM
# ==========================================================

EXIT_COMMANDS = [

    "exit",
    "quit",
    "goodbye",
    "shutdown",
    "shutdown nitron",
    "stop nitron"

]


def should_exit(command):

    return command in EXIT_COMMANDS


# ==========================================================
# APP COMMAND SYSTEM
# Keeps your old app opening working
# ==========================================================

def handle_apps(command):

    try:

        result = execute(command)

        if result:

            return result

    except Exception as error:

        print("App system error:", error)

    return None


# ==========================================================
# PLUGIN SYSTEM
# ==========================================================

def handle_plugins(command):

    if not plugin_manager:

        return None

    try:

        result = plugin_manager.execute(command)

        if result:

            return result

    except Exception as error:

        print("Plugin error:", error)

    return None


# ==========================================================
# ROUTER SYSTEM
# ==========================================================

def handle_router(command):

    if not router:

        return None

    try:

        result = router.route(command)

        if result:

            return result

    except Exception as error:

        print("Router error:", error)

    return None


# ==========================================================
# AI BRAIN
# ==========================================================

def handle_brain(command):

    try:

        result = think(command)

        if result:

            return result

    except Exception as error:

        print("Brain error:", error)

    return None# ==========================================================
# ACADEMY SYSTEM
# ==========================================================

def handle_academy(command):

    if not command.startswith("teach me"):

        return None

    topic = command.replace(
        "teach me",
        "",
        1
    ).strip()


    if not topic:

        return "Tell me what you want to learn."


    try:

        return teach(topic)

    except Exception as error:

        return f"Academy error: {error}"


# ==========================================================
# TRADING SYSTEM
# ==========================================================

def handle_trading(command):

    if not advise:

        return None


    trading_words = [

        "analyze",
        "trade",
        "buy",
        "sell"

    ]


    if not any(word in command for word in trading_words):

        return None


    try:

        result = advise(command)

        return result


    except Exception as error:

        return f"Trading error: {error}"


# ==========================================================
# DEVELOPER BUILDER SYSTEM
# ==========================================================

def handle_builder(command):

    if not builder:

        return None


    try:

        if command.startswith("create python project"):

            name = command.replace(
                "create python project",
                "",
                1
            ).strip()

            if not name:

                name = "python_project"


            return builder.projects.create_python_project(name)



        if command.startswith("create website"):

            name = command.replace(
                "create website",
                "",
                1
            ).strip()

            if not name:

                name = "website"


            return builder.projects.create_website(name)



        if command.startswith("create flask app"):

            name = command.replace(
                "create flask app",
                "",
                1
            ).strip()

            if not name:

                name = "flask_app"


            return builder.projects.create_flask(name)



        if command.startswith("create fastapi app"):

            name = command.replace(
                "create fastapi app",
                "",
                1
            ).strip()

            if not name:

                name = "fastapi_app"


            return builder.projects.create_fastapi(name)


    except Exception as error:

        return f"Builder error: {error}"


    return None


# ==========================================================
# MEMORY SYSTEM
# ==========================================================

def remember_command(command):

    if not memory:

        return


    try:

        memory.remember(
            "last_command",
            command
        )

    except Exception:

        pass# ==========================================================
# NITRON GENERATOR SYSTEM
# ==========================================================

def handle_generator(command):

    if not nitron:

        return None


    try:

        # ------------------------------------------
        # IMAGE GENERATION
        # ------------------------------------------

        if command.startswith("generate image"):

            prompt = command.replace(
                "generate image",
                "",
                1
            ).strip()


            if not prompt:

                prompt = "futuristic robot"


            return nitron.generate_image(prompt)


        # ------------------------------------------
        # CODE GENERATION
        # ------------------------------------------

        if command.startswith("generate code"):

            prompt = command.replace(
                "generate code",
                "",
                1
            ).strip()


            return nitron.generate_code(prompt)



        # ------------------------------------------
        # GAME GENERATION
        # ------------------------------------------

        if command.startswith("create game"):

            name = command.replace(
                "create game",
                "",
                1
            ).strip()


            if not name:

                name = "new_game"


            return nitron.create_game(name)



        # ------------------------------------------
        # WEBSITE GENERATION
        # ------------------------------------------

        if command.startswith("create website"):

            name = command.replace(
                "create website",
                "",
                1
            ).strip()


            if not name:

                name = "website"


            return nitron.create_website(name)



        # ------------------------------------------
        # CHATBOT GENERATION
        # ------------------------------------------

        if command.startswith("create chatbot"):

            name = command.replace(
                "create chatbot",
                "",
                1
            ).strip()


            if not name:

                name = "chatbot"


            return nitron.create_chatbot(name)



        # ------------------------------------------
        # API GENERATION
        # ------------------------------------------

        if command.startswith("create api"):

            name = command.replace(
                "create api",
                "",
                1
            ).strip()


            if not name:

                name = "api"


            return nitron.create_api(name)


    except Exception as error:

        return f"Generator error: {error}"


    return None


# ==========================================================
# TASK SYSTEM
# ==========================================================

def handle_tasks(command):

    if not tasks:

        return None


    try:

        if command.startswith("add task"):

            task = command.replace(
                "add task",
                "",
                1
            ).strip()


            return tasks.add(
                "general",
                task
            )


        if command == "next task":

            return tasks.next()


    except Exception as error:

        return f"Task error: {error}"


    return None


# ==========================================================
# WORKFLOW SYSTEM
# ==========================================================

def handle_workflow(command):

    if not workflow:

        return None


    if command.startswith("run workflow"):

        name = command.replace(
            "run workflow",
            "",
            1
        ).strip()


        try:

            return workflow.run(name)

        except Exception as error:

            return f"Workflow error: {error}"


    return None# ==========================================================
# AUTOMATION SYSTEM
# ==========================================================

def handle_automation(command):

    if not automation:

        return None


    try:

        if command.startswith("automate game"):

            name = command.replace(
                "automate game",
                "",
                1
            ).strip()


            if not name:

                name = "game"


            return automation.create_game(name)


        if command.startswith("automate website"):

            name = command.replace(
                "automate website",
                "",
                1
            ).strip()


            if not name:

                name = "website"


            return automation.create_website(name)


    except Exception as error:

        return f"Automation error: {error}"


    return None



# ==========================================================
# JOB SYSTEM
# ==========================================================

def handle_jobs(command):

    if not jobs:

        return None


    try:

        if command.startswith("create job"):

            parts = command.replace(
                "create job",
                "",
                1
            ).strip().split()


            if len(parts) >= 2:

                job_type = parts[0]

                prompt = " ".join(parts[1:])

            else:

                job_type = "general"

                prompt = "task"


            job = jobs.create(
                job_type,
                prompt
            )


            jobs.start(job)


            jobs.finish(
                job,
                "completed"
            )


            return jobs.get(job)


    except Exception as error:

        return f"Job error: {error}"


    return None



# ==========================================================
# COMMAND PIPELINE
# ==========================================================

def process_command(command):


    # 1. Phone apps first
    response = handle_apps(command)

    if response:

        return response



    # 2. Plugins

    response = handle_plugins(command)

    if response:

        return response



    # 3. Router

    response = handle_router(command)

    if response:

        return response



    # 4. Academy

    response = handle_academy(command)

    if response:

        return response



    # 5. Trading

    response = handle_trading(command)

    if response:

        return response



    # 6. Builder

    response = handle_builder(command)

    if response:

        return response



    # 7. Generators

    response = handle_generator(command)

    if response:

        return response



    # 8. Tasks

    response = handle_tasks(command)

    if response:

        return response



    # 9. Workflows

    response = handle_workflow(command)

    if response:

        return response



    # 10. Automation

    response = handle_automation(command)

    if response:

        return response



    # 11. Jobs

    response = handle_jobs(command)

    if response:

        return response



    # 12. AI Brain

    response = handle_brain(command)

    if response:

        return response



    return "Sorry Boss, I don't know that command yet."# ==========================================================
# VOICE COMMAND LOOP
# ==========================================================

def run():

    startup()


    while True:

        try:

            banner("LISTENING")


            command = listen()


            if not command:

                time.sleep(1)

                continue



            command = clean_command(command)


            print()

            print("You:", command)

            print()



            # ------------------------------------------
            # EXIT
            # ------------------------------------------

            if should_exit(command):

                speak(
                    "Goodbye Boss. Nitron shutting down."
                )

                print(
                    "Nitron stopped."
                )

                break



            # ------------------------------------------
            # SAVE MEMORY
            # ------------------------------------------

            remember_command(command)



            # ------------------------------------------
            # PROCESS COMMAND
            # ------------------------------------------

            response = process_command(command)



            # ------------------------------------------
            # OUTPUT
            # ------------------------------------------

            print(
                "Nitron:",
                response
            )


            if isinstance(response, dict):

                if "result" in response:

                    speak(
                        str(response["result"])
                    )

                elif "status" in response:

                    speak(
                        str(response["status"])
                    )

                else:

                    speak(
                        "Task completed."
                    )

            else:

                speak(
                    str(response)
                )



        except KeyboardInterrupt:


            print()

            print(
                "Nitron stopped manually."
            )


            speak(
                "Nitron shutting down."
            )


            break



        except Exception as error:


            print(
                "SYSTEM ERROR:"
            )

            print(
                error
            )


            traceback.print_exc()


            try:

                speak(
                    "I found an error."
                )

            except Exception:

                pass


            time.sleep(2)



# ==========================================================
# START PROGRAM
# ==========================================================

if __name__ == "__main__":

    run()# ==========================================================
# NITRON STATUS SYSTEM
# ==========================================================

def nitron_status():

    status = {

        "name": "Nitron",

        "version": "3.0",

        "time": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        "modules": {}

    }


    modules = {

        "Brain": think,

        "Academy": teach,

        "Builder": builder,

        "Router": router,

        "Plugin Manager": plugin_manager,

        "Memory": memory,

        "Tasks": tasks,

        "Jobs": jobs,

        "Automation": automation,

        "Workflow": workflow

    }


    for name, module in modules.items():

        status["modules"][name] = (

            "online"
            if module
            else
            "offline"

        )


    return status



# ==========================================================
# SELF TEST
# ==========================================================

def self_test():

    results = {}


    tests = {

        "Speech":

            speak,

        "Listening":

            listen,

        "Commands":

            execute,

        "Brain":

            think

    }


    for name, test in tests.items():

        try:

            if test:

                results[name] = "OK"

            else:

                results[name] = "FAILED"


        except Exception:

            results[name] = "ERROR"


    return results



# ==========================================================
# SYSTEM COMMANDS
# ==========================================================

def handle_system_commands(command):


    if command == "nitron status":

        return nitron_status()



    if command == "self test":

        return self_test()



    if command == "hello nitron":

        return "Hello Boss. I am online."



    if command == "what time is it":

        return datetime.now().strftime(
            "%H:%M:%S"
        )



    if command == "what is your name":

        return "I am Nitron AI Assistant."


    return None



# ==========================================================
# EXTEND PROCESSOR
# ==========================================================

old_process_command = process_command


def process_command(command):

    system_response = handle_system_commands(command)


    if system_response:

        return system_response


    return old_process_command(command)# ==========================================================
# STARTUP INFORMATION
# ==========================================================

def show_startup_info():

    print()
    print("=" * 60)
    print("              NITRON AI ASSISTANT")
    print("=" * 60)

    print("""
Features:

[+] Voice Assistant
[+] App Control
[+] AI Brain
[+] Python Academy
[+] Code Generation
[+] Image Generation
[+] Website Generation
[+] Game Generation
[+] API Generation
[+] Plugin System
[+] Task Manager
[+] Job Manager
[+] Automation
[+] Memory System
[+] Workflow System
[+] Trading Tools

""")

    print(
        "System ready."
    )

    print(
        "=" * 60
    )



# ==========================================================
# SAFE STARTUP WRAPPER
# ==========================================================

def start_nitron():

    try:

        show_startup_info()

        run()


    except Exception as error:

        print(
            "Critical Nitron error:"
        )

        print(
            error
        )

        traceback.print_exc()


        try:

            speak(
                "Nitron failed to start."
            )

        except Exception:

            pass



# ==========================================================
# PROGRAM ENTRY
# ==========================================================

if __name__ == "__main__":

    start_nitron()
