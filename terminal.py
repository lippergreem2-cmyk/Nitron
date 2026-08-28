import os
import subprocess

from .history import History
from .security import Security


class TerminalAssistant:

    def __init__(self):
        self.history = History()
        self.security = Security()
        self.current_directory = os.getcwd()

    def banner(self):
        print("=" * 50)
        print("      NITRON TERMINAL ASSISTANT")
        print("=" * 50)
        print("Type 'help' for commands.")
        print("Type 'exit' to quit.")
        print()

    def execute(self, command):

        command = command.strip()

        if not command:
            return

        self.history.add(command)

        if not self.security.allowed(command):
            print("Command blocked.")
            return

        if command == "help":
            self.help()
            return

        if command == "history":
            self.history.show()
            return

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
            print(error)

    def help(self):
        print("""
Commands
--------
help
history
pwd
ls
cd
mkdir
rm
cp
mv
cat
python
git
exit
""")

    def run(self):

        self.banner()

        while True:

            cmd = input("Nitron> ")

            if cmd.lower() in ["exit", "quit"]:
                break

            self.execute(cmd)
