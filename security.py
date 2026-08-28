import re


class Security:

    def __init__(self):

        self.blocked = {

            "rm -rf /",

            "mkfs",

            "dd",

            "shutdown",

            "reboot",

            "poweroff",

            "halt",

            ":(){:|:&};:",

            "chmod 777 /",

            "wipe",

            "format"

        }

        self.blocked_patterns = [

            r"rm\s+-rf\s+/",

            r"mkfs",

            r"dd\s+if=",

            r"shutdown",

            r"reboot",

            r"poweroff",

            r"halt",

            r":\(\)\{:\|:\&\};:",

            r"chmod\s+777\s+/",

            r"sudo\s+rm"

        ]

    def allowed(self, command):

        command = command.strip().lower()

        if command in self.blocked:

            return False

        for pattern in self.blocked_patterns:

            if re.search(pattern, command):

                return False

        return True

    def add_block(self, command):

        self.blocked.add(command.lower())

    def remove_block(self, command):

        self.blocked.discard(command.lower())

    def list_blocked(self):

        return sorted(self.blocked)

    def is_dangerous(self, command):

        return not self.allowed(command)

    def check(self, command):

        if self.allowed(command):

            return {

                "safe": True,

                "message": "Command allowed."

            }

        return {

            "safe": False,

            "message": "Dangerous command blocked."

        }

    def reset(self):

        self.__init__()
