import subprocess
import json
import os

CONTACTS_FILE = "contacts.json"


def create_contacts():
    contacts = {
        "mum": "0795201431",
        "dad": "0724631182"
    }

    with open(CONTACTS_FILE, "w") as f:
        json.dump(contacts, f, indent=4)


def load_contacts():
    if not os.path.exists(CONTACTS_FILE):
        create_contacts()

    with open(CONTACTS_FILE, "r") as f:
        return json.load(f)


def call_contact(command):
    command = command.lower()

    contacts = load_contacts()

    for name, number in contacts.items():
        if f"call {name}" in command:
            subprocess.run([
                "am",
                "start",
                "-a",
                "android.intent.action.DIAL",
                "-d",
                f"tel:{number}"
            ])

            return f"Opening dialer for {name.title()}."

    return None


def message_contact(command):
    command = command.lower()

    contacts = load_contacts()

    for name, number in contacts.items():
        if f"message {name}" in command or f"text {name}" in command:
            subprocess.run([
                "am",
                "start",
                "-a",
                "android.intent.action.SENDTO",
                "-d",
                f"sms:{number}"
            ])

            return f"Opening messages for {name.title()}."

    return None


def add_contact(name, number):
    contacts = load_contacts()

    contacts[name.lower()] = number

    with open(CONTACTS_FILE, "w") as f:
        json.dump(contacts, f, indent=4)

    return f"{name.title()} has been saved."


def list_contacts():
    contacts = load_contacts()

    reply = "Saved contacts:\n"

    for name, number in contacts.items():
        reply += f"{name.title()} : {number}\n"

    return reply
