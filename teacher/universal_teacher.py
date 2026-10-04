"""
Nitron Universal Teacher Engine
The teaching layer sits above the AI model and makes Nitron behave like a tutor.
"""

SYSTEM_PROMPT = """
You are Nitron, a universal AI assistant and teacher.

Your job is to help the user understand things, not merely provide answers.

Teaching rules:
1. Identify what the user is trying to learn or accomplish.
2. Explain concepts clearly at an appropriate level.
3. Break difficult subjects into smaller steps.
4. Use examples when useful.
5. When solving academic problems, show the reasoning clearly.
6. Check for misunderstandings and correct them respectfully.
7. Give short practice questions when learning would benefit from practice.
8. Adapt difficulty based on the user's responses.
9. Never pretend to know something you do not know.
10. For current information, use an appropriate online source/tool when available.
11. Be concise when the user wants a quick answer and detailed when they want a lesson.
12. Support mathematics, science, languages, programming, history, geography,
    cybersecurity, business, arts, and general knowledge.

Nitron should feel like one consistent assistant, not a collection of unrelated bots.
"""

def build_teacher_prompt(user_message: str, context: str = "") -> str:
    parts = [SYSTEM_PROMPT]

    if context:
        parts.append(
            "\nRelevant conversation/learning context:\n" + context
        )

    parts.append(
        "\nUser request:\n" + user_message
    )

    return "\n".join(parts)


def classify_learning_request(message: str) -> dict:
    text = message.lower()

    subjects = {
        "mathematics": [
            "math", "algebra", "geometry", "equation", "calculus",
            "fraction", "percentage", "probability"
        ],
        "science": [
            "physics", "chemistry", "biology", "science",
            "atom", "force", "energy", "cell"
        ],
        "programming": [
            "python", "kotlin", "java", "javascript", "code",
            "programming", "algorithm", "program"
        ],
        "cybersecurity": [
            "cybersecurity", "cyber security", "security",
            "network security", "ethical hacking"
        ],
        "languages": [
            "english", "swahili", "grammar", "translate",
            "language", "vocabulary"
        ],
        "history": [
            "history", "historical", "war", "civilization"
        ],
        "geography": [
            "geography", "country", "continent", "capital",
            "climate", "map"
        ],
    }

    detected = []

    for subject, keywords in subjects.items():
        if any(keyword in text for keyword in keywords):
            detected.append(subject)

    return {
        "is_learning_request": bool(detected),
        "subjects": detected,
    }


if __name__ == "__main__":
    import sys

    message = " ".join(sys.argv[1:]).strip()

    if not message:
        print("Usage: python teacher/universal_teacher.py \"your question\"")
        raise SystemExit(1)

    result = classify_learning_request(message)

    print("Nitron Universal Teacher")
    print("========================")
    print("Learning request:", result["is_learning_request"])
    print("Subjects:", ", ".join(result["subjects"]) or "general")
    print()
    print(build_teacher_prompt(message))
