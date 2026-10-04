#!/usr/bin/env python3

def reply(msg):
    msg = msg.lower()
    if "hello" in msg:
        return "Hi there!"
    if "how are you" in msg:
        return "I'm just code, but I'm doing great!"
    return "I don't understand that."

def main():
    print("Xee chatbot. Type 'exit' to quit.")
    while True:
        user = input("> ")
        if user.strip().lower() == "exit":
            break
        print(reply(user))

if __name__ == "__main__":
    main()
