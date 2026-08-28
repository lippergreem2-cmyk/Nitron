import speech_recognition as sr


class CommandListener:

    def __init__(self):

        self.recognizer = sr.Recognizer()

    def listen(self):

        with sr.Microphone() as source:

            print("Waiting for your command...")

            self.recognizer.adjust_for_ambient_noise(source)

            audio = self.recognizer.listen(source)

        try:

            command = self.recognizer.recognize_google(audio)

            print("Command:", command)

            return command

        except sr.UnknownValueError:

            return ""

        except sr.RequestError:

            return ""

        except Exception:

            return ""

    def get_command(self):

        while True:

            command = self.listen()

            if command != "":

                return command
