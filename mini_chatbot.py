"""
mini_chatbot.py
A rule-based chatbot using regex pattern matching -- no API, no external
libraries, pure Python logic.
"""

import re
import random


class MiniChatbot:
    def __init__(self):
        self.user_name = None
        self.rules = [
            (r"hi|hello|hey", ["Hi there! \U0001F44B", "Hello! How are you?", "Hey! What's up?"]),
            (r"how are you|how're you", ["I'm just a bot, but I'm doing great!", "Running smoothly, thanks for asking!"]),
            (r"what is your name|who are you", ["I'm your Mini Chatbot!", "I'm just a simple Python bot."]),
            (r"my name is (\w+)", None),   # handled specially below
            (r"what is my name|who am i", None),  # handled specially below
            (r"who created you|who made you", ["I was built with pure Python logic, no APIs!"]),
            (r"thank you|thanks", ["You're welcome!", "No problem!", "Anytime!"]),
            (r"joke", ["Why don't programmers like nature? It has too many bugs!",
                        "Why do Java developers wear glasses? Because they don't see sharp!"]),
            (r"bye|exit|quit", ["Goodbye! Take care.", "See you later!"]),
        ]

    def save_name(self, match):
        self.user_name = match.group(1)
        return f"Nice to meet you, {self.user_name}! I'll remember that."

    def remember_name(self):
        if self.user_name:
            return f"Your name is {self.user_name}!"
        return "I don't know your name yet -- tell me by saying 'my name is ...'"

    def get_response(self, message):
        message = message.lower().strip()

        name_match = re.search(r"my name is (\w+)", message)
        if name_match:
            return self.save_name(name_match)

        if re.search(r"what is my name|who am i", message):
            return self.remember_name()

        for pattern, responses in self.rules:
            if responses is None:
                continue
            if re.search(pattern, message):
                return random.choice(responses)

        return "I don't quite understand that yet -- try asking something else!"

    def chat(self):
        print("Mini Chatbot (Type 'bye' to exit)")
        while True:
            user_input = input("You: ")
            if re.search(r"bye|exit|quit", user_input.lower()):
                print("Bot: Goodbye! Take care. \U0001F44B")
                break
            response = self.get_response(user_input)
            print(f"Bot: {response}")


if __name__ == "__main__":
    bot = MiniChatbot()
    bot.chat()
