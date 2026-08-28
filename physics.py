import json
import os

PHYSICS_FILE = "physics.json"


def load_physics():
    if not os.path.exists(PHYSICS_FILE):
        return {}

    try:
        with open(PHYSICS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    except json.JSONDecodeError as e:
        print(f"[Physics Error] Invalid JSON at line {e.lineno}, column {e.colno}")
        return {}

    except Exception as e:
        print(f"[Physics Error] {e}")
        return {}


def normalize(text):
    text = text.lower().strip()

    replacements = {
        "1": "i",
        "2": "ii",
        "3": "iii",
        "4": "iv"
    }

    words = text.split()

    words = [replacements.get(word, word) for word in words]

    return " ".join(words)


def ask_physics(topic):

    physics = load_physics()

    if not physics:
        return "Physics database could not be loaded."

    topic = normalize(topic)

    if topic not in physics:

        for key in physics:
            if topic in normalize(key):
                topic = key
                break
        else:
            return "Topic not found."

    lesson = physics[topic]

    reply = []

    reply.append(f"TOPIC: {topic.title()}")
    reply.append("")

    if "definition" in lesson:
        reply.append("Definition:")
        reply.append(lesson["definition"])
        reply.append("")

    if lesson.get("notes"):
        reply.append("Notes:")
        for note in lesson["notes"]:
            reply.append(f"- {note}")
        reply.append("")

    if lesson.get("formulae"):
        reply.append("Formulae:")
        for formula in lesson["formulae"]:
            reply.append(f"- {formula}")
        reply.append("")

    if lesson.get("si_units"):
        reply.append("SI Units:")
        for k, v in lesson["si_units"].items():
            reply.append(f"- {k}: {v}")
        reply.append("")

    if lesson.get("worked_examples"):
        reply.append("Worked Examples:")
        for example in lesson["worked_examples"]:
            reply.append(f"Q: {example['question']}")
            reply.append(f"A: {example['solution']}")
            reply.append("")
        reply.append("")

    if lesson.get("practice_questions"):
        reply.append("Practice Questions:")
        for q in lesson["practice_questions"]:
            reply.append(f"- {q}")
        reply.append("")

    if lesson.get("answers"):
        reply.append("Answers:")
        for ans in lesson["answers"]:
            reply.append(f"- {ans}")

    return "\n".join(reply)
