from chatbot import ChatBot


bot = ChatBot()


print("Chatbot started.")
print("Type 'exit' to quit.")


while True:

    message = input("You: ")

    if message.lower() == "exit":
        break

    print("Bot:", bot.reply(message))
