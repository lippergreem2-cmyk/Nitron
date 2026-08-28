import json
import os

CPP_FILE = os.path.expanduser("~/Nitron/academy/cpp.json")


def load_cpp():
    if not os.path.exists(CPP_FILE):
        return {}
    with open(CPP_FILE, "r") as f:
        return json.load(f)


def ask_cpp(topic):
    cpp = load_cpp()

    topic = topic.lower().strip()

    if topic == "topics":
        return "\n".join(sorted(cpp.keys()))

    if topic in cpp:
        return cpp[topic].get("definition", "Topic found.")

    return "C++ topic not found."
