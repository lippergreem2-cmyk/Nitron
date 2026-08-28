import os
import subprocess
import datetime
import shutil
import json


class TerminalAssistant:

    def __init__(self):

        self.current_directory = os.getcwd()

        self.history = []

        self.aliases = {}

        self.variables = {}

        self.running = False

        self.load_aliases()

    # =====================================
    # START
    # =====================================

    def banner(self):

        print("=" * 60)
        print("            NITRON TERMINAL")
        print("=" * 60)
        print("Current Directory :", self.current_directory)
        print("Type 'help' for commands.")
        print("Type 'exit' to quit.")
        print("=" * 60)

    def run(self):

        self.running = True

        self.banner()

        while self.running:

            try:

                command = input("Nitron> ").strip()

                if not command:

                    continue

                self.history.append(command)

                self.execute(command)

            except KeyboardInterrupt:

                print()

                print("Interrupted.")

            except EOFError:

                print()

                break

    # =====================================
    # EXECUTION
    # =====================================

    def execute(self, command):

        command = command.strip()

        if command.lower() in ["exit", "quit"]:

            self.running = False

            print("Leaving Terminal.")

            return

        if command == "help":

            self.help()

            return

        if command == "pwd":

            print(self.current_directory)

            return

        if command == "ls":

            self.list_directory()

            return

        if command.startswith("cd "):

            self.change_directory(command[3:])

            return

        if command == "history":

            self.show_history()

            return

        if command == "clear history":

            self.history.clear()

            print("History cleared.")

            return

        if command == "clear":

            os.system("clear")

            return

        if command.startswith("mkdir "):

            self.make_directory(command[6:])

            return

        if command.startswith("touch "):

            self.touch(command[6:])

            return

        if command.startswith("cat "):

            self.cat(command[4:])

            return

        if command.startswith("rm "):

            self.remove(command[3:])

            return

        if command.startswith("cp "):

            self.copy(command)

            return

        if command.startswith("mv "):

            self.move(command)

            return

        if command == "time":

            print(datetime.datetime.now())

            return

        if command == "date":

            print(datetime.date.today())

            return

        if command == "python version":

            print(subprocess.getoutput("python --version"))

            return

        self.shell(command)

    # =====================================
    # FILESYSTEM
    # =====================================

    def list_directory(self):

        try:

            for item in sorted(os.listdir(self.current_directory)):

                print(item)

        except Exception as e:

            print(e)

    def change_directory(self, folder):

        try:

            os.chdir(folder)

            self.current_directory = os.getcwd()

            print(self.current_directory)

        except Exception as e:

            print(e)

    def make_directory(self, folder):

        try:

            os.mkdir(folder)

            print("Folder created.")

        except Exception as e:

            print(e)

    def touch(self, filename):

        try:

            open(filename, "a").close()

            print("File created.")

        except Exception as e:

            print(e)

    def cat(self, filename):

        try:

            with open(filename, "r") as file:

                print(file.read())

        except Exception as e:

            print(e)

    def remove(self, filename):

        try:

            os.remove(filename)

            print("Deleted.")

        except Exception as e:

            print(e)

    def copy(self, command):

        try:

            args = command.split(maxsplit=2)

            shutil.copy(args[1], args[2])

            print("Copied.")

        except Exception as e:

            print(e)

    def move(self, command):

        try:

            args = command.split(maxsplit=2)

            shutil.move(args[1], args[2])

            print("Moved.")

        except Exception as e:

            print(e)    # =====================================
    # HISTORY
    # =====================================

    def show_history(self):

        if not self.history:

            print("History is empty.")

            return

        print()

        for number, command in enumerate(self.history, start=1):

            print(f"{number}. {command}")

    def save_history(self):

        try:

            with open("terminal_history.json", "w") as file:

                json.dump(self.history, file, indent=4)

        except Exception:

            pass

    def load_history(self):

        if not os.path.exists("terminal_history.json"):

            return

        try:

            with open("terminal_history.json", "r") as file:

                self.history = json.load(file)

        except Exception:

            self.history = []

    # =====================================
    # ALIASES
    # =====================================

    def load_aliases(self):

        if not os.path.exists("aliases.json"):

            self.aliases = {}

            return

        try:

            with open("aliases.json", "r") as file:

                self.aliases = json.load(file)

        except Exception:

            self.aliases = {}

    def save_aliases(self):

        try:

            with open("aliases.json", "w") as file:

                json.dump(self.aliases, file, indent=4)

        except Exception:

            pass

    def add_alias(self, name, command):

        self.aliases[name] = command

        self.save_aliases()

        print("Alias added.")

    def remove_alias(self, name):

        if name in self.aliases:

            del self.aliases[name]

            self.save_aliases()

            print("Alias removed.")

    def list_aliases(self):

        if not self.aliases:

            print("No aliases.")

            return

        print()

        for name, command in self.aliases.items():

            print(f"{name} -> {command}")

    # =====================================
    # SHELL
    # =====================================

    def shell(self, command):

        if command in self.aliases:

            command = self.aliases[command]

        try:

            result = subprocess.run(

                command,

                shell=True,

                cwd=self.current_directory,

                capture_output=True,

                text=True

            )

            if result.stdout:

                print(result.stdout)

            if result.stderr:

                print(result.stderr)

        except Exception as error:

            print(error)    # =====================================
    # FILE SEARCH
    # =====================================

    def find_file(self, name):

        found = False

        for root, dirs, files in os.walk(self.current_directory):

            for file in files:

                if name.lower() in file.lower():

                    print(os.path.join(root, file))

                    found = True

        if not found:

            print("No matching file found.")

    # =====================================
    # TREE VIEW
    # =====================================

    def tree(self, directory=None, level=0):

        if directory is None:

            directory = self.current_directory

        try:

            items = sorted(os.listdir(directory))

        except Exception as e:

            print(e)

            return

        for item in items:

            path = os.path.join(directory, item)

            print("│   " * level + "├── " + item)

            if os.path.isdir(path):

                self.tree(path, level + 1)

    # =====================================
    # DISK USAGE
    # =====================================

    def disk_usage(self):

        try:

            total, used, free = shutil.disk_usage(self.current_directory)

            print(f"Total : {total // (1024**3)} GB")

            print(f"Used  : {used // (1024**3)} GB")

            print(f"Free  : {free // (1024**3)} GB")

        except Exception as e:

            print(e)

    # =====================================
    # FILE INFORMATION
    # =====================================

    def file_info(self, filename):

        try:

            size = os.path.getsize(filename)

            modified = datetime.datetime.fromtimestamp(

                os.path.getmtime(filename)

            )

            print("Name :", os.path.basename(filename))

            print("Path :", os.path.abspath(filename))

            print("Size :", size, "bytes")

            print("Modified :", modified)

        except Exception as e:

            print(e)

    # =====================================
    # PROCESS MANAGER
    # =====================================

    def processes(self):

        print(subprocess.getoutput("ps"))

    def kill(self, pid):

        try:

            os.kill(int(pid), 9)

            print("Process terminated.")

        except Exception as e:

            print(e)

    # =====================================
    # SYSTEM INFORMATION
    # =====================================

    def system_info(self):

        print("Current Directory :", self.current_directory)

        print("Operating System  :", os.name)

        print("Platform          :", subprocess.getoutput("uname -a"))

        print("Python            :", subprocess.getoutput("python --version"))

        print("User              :", subprocess.getoutput("whoami"))

        print("Date              :", datetime.datetime.now())    # =====================================
    # ZIP FILES
    # =====================================

    def zip_folder(self, folder, archive):

        try:

            shutil.make_archive(archive, "zip", folder)

            print("Archive created.")

        except Exception as e:

            print(e)

    def unzip(self, archive, destination="."):

        try:

            shutil.unpack_archive(archive, destination)

            print("Archive extracted.")

        except Exception as e:

            print(e)

    # =====================================
    # ENVIRONMENT VARIABLES
    # =====================================

    def set_variable(self, key, value):

        self.variables[key] = value

        print(f"{key} = {value}")

    def get_variable(self, key):

        if key in self.variables:

            print(self.variables[key])

        else:

            print("Variable not found.")

    def list_variables(self):

        if not self.variables:

            print("No variables defined.")

            return

        print()

        for key, value in self.variables.items():

            print(f"{key} = {value}")

    # =====================================
    # GIT
    # =====================================

    def git_status(self):

        print(subprocess.getoutput("git status"))

    def git_branch(self):

        print(subprocess.getoutput("git branch"))

    def git_log(self):

        print(subprocess.getoutput("git log --oneline"))

    def git_pull(self):

        print(subprocess.getoutput("git pull"))

    # =====================================
    # ANDROID UTILITIES
    # =====================================

    def battery(self):

        print(subprocess.getoutput("termux-battery-status"))

    def wifi(self):

        print(subprocess.getoutput("termux-wifi-connectioninfo"))

    def location(self):

        print(subprocess.getoutput("termux-location"))

    def clipboard(self):

        print(subprocess.getoutput("termux-clipboard-get"))

    def speak(self, text):

        subprocess.run(

            [

                "termux-tts-speak",

                text

            ]

        )

    # =====================================
    # TERMINAL SUMMARY
    # =====================================

    def about(self):

        print("=" * 60)

        print("Nitron Terminal Assistant")

        print("Version : 1.0")

        print("Features")

        print("- File Manager")

        print("- Command History")

        print("- Process Manager")

        print("- Git Tools")

        print("- ZIP Manager")

        print("- Android Utilities")

        print("- Variables")

        print("- Shell Execution")

        print("=" * 60)    # =====================================
    # PLUGIN MANAGER
    # =====================================

    def load_plugins(self):

        self.plugins = {}

        plugin_folder = "plugins"

        if not os.path.exists(plugin_folder):

            os.mkdir(plugin_folder)

            return

        for filename in os.listdir(plugin_folder):

            if not filename.endswith(".py"):

                continue

            name = filename[:-3]

            self.plugins[name] = os.path.join(
                plugin_folder,
                filename
            )

    def list_plugins(self):

        if not hasattr(self, "plugins"):

            self.load_plugins()

        if not self.plugins:

            print("No plugins installed.")

            return

        print()

        print("Installed Plugins")

        print("-----------------")

        for plugin in sorted(self.plugins):

            print(plugin)

    # =====================================
    # LOGGING
    # =====================================

    def log(self, message):

        try:

            with open("terminal.log", "a") as file:

                file.write(

                    f"[{datetime.datetime.now()}] {message}\n"

                )

        except:

            pass

    def show_log(self):

        try:

            with open("terminal.log", "r") as file:

                print(file.read())

        except:

            print("No log file found.")

    def clear_log(self):

        open("terminal.log", "w").close()

        print("Log cleared.")

    # =====================================
    # AUTOCOMPLETE
    # =====================================

    def suggestions(self, text):

        commands = [

            "help",

            "pwd",

            "ls",

            "cd",

            "mkdir",

            "touch",

            "cat",

            "rm",

            "cp",

            "mv",

            "history",

            "tree",

            "find",

            "disk",

            "battery",

            "wifi",

            "location",

            "git status",

            "git pull",

            "git branch",

            "git log",

            "exit"

        ]

        matches = []

        for command in commands:

            if command.startswith(text):

                matches.append(command)

        return matches

    # =====================================
    # BACKGROUND TASKS
    # =====================================

    def add_task(self, command):

        if not hasattr(self, "tasks"):

            self.tasks = []

        self.tasks.append(command)

        print("Task added.")

    def list_tasks(self):

        if not hasattr(self, "tasks"):

            self.tasks = []

        if not self.tasks:

            print("No background tasks.")

            return

        print()

        for index, task in enumerate(self.tasks, start=1):

            print(f"{index}. {task}")

    def clear_tasks(self):

        self.tasks = []

        print("Tasks cleared.")

    # =====================================
    # STATISTICS
    # =====================================

    def stats(self):

        print()

        print("========== TERMINAL STATS ==========")

        print("Current Directory :", self.current_directory)

        print("History Entries   :", len(self.history))

        print("Aliases           :", len(self.aliases))

        print("Variables         :", len(self.variables))

        print("Plugins           :", len(getattr(self, "plugins", {})))

        print("Tasks             :", len(getattr(self, "tasks", [])))

        print("====================================")
