from wakeword.wakeword import WakeWordDetector
from listener.listener import CommandListener
from speech.speaker import Speaker

from commands import execute


wake = WakeWordDetector()
listener = CommandListener()
speaker = Speaker()


def start():

    speaker.speak("Nitron voice mode activated.")

    while True:

        wake.wait_for_wakeword()

        speaker.wake_up()

        command = listener.get_command()

        if command == "":
            speaker.error()
            continue

        response = execute(command)

        if response:
            speaker.speak(response)


if __name__ == "__main__":
    start()
