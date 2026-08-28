from speech import speak


WAKE_WORDS = [
    "hey jarvis",
    "jarvis",
    "hello jarvis"
]


def detect(command):
    if not command:
        return False

    command = command.lower().strip()

    for wake in WAKE_WORDS:
        if wake in command:
            speak("Yes Boss?")
            return True

    return False
