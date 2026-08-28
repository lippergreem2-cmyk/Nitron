import json
import os

MEMORY_FILE = "memory.json"


def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}

    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)


def remember(key, value):
    memory = load_memory()

    memory[key] = value

    save_memory(memory)

    return f"I will remember that {key} is {value}."


def recall(key):
    memory = load_memory()

    if key in memory:
        return memory[key]

    return None


def forget(key):
    memory = load_memory()

    if key in memory:
        del memory[key]
        save_memory(memory)
        return f"I forgot {key}."

    return "I don't remember that."


def show_memory():
    memory = load_memory()

    if not memory:
        return "Memory is empty."

    output = "=============================\n"
    output += "      NITRON MEMORY\n"
    output += "=============================\n"

    for key, value in memory.items():
        output += f"{key} : {value}\n"

    return output


def clear_memory():
    save_memory({})
    return "Memory cleared."


if __name__ == "__main__":

    print(show_memory())
