# ==========================================================
# NITRON AI ASSISTANT
# Version 4.0
# main.py
# Part 1/5
# ==========================================================

import os
import time
import traceback
from datetime import datetime


# ==========================================================
# CORE MODULES
# ==========================================================

try:
    from speech import listen, speak
except Exception:

    def listen():
        return input("You: ")


    def speak(text):
        print("Nitron:", text)


try:
    from commands import execute
except Exception:

    def execute(command):
        return None


try:
    from brain import think
except Exception:

    def think(command):
        return None



# ==========================================================
# OPTIONAL MODULES
# ==========================================================

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
    from plugin_manager import plugin_manager

except Exception:

    plugin_manager = None



try:
    from command_router import router

except Exception:

    router = None



try:
    from memory_manager import memory

except Exception:

    memory = None



try:
    from task_manager import tasks

except Exception:

    tasks = None



try:
    from workflow_manager import workflow

except Exception:

    workflow = None



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
        ◇◇◇◆◆◆◇◇◇
          ◇◇◇◇◇
             ◇
""",

"""
             ◆
          ◆◆◆◆◆
        ◆◆◆◇◇◇◆◆◆
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
    print("              N I T R O N")
    print("=" * 50)
    print("Status:", status)
    print("Wake: Hey Nitron")
    print(
        "Time:",
        datetime.now().strftime("%H:%M:%S")
    )
    print("=" * 50)



# ==========================================================
# STARTUP
# ==========================================================

def startup():

    banner("STARTING")

    print("Loading Nitron modules...\n")


    modules = {

        "Brain": think,
        "Academy": teach,
        "Builder": builder,
        "Router": router,
        "Plugins": plugin_manager,
        "Memory": memory,
        "Tasks": tasks,
        "Workflow": workflow,
        "Automation": automation,
        "Jobs": jobs

    }


    for name, module in modules.items():

        if module:

            print(
                "[ OK ]",
                name
            )

        else:

            print(
                "[ -- ]",
                name
            )


    speak(
        "Nitron is online. Welcome back Boss."
    )



# ==========================================================
# COMMAND CLEANER
# ==========================================================

def clean_command(command):

    if not command:

        return ""


    command = command.lower().strip()


    fixes = {

        "insta":
        "instagram",

        "you tube":
        "youtube",

        "face book":
        "facebook",

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
# EXIT SYSTEM
# ==========================================================

EXIT_COMMANDS = [

    "exit",
    "quit",
    "goodbye",
    "shutdown",
    "stop nitron"

]


def should_exit(command):

    return command in EXIT_COMMANDS# ==========================================================
# APP SYSTEM
# ==========================================================

def handle_apps(command):

    try:

        result = execute(command)

        if result:
            return result

    except Exception as error:

        print("App error:", error)

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
# BRAIN SYSTEM
# ==========================================================

def handle_brain(command):

    try:

        result = think(command)

        if result:
            return result

    except Exception as error:

        print("Brain error:", error)

    return None



# ==========================================================
# ACADEMY SYSTEM
# ==========================================================

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

        return f"Trading error: {error}"# ==========================================================
# BUILDER SYSTEM
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


    except Exception as error:

        return f"Builder error: {error}"

    return None



# ==========================================================
# CODE AI SYSTEM
# ==========================================================

try:

    from developer.code_ai import CodeAI

    code_ai = CodeAI()

except Exception:

    code_ai = None



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

        pass



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


    return None



# ==========================================================
# AUTOMATION SYSTEM
# ==========================================================

def handle_automation(command):

    if not automation:
        return None


    try:

        if command.startswith("automate website"):

            name = command.replace(
                "automate website",
                "",
                1
            ).strip()

            return automation.create_website(name)


        if command.startswith("automate game"):

            name = command.replace(
                "automate game",
                "",
                1
            ).strip()

            return automation.create_game(name)


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

            data = command.replace(
                "create job",
                "",
                1
            ).strip().split()


            job_type = data[0] if data else "general"

            prompt = " ".join(data[1:]) if len(data) > 1 else "task"


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


    return None# ==========================================================
# COMMAND PIPELINE
# ==========================================================

def process_command(command):

    handlers = [

        handle_apps,
        handle_plugins,
        handle_router,
        handle_academy,
        handle_trading,
        handle_code_ai,
        handle_builder,
        handle_tasks,
        handle_workflow,
        handle_automation,
        handle_jobs,
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
                "error:",
                error
            )


    return "Sorry Boss, I don't know that command yet."



# ==========================================================
# VOICE LOOP
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



            if should_exit(command):

                speak(
                    "Goodbye Boss. Nitron shutting down."
                )

                break



            remember_command(command)



            response = process_command(command)


            print(
                "Nitron:",
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


            try:

                speak(
                    "I found an error."
                )

            except Exception:

                pass


            time.sleep(2)# ==========================================================
# NITRON STATUS
# ==========================================================

def nitron_status():

    return {

        "name": "Nitron",

        "version": "4.0",

        "time":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

        "modules": {

            "Brain":
                "online" if think else "offline",

            "Speech":
                "online" if listen else "offline",

            "Code AI":
                "online" if code_ai else "offline",

            "Builder":
                "online" if builder else "offline",

            "Memory":
                "online" if memory else "offline",

            "Tasks":
                "online" if tasks else "offline"

        }

    }



# ==========================================================
# SELF TEST
# ==========================================================

def self_test():

    tests = {

        "Speech": listen,

        "Voice Output": speak,

        "Commands": execute,

        "Brain": think

    }


    results = {}


    for name, module in tests.items():

        try:

            if module:

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


    if command == "what is your name":

        return "I am Nitron AI Assistant."


    if command == "time":

        return datetime.now().strftime(
            "%H:%M:%S"
        )


    return None



# ==========================================================
# ADD SYSTEM COMMANDS TO PIPELINE
# ==========================================================

old_process_command = process_command


def process_command(command):

    system = handle_system_commands(command)

    if system:

        return system


    return old_process_command(command)



# ==========================================================
# START NITRON
# ==========================================================

def start_nitron():

    try:

        run()


    except Exception as error:

        print(
            "Critical Nitron error:",
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
