# ~/Nitron/client.py

import requests
import json


SERVER = "http://127.0.0.1:8081"


def ask_nitron(command):

    data = {
        "command": command
    }

    response = requests.post(
        SERVER,
        json=data
    )

    return response.json()



print("Nitron Client Online")

while True:

    command = input("You: ")

    if command.lower() == "exit":

        print("Goodbye Boss.")

        break


    try:

        result = ask_nitron(command)

        print(
            "Nitron:",
            result.get("answer")
        )


    except Exception as e:

        print(
            "Connection error:",
            e
        )
