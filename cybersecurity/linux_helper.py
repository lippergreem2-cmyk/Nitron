# linux_helper.py

COMMANDS = {

    "ls": {
        "description": "Lists files and folders.",
        "syntax": "ls",
        "example": "ls -la"
    },

    "pwd": {
        "description": "Shows the current working directory.",
        "syntax": "pwd",
        "example": "pwd"
    },

    "cd": {
        "description": "Changes the current directory.",
        "syntax": "cd <directory>",
        "example": "cd ~/Nitron"
    },

    "mkdir": {
        "description": "Creates a new directory.",
        "syntax": "mkdir <folder>",
        "example": "mkdir projects"
    },

    "rm": {
        "description": "Deletes files or folders.",
        "syntax": "rm <file>",
        "example": "rm test.txt"
    },

    "cp": {
        "description": "Copies files.",
        "syntax": "cp source destination",
        "example": "cp file.txt backup.txt"
    },

    "mv": {
        "description": "Moves or renames files.",
        "syntax": "mv source destination",
        "example": "mv old.txt new.txt"
    },

    "cat": {
        "description": "Displays file contents.",
        "syntax": "cat <file>",
        "example": "cat config.py"
    },

    "grep": {
        "description": "Searches for text in files.",
        "syntax": "grep word file",
        "example": "grep python notes.txt"
    },

    "find": {
        "description": "Finds files and folders.",
        "syntax": "find <path> -name filename",
        "example": "find . -name config.py"
    },

    "chmod": {
        "description": "Changes file permissions.",
        "syntax": "chmod permissions file",
        "example": "chmod +x script.sh"
    },

    "python": {
        "description": "Runs Python programs.",
        "syntax": "python file.py",
        "example": "python trade_advisor.py"
    }

}


def explain_command(command):

    command = command.strip().split()[0]

    if command in COMMANDS:

        data = COMMANDS[command]

        return f"""
============================
Linux Command
============================
Command     : {command}

Description : {data['description']}

Syntax      : {data['syntax']}

Example     : {data['example']}
============================
"""

    return "Unknown Linux command."


if __name__ == "__main__":

    while True:

        cmd = input("Linux> ")

        if cmd.lower() == "exit":
            break

        print(explain_command(cmd))
