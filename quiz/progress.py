import json
import os

PROGRESS_FILE = "quiz_progress.json"


def load_progress():

    if not os.path.exists(PROGRESS_FILE):

        return {}

    with open(PROGRESS_FILE, "r") as f:

        return json.load(f)


def save_progress(progress):

    with open(PROGRESS_FILE, "w") as f:

        json.dump(progress, f, indent=4)


def record_score(topic, score, total):

    progress = load_progress()

    percentage = round((score / total) * 100, 1)

    progress[topic] = {

        "score": score,

        "total": total,

        "percentage": percentage

    }

    save_progress(progress)

    return percentage


def show_progress():

    progress = load_progress()

    if not progress:

        return "No quiz results recorded."

    text = "=== Mathematics Progress ===\n\n"

    for topic in sorted(progress):

        p = progress[topic]

        text += (

            f"{topic.title()}\n"

            f"Score: {p['score']}/{p['total']}\n"

            f"Percentage: {p['percentage']}%\n\n"

        )

    return text


def weak_topics():

    progress = load_progress()

    weak = []

    for topic, p in progress.items():

        if p["percentage"] < 60:

            weak.append(topic)

    return weak


def recommendation():

    weak = weak_topics()

    if not weak:

        return "Excellent! You have no weak mathematics topics."

    text = "You should revise:\n"

    for topic in weak:

        text += f"- {topic.title()}\n"

    return text
