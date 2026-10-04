#!/usr/bin/env python3

"""
Nitron Fitness Coach
Healthy strength, mobility, recovery, and fitness education.
"""

WORKOUTS = {
    "beginner": [
        "Warm-up: 5 minutes of easy movement",
        "Bodyweight squats: 2 sets",
        "Wall or incline push-ups: 2 sets",
        "Glute bridges: 2 sets",
        "Bird-dogs: 2 sets",
        "Easy cooldown and stretching",
    ],
    "full_body": [
        "Warm-up: 5 minutes",
        "Bodyweight squats",
        "Incline push-ups",
        "Glute bridges",
        "Bird-dogs",
        "Calf raises",
        "Cooldown",
    ],
}

QUOTES = [
    "Consistency matters more than perfection.",
    "Build strength patiently and recover well.",
    "Small improvements add up over time.",
    "Good technique comes before adding difficulty.",
    "Rest is part of training.",
]


def get_workout(level="beginner"):
    return WORKOUTS.get(level, WORKOUTS["beginner"])


def get_quote():
    import random
    return random.choice(QUOTES)


def coach(command):
    command = command.lower().strip()

    if command in ("workout", "exercise", "train"):
        return "\n".join(get_workout())

    if command in ("quote", "motivation", "motivate"):
        return get_quote()

    if command in ("help", "fitness"):
        return (
            "Nitron Fitness Coach commands:\n"
            "  workout    - get a beginner workout\n"
            "  quote      - get a motivation quote\n"
            "  help       - show this menu"
        )

    return "I don't recognize that fitness command. Try: workout, quote, or help."


if __name__ == "__main__":
    import sys

    command = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "help"
    print(coach(command))
