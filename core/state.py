"""
Nitron State Manager
"""

class State:
    IDLE = "idle"
    LISTENING = "listening"
    THINKING = "thinking"
    SPEAKING = "speaking"
    LEARNING = "learning"
    DEVELOPING = "developing"
    TRADING = "trading"
    SHUTDOWN = "shutdown"

    def __init__(self):
        self.current = self.IDLE
        self.previous = None

    def set(self, state):
        self.previous = self.current
        self.current = state

    def get(self):
        return self.current

    def last(self):
        return self.previous

    def is_idle(self):
        return self.current == self.IDLE

    def is_listening(self):
        return self.current == self.LISTENING

    def is_thinking(self):
        return self.current == self.THINKING

    def is_speaking(self):
        return self.current == self.SPEAKING

    def reset(self):
        self.previous = self.current
        self.current = self.IDLE

    def __str__(self):
        return f"State(current={self.current}, previous={self.previous})"
