"""
Nitron Local AI
"""

from ai_engine import engine


def local_ai(prompt):

    return f"Nitron received: {prompt}"


engine.register(
    "local",
    local_ai
)
