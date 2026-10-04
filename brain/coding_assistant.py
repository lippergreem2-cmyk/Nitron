# ==========================================================
# NITRON CODING ASSISTANT
# Clean code + explanations + step-by-step guidance
# ==========================================================

import re


class NitronCodingAssistant:

    def __init__(self):
        self.name = "Nitron Coding Assistant"
        self.version = "1.0"

    def is_coding_request(self, text):
        q = str(text).lower()

        patterns = [
            "write code",
            "generate code",
            "create code",
            "fix my code",
            "debug",
            "debug this",
            "find the error",
            "explain this code",
            "build an app",
            "create an app",
            "make an app",
            "create a website",
            "build a website",
            "modify my code",
            "modify my project",
            "add a feature",
            "coding",
            "programming",
            "python",
            "javascript",
            "kotlin",
            "java",
            "html",
            "css",
            "android app"
        ]

        return any(p in q for p in patterns)

    def create_plan(self, request):
        return {
            "goal": request.strip(),
            "status": "planning",
            "step": 1,
            "steps": [
                "Understand the request",
                "Choose the correct technology",
                "Create or inspect the project",
                "Write clean code",
                "Check the code for errors",
                "Fix detected problems",
                "Explain what was changed",
                "Give the user the next step"
            ]
        }

    def format_response(self, explanation, code=None, next_step=None):
        result = {
            "type": "coding_response",
            "explanation": explanation
        }

        if code:
            result["code"] = code

        if next_step:
            result["next_step"] = next_step

        return result

    def generate_code(self, request, preferred=None):
        from developer.ai_provider import AIProviderManager

        prompt = coding_prompt(request)

        manager = AIProviderManager()

        return manager.generate(
            prompt,
            preferred=preferred
        )


coding_assistant = NitronCodingAssistant()


def coding_prompt(request):
    return f"""
You are Nitron, a professional coding assistant.

User request:
{request}

Your job:
1. Understand exactly what the user wants.
2. Choose the appropriate programming language and tools.
3. Write complete, working code.
4. Never give placeholder code such as "add your code here".
5. Include all required imports.
6. Keep the code clean and readable.
7. Check the logic for obvious errors before returning it.
8. If the request involves multiple files, clearly separate every file.
9. Explain briefly how to run it.
10. If the task requires the user to perform steps, give ONE step at a time.

Return:
- What you built
- Complete code
- How to run it
- The next step when another action is required
"""
