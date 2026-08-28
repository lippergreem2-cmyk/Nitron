"""
Nitron Image Plugin
"""

import os
from datetime import datetime

OUTPUT = os.path.expanduser("~/Nitron/media/generated")

os.makedirs(OUTPUT, exist_ok=True)


def run(command):

    prompt = command

    if command.startswith("generate image"):

        prompt = command.replace(
            "generate image",
            "",
            1
        ).strip()

    elif command.startswith("create image"):

        prompt = command.replace(
            "create image",
            "",
            1
        ).strip()

    if not prompt:

        return "Please describe the image."

    filename = (
        prompt
        .replace(" ", "_")
        .lower()
    ) + ".txt"

    path = os.path.join(
        OUTPUT,
        filename
    )

    with open(path, "w") as file:

        file.write(
            "Image Prompt\n\n"
        )

        file.write(prompt)

        file.write("\n")

        file.write(
            datetime.now().isoformat()
        )

    return f"Image request saved:\n{path}"


def plugin():

    return {

        "name": "Image Generator",

        "description":
        "Generate AI image prompts.",

        "version": "1.0",

        "author": "Nitron",

        "category": "Media",

        "commands": [

            "generate image",

            "create image"

        ],

        "run": run

    }
