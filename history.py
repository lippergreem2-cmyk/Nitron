import json
import os
from datetime import datetime

HISTORY_FILE = "terminal_history.json"


class History:

    def __init__(self):

        self.commands = []

        self.load()

    def add(self, command):

        self.commands.append({

            "command": command,

            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        })

        self.save()

    def save(self):

        try:

            with open(HISTORY_FILE, "w") as file:

                json.dump(

                    self.commands,

                    file,

                    indent=4

                )

        except Exception:

            pass

    def load(self):

        if not os.path.exists(HISTORY_FILE):

            self.commands = []

            return

        try:

            with open(HISTORY_FILE, "r") as file:

                self.commands = json.load(file)

        except Exception:

            self.commands = []

    def show(self):

        if not self.commands:

            print("No command history.")

            return

        print()

        print("========== COMMAND HISTORY ==========")

        for index, item in enumerate(self.commands, start=1):

            print(

                f"{index}. [{item['time']}] {item['command']}"

            )

        print()

    def clear(self):

        self.commands = []

        self.save()

    def last(self):

        if not self.commands:

            return None

        return self.commands[-1]

    def count(self):

        return len(self.commands)

    def search(self, keyword):

        keyword = keyword.lower()

        results = []

        for item in self.commands:

            if keyword in item["command"].lower():

                results.append(item)

        return results
