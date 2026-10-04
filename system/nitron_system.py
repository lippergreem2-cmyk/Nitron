#!/usr/bin/env python3

import json
import os
import random
from datetime import date

DATA_FILE = os.path.expanduser("~/Nitron/system/player.json")

BLUE = "\033[94m"
CYAN = "\033[96m"
RESET = "\033[0m"

DEFAULT_PLAYER = {
    "level": 1,
    "xp": 0,
    "streak": 0,
    "quests_completed": 0,
    "last_completion": "",
    "terms_accepted": False
}

TRAINING = {
    "1": {
        "name": "FIGHTING",
        "subtitle": "Non-contact conditioning",
        "steps": [
            "Warm up for 5 minutes",
            "Practice controlled footwork",
            "Work on balance and coordination",
            "Perform bodyweight conditioning",
            "Cool down and recover"
        ]
    },
    "2": {
        "name": "BODY FITNESS",
        "subtitle": "Strength and mobility",
        "steps": [
            "Warm up",
            "Bodyweight squats",
            "Incline or wall push-ups",
            "Glute bridges",
            "Bird-dogs",
            "Mobility cooldown"
        ]
    },
    "3": {
        "name": "SPEED",
        "subtitle": "Movement and coordination",
        "steps": [
            "Warm up thoroughly",
            "Fast-feet coordination drill",
            "Short controlled acceleration drills",
            "Rest between efforts",
            "Cool down"
        ]
    },
    "4": {
        "name": "REFLEX",
        "subtitle": "Reaction and coordination",
        "steps": [
            "Warm up",
            "Visual reaction drill",
            "Hand-eye coordination drill",
            "Balance and movement drill",
            "Cool down"
        ]
    }
}

QUOTES = [
    "Consistency creates progress.",
    "Technique comes before intensity.",
    "Train patiently. Recover properly.",
    "Every completed session is progress.",
    "Discipline is built one session at a time."
]


def load_player():
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

    if not os.path.exists(DATA_FILE):
        save_player(DEFAULT_PLAYER.copy())

    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_PLAYER.copy()


def save_player(player):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

    with open(DATA_FILE, "w") as f:
        json.dump(player, f, indent=2)


def xp_required(level):
    return level * 100


def add_xp(amount):
    player = load_player()
    player["xp"] += amount
    leveled_up = False

    while player["xp"] >= xp_required(player["level"]):
        player["xp"] -= xp_required(player["level"])
        player["level"] += 1
        leveled_up = True

    save_player(player)
    return player, leveled_up


def status():
    player = load_player()

    return (
        f"{BLUE}"
        "╔════════════════════════════╗\n"
        "║       NITRON SYSTEM        ║\n"
        "╠════════════════════════════╣\n"
        f"║ Level: {player['level']:<18}║\n"
        f"║ XP: {player['xp']} / "
        f"{xp_required(player['level']):<10}║\n"
        f"║ Streak: {player['streak']:<15}║\n"
        f"║ Quests: {player['quests_completed']:<15}║\n"
        "╚════════════════════════════╝"
        f"{RESET}"
    )


def terms():
    return """
╔══════════════════════════════════╗
║       NITRON TRAINING TERMS      ║
╚══════════════════════════════════╝

Before starting a training session:

• Train at a safe pace.
• Stop if you feel pain, dizzy, or unwell.
• Use enough space for movement.
• Fighting mode is conditioning only.
• No-contact training is used.
• Rest and recovery are part of training.
• Nitron does not replace professional coaching
  or medical advice.

You can end a session at any time.

Type:
ACCEPT
or
CANCEL
"""


def menu():
    return f"""
{BLUE}╔══════════════════════════════╗
║       NITRON TRAINING        ║
╠══════════════════════════════╣
║  1. FIGHTING                 ║
║  2. BODY FITNESS             ║
║  3. SPEED                    ║
║  4. REFLEX                   ║
║                              ║
║  5. SYSTEM STATUS            ║
║  6. DAILY QUEST              ║
║  7. QUOTE                    ║
╚══════════════════════════════╝{RESET}

Choose 1-7.
"""


def training(choice):
    player = load_player()

    if not player.get("terms_accepted", False):
        return terms()

    item = TRAINING.get(choice)

    if not item:
        return "SYSTEM: Invalid training choice."

    output = [
        f"{CYAN}SYSTEM: {item['name']}{RESET}",
        f"{item['subtitle']}",
        "",
        "TRAINING PLAN:"
    ]

    for index, step in enumerate(item["steps"], 1):
        output.append(f"[ ] {index}. {step}")

    output.extend([
        "",
        "SESSION ACTIVE",
        "Type 'end session' when finished."
    ])

    return "\n".join(output)


def accept_terms():
    player = load_player()
    player["terms_accepted"] = True
    save_player(player)

    return (
        f"{CYAN}SYSTEM: Terms accepted.{RESET}\n\n"
        "Training System unlocked.\n"
        "Choose your training mode:\n\n"
        + menu()
    )


def complete_quest():
    today = str(date.today())
    player = load_player()

    if player["last_completion"] == today:
        return "SYSTEM: Today's quest has already been completed."

    player["last_completion"] = today
    player["quests_completed"] += 1
    player["streak"] += 1
    save_player(player)

    player, leveled_up = add_xp(50)

    result = [
        f"{CYAN}SYSTEM: QUEST COMPLETE{RESET}",
        "",
        "+50 XP",
        f"Streak: {player['streak']}"
    ]

    if leveled_up:
        result.extend([
            "",
            "LEVEL UP!",
            f"New Level: {player['level']}"
        ])

    return "\n".join(result)


def daily_quest():
    return """
SYSTEM: DAILY QUEST

[ ] Safe warm-up
[ ] Strength session
[ ] Conditioning session
[ ] Mobility/recovery

Reward: +50 XP
"""


def command(text):
    if not text:
        return None

    command_text = text.lower().strip()
    player = load_player()

    if command_text in ("system", "open system", "nitron system"):
        return menu()

    if command_text in ("status", "system status", "player status"):
        return status()

    if command_text in ("terms", "terms and conditions"):
        return terms()

    if command_text in ("accept", "accept terms"):
        return accept_terms()

    if command_text in ("cancel", "cancel terms"):
        return "SYSTEM: Training cancelled."

    if command_text in ("daily quest", "daily", "quest"):
        return daily_quest()

    if command_text in ("complete quest", "complete daily quest"):
        return complete_quest()

    if command_text in ("quote", "motivation", "system quote"):
        return "SYSTEM QUOTE: " + random.choice(QUOTES)

    if command_text in ("end session", "end training", "stop training"):
        return "SYSTEM: Session ended. Recover well."

    if command_text in ("1", "fighting"):
        return training("1")

    if command_text in ("2", "body fitness", "fitness"):
        return training("2")

    if command_text in ("3", "speed"):
        return training("3")

    if command_text in ("4", "reflex"):
        return training("4")

    if command_text in ("5",):
        return status()

    if command_text in ("6",):
        return daily_quest()

    if command_text in ("7",):
        return "SYSTEM QUOTE: " + random.choice(QUOTES)

    return None


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "system"
    result = command(text)

    if result:
        print(result)
