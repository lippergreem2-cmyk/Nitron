import re
import subprocess
import time

from wakeword.wakeword import WakeWord
from listener.listener import CommandListener
from speech.speaker import Speaker
from commands import execute


wake = WakeWord()
listener = CommandListener()
speaker = Speaker()

STOP_WORDS = ["stop", "quiet", "shut up", "be quiet", "nitron stop"]


def split_sentences(text):
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s for s in sentences if s]


def check_for_stop():
    print("[listening for stop...]")
    start_time = time.time()
    try:
        result = subprocess.check_output(
            ["termux-speech-to-text"],
            text=True,
            timeout=10
        )
        elapsed = time.time() - start_time
        heard = result.strip().lower()
        print(f"[heard after {elapsed:.1f}s]:", heard if heard else "(nothing)")
        return any(word in heard for word in STOP_WORDS)
    except subprocess.TimeoutExpired:
        elapsed = time.time() - start_time
        print(f"[stop-check timed out after {elapsed:.1f}s]")
        return False
    except Exception as e:
        print("[stop-check error]:", e)
        return False


def speak_with_interrupt_check(text):
    for sentence in split_sentences(text):
        speaker.speak(sentence)
        if check_for_stop():
            print("[Interrupted by user]")
            return


def start():

    speaker.speak("Nitron voice mode activated.")

    while True:

        wake.detected()

        speaker.wake_up()

        command = listener.get_command()

        if command == "":
            speaker.error()
            continue

        response = execute(command)

        if response:
            speak_with_interrupt_check(response)


if __name__ == "__main__":
    start()
