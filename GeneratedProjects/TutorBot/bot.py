class TutorBot:

    def __init__(self):

        self.name = "TutorBot"

    def reply(self, message):

        message = message.lower()

        if "hello" in message:
            return "Hello!"

        if "how are you" in message:
            return "I'm doing great."

        return "I am still learning."


bot = TutorBot()

while True:

    text = input("You: ")

    if text.lower() in ["exit", "quit"]:

        break

    print(bot.reply(text))
