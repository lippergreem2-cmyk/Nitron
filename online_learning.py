import subprocess
import urllib.parse


def internet_available():

    try:

        result = subprocess.run(
            ["ping", "-c", "1", "8.8.8.8"],
            capture_output=True
        )

        return result.returncode == 0

    except:

        return False


def learn_online(topic):

    if not internet_available():

        return "No internet connection."

    answer = input(
        f"I found an internet connection.\n"
        f"Would you like me to learn about '{topic}' online? (yes/no): "
    ).strip().lower()

    if answer not in ["yes", "y"]:

        return "Using offline lessons."

    query = urllib.parse.quote(topic)

    subprocess.run([
        "am",
        "start",
        "-a",
        "android.intent.action.VIEW",
        "-d",
        f"https://www.google.com/search?q={query}"
    ])

    return f"Opening online resources for {topic}."
