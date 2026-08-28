# commands.py

from brain import think
from memory import remember, recall, forget, show_memory


def execute(command):

    cmd = command.strip()

    lower = cmd.lower()

    # --------------------------
    # Memory Commands
    # --------------------------

    if lower.startswith("remember "):

        text = cmd[9:]

        if "=" in text:

            key, value = text.split("=", 1)

        elif " is " in text:

            key, value = text.split(" is ", 1)

        else:

            return "Usage:\nremember name=Nitron\nor\nremember owner is Boss"

        return remember(key.strip(), value.strip())

    if lower.startswith("recall "):

        key = cmd[7:].strip()

        value = recall(key)

        if value is None:
            return "I don't remember that."

        return f"{key} = {value}"

    if lower.startswith("forget "):

        key = cmd[7:].strip()

        return forget(key)

    if lower == "memory":

        return show_memory()

    # --------------------------
    # AI Brain
    # --------------------------

    answer = think(cmd)

    if answer:
        return answer

    return "Unknown command."


if __name__ == "__main__":

    print("Nitron Command Processor")
    print("Type 'exit' to quit.")

    while True:

        command = input("Command> ")

        if command.lower() == "exit":
            break

        print(execute(command))
