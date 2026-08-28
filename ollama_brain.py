import subprocess


MODEL = "qwen2.5-coder:1.5b"


def ask_qwen(prompt):
    try:
        result = subprocess.run(
            ["ollama", "run", MODEL, prompt],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode != 0:
            return "Sorry, I couldn't connect to my AI brain."

        response = result.stdout.strip()

        if not response:
            return "I didn't get a response."

        return response

    except subprocess.TimeoutExpired:
        return "My AI response took too long."

    except Exception as e:
        return f"AI brain error: {e}"


if __name__ == "__main__":
    print("NITRON QWEN BRAIN TEST")
    print("-" * 40)

    while True:
        prompt = input("You: ").strip()

        if prompt.lower() in ["exit", "quit", "bye"]:
            break

        print("Nitron:", ask_qwen(prompt))
