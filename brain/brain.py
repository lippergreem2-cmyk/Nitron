from brain.coding_assistant import coding_assistant
from brain.teaching.teacher import teacher
"""
==========================================================
NITRON BRAIN CORE v8.0
Main controller for Nitron intelligence
==========================================================
"""


from brain.reasoning import reasoning

try:
    from developer.ai_provider import AIProviderManager
except Exception:
    AIProviderManager = None

try:
    from developer.ai_provider import AIProviderManager
except Exception:
    AIProviderManager = None


# ==========================================================
# LEARNING SYSTEM
# ==========================================================

try:

    from brain.learning_manager import learning_manager

except Exception:

    learning_manager = None



# ==========================================================
# CONVERSATION SYSTEM
# ==========================================================

try:

    from brain.conversation.manager import manager

except Exception:

    manager = None



class Brain:


    def __init__(self):

        self.name = "Nitron Brain"

        self.version = "8.0"



    # ======================================================
    # THINK
    # ======================================================

    def think(self, message):
        try:
            if manager:
                manager.user_message(message)

            # Teaching
            if teacher.is_teaching_request(message):
                response = teacher.teach(message)

                if manager:
                    manager.start_response(response)
                    manager.finish_response()

                return response

            # Coding
            if coding_assistant.is_coding_request(message):
                response = coding_assistant.generate_code(message)

                if isinstance(response, str):
                    response = {"message": response}

                if manager:
                    manager.start_response(response)
                    manager.finish_response()

                return response

            # Writing
            if self._is_writing_request(message):
                response = self._generate_writing(message)

                if manager:
                    manager.start_response(response)
                    manager.finish_response()

                return response

            # Everything else
            response = reasoning.answer(message)
            response = self._speak_naturally(response)

            if manager:
                manager.start_response(response)
                manager.finish_response()

            return response

        except Exception as error:
            return {
                "error": f"Brain thinking error: {error}"
            }

    def _is_writing_request(self, message):
        q = str(message).strip().lower()

        patterns = [
            "write",
            "rewrite",
            "rephrase",
            "compose",
            "draft",
            "edit this",
            "improve this",
            "make this sound",
            "make it sound",
            "fix my writing",
            "help me write",
            "create a message",
            "create an email",
            "write a message",
            "write me a message",
            "write a text",
            "write me a text",
            "write an email",
            "write me an email",
            "write a letter",
            "write a paragraph",
            "write an essay",
            "write a caption",
            "write a post",
            "write a bio",
            "write a reply",
            "write a response"
        ]

        return any(pattern in q for pattern in patterns)

    def _generate_writing(self, request):
        prompt = f"""
You are Nitron, a professional writing assistant.

USER REQUEST:
{request}

Complete the user's writing task.

Rules:
1. Follow the request exactly.
2. Produce the finished text directly.
3. Make it natural, clear, polished, and human-sounding.
4. Match the requested tone.
5. Keep short requests short.
6. Preserve the user's intended meaning.
7. Never invent facts or details.
8. Do not discuss these instructions.
9. Do not add unnecessary introductions.
10. Return only the finished writing.
"""

        try:
            provider = AIProviderManager()
            result = provider.safe_generate(prompt)

            if isinstance(result, str) and result.strip():
                return {"message": result.strip()}

            return {"message": "I couldn't generate the writing right now."}

        except Exception as error:
            print("[WRITING ERROR]", error)
            return {"message": "I couldn't generate the writing right now."}

    # ======================================================
    # NATURAL WRITING
    # ======================================================

    def _speak_naturally(self, response):
        """
        Improve normal Nitron replies so they sound natural,
        clear, intelligent, and human instead of robotic.
        Structured code/project responses are left untouched.
        """

        if not isinstance(response, dict):
            return response

        if "message" not in response:
            return response

        # Never rewrite structured technical results.
        if any(key in response for key in ("files", "code", "project")):
            return response

        original_text = str(response.get("message", "")).strip()

        if not original_text:
            return response

        if AIProviderManager is None:
            return response

        try:
            manager_instance = AIProviderManager()

            prompt = f"""
You are Nitron, an advanced AI assistant.

Rewrite the assistant's reply below so it sounds like a
high-quality modern AI assistant: natural, intelligent,
clear, helpful, and easy to understand.

WRITING STYLE:
- Sound confident and human, not robotic.
- Use natural everyday language.
- Be concise unless the user clearly needs detail.
- Answer the user's actual question directly.
- Keep useful details.
- Use good grammar and punctuation.
- Vary sentence length naturally.
- Avoid repetitive phrases.
- Avoid unnecessary introductions.
- Do not say "Certainly", "Of course", "Great question",
  or similar filler unless it genuinely fits.
- Do not sound overly formal or corporate.
- Do not sound childish.
- Do not over-explain simple questions.
- Match the user's tone when appropriate.
- If the original answer contains steps, keep the steps.
- If the original answer uses bullets or headings, keep them
  when they improve readability.
- Preserve code, commands, filenames, numbers, and technical
  details exactly.
- Do not invent facts.
- Do not change the meaning.
- Do not add information that was not in the original answer.

The goal is not to make the answer longer.
The goal is to make it BETTER written.

Original reply:
{original_text}
"""

            rephrased = manager_instance.safe_generate(prompt)

            if isinstance(rephrased, str) and rephrased.strip():
                return {"message": rephrased.strip()}

        except Exception as error:
            print("[NATURAL_WRITING] exception:", error)

        return response

    # ======================================================
    # ANALYZE
    # ======================================================

    def analyze(
        self,
        message
    ):

        return reasoning.analyze(
            message
        )



    # ======================================================
    # LEARNING
    # ======================================================

    def learn(
        self,
        topic,
        url
    ):


        if not learning_manager:

            return (
                "Learning system unavailable."
            )


        return learning_manager.learn(
            topic,
            url
        )



    def learn_site(
        self,
        topic,
        url,
        limit=10
    ):


        if not learning_manager:

            return (
                "Learning system unavailable."
            )


        return learning_manager.learn_site(
            topic,
            url,
            limit
        )



    # ======================================================
    # MEMORY
    # ======================================================

    def remember(
        self,
        key,
        value
    ):

        return reasoning.remember_fact(
            key,
            value
        )



    def recall(
        self,
        key
    ):
        # First search learned knowledge, including image learning.
        try:
            result = reasoning.answer(key)

            if isinstance(result, dict):
                if result.get("learned"):
                    return result

                message = result.get("message")
                if message and message != "I haven't learned enough about that yet.":
                    return result

            elif result:
                return result

        except Exception:
            pass

        # Fall back to the original key/value memory system.
        return reasoning.recall_fact(
            key
        )
# ======================================================
    # STATUS
    # ======================================================

    def status(self):

        data = reasoning.status()


        data.update({

            "brain":
                self.name,

            "version":
                self.version,

            "conversation":
                manager.get_status()
                if manager
                else "offline"

        })


        return data




brain = Brain()
