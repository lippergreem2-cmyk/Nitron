import requests
import os
import time
import urllib.parse

TRIGGERS = [
    "image", "picture", "photo", "drawing",
    "illustration", "artwork", "wallpaper", "draw",
]


def generate_image(prompt, size="1024x1024"):
    try:
        width, height = size.split("x") if "x" in size else ("1024", "1024")
        encoded_prompt = urllib.parse.quote(prompt)

        url = (
            f"https://image.pollinations.ai/prompt/{encoded_prompt}"
            f"?width={width}&height={height}&nologo=true"
        )

        response = requests.get(url, timeout=90)
        response.raise_for_status()

        filename = f"generated_{int(time.time())}.jpg"
        filepath = os.path.join(
            os.path.dirname(__file__), "..", "generated_images", filename
        )
        filepath = os.path.abspath(filepath)

        with open(filepath, "wb") as f:
            f.write(response.content)

        return {
            "success": True,
            "path": filepath,
            "filename": filename
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def matches(command):
    lowered = command.lower().strip()
    for trigger in TRIGGERS:
        if trigger in lowered:
            return True
    return False


def run_command(command):
    prompt = command.strip()

    if not prompt:
        return "What would you like me to draw?"

    result = generate_image(prompt)

    if result["success"]:
        return f"[NITRON_IMAGE]{result['filename']}[/NITRON_IMAGE]I made this for you: {prompt}"
    else:
        return f"I couldn't generate that image: {result['error']}"


def plugin():
    return {
        "commands": TRIGGERS,
        "aliases": [],
        "run": run_command,
        "match_mode": "contains"
    }
