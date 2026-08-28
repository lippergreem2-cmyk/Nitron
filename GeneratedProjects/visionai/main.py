from model import AIModel

ai = AIModel()

print("Nitron AI Started")

while True:

    text = input("You: ")

    if text.lower() == "exit":
        break

    print("AI:", ai.chat(text))
