from .prompt_builder import image_prompt
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "generated")

os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_image(subject, style="realistic"):
    prompt = image_prompt(subject, style)

    filename = subject.replace(" ", "_").lower() + ".txt"
    path = os.path.join(OUTPUT_DIR, filename)

    with open(path, "w") as file:
        file.write(prompt)

    return {
        "status": "success",
        "prompt": prompt,
        "file": path
    }
