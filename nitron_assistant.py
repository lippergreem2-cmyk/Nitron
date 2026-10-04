"""
nitron_assistant.py
A single chat interface for Nitron that can either talk normally, or
generate and save code when you ask it to build something.

Trigger phrases like "write a script", "build me", "create a program",
"generate code" route to code_generator.py automatically. Everything else
goes to normal chat via ai_brain.py.

Usage:
    python nitron_assistant.py
"""

from ai_brain import chat
from code_generator import generate_and_save

CODE_TRIGGERS = [
    "write a script", "write a program", "build me", "create a program",
    "generate code", "make a script", "code a", "write code for",
]


def looks_like_code_request(message: str) -> bool:
    lower = message.lower()
    return any(trigger in lower for trigger in CODE_TRIGGERS)


def handle_message(message: str, history: list) -> str:
    if looks_like_code_request(message):
        filename = input("Nitron: What should I name the file? (e.g. script.py): ").strip()
        filename = filename or "generated_script.py"
        try:
            generate_and_save(message, filename)
            return f"Done -- saved as {filename}. Want me to explain what it does?"
        except ValueError as e:
            return str(e)
    else:
        return chat(message, history)


def main():
    print("Nitron Assistant. Type 'exit' to quit.")
    history = []
    while True:
        user_input = input("You: ")
        if user_input.lower() in ("exit", "quit"):
            break
        reply = handle_message(user_input, history)
        print(f"Nitron: {reply}\n")
        history.append({"role": "user", "content": user_input})
        history.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    main()
