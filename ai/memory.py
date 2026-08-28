import json
import os

MEMORY_FILE = os.path.expanduser("~/Nitron/data/memory.json")


def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}

    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


def save_memory(memory):
    os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)

    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)


def remember(key, value):
    memory = load_memory()
    memory[key] = value
    save_memory(memory)
    return f"I'll remember that {key} is {value}."


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

    return "I don't know that."


def show_memory():
    memory = load_memory()

    if not memory:
        return "Memory is empty."

    output = "Nitron Memory\n"
    output += "=" * 30 + "\n"

    for key, value in memory.items():
        output += f"{key}: {value}\n"

    return output


if __name__ == "__main__":

    print(remember("owner", "Boss Nimrod"))
    print(recall("owner"))
    print(show_memory())
