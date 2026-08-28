"""
==========================================================
NITRON BRAIN CORE v8.0
Main controller for Nitron intelligence
==========================================================
"""


from brain.reasoning import reasoning


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

    def think(
        self,
        message
    ):

        try:

            if manager:

                manager.user_message(
                    message
                )


            response = reasoning.answer(
                message
            )


            if manager:

                manager.start_response(
                    response
                )

                manager.finish_response()


            return response


        except Exception as error:

            return {
                "error":
                    f"Brain thinking error: {error}"
            }



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
