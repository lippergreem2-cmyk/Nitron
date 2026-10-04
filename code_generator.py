"""
code_generator.py
Lets Nitron generate Python scripts on demand from a plain-language
description, using the OpenAI API (same setup as ai_brain.py).

Usage:
    from code_generator import generate_code, generate_and_save

    code = generate_code("a script that animates a butterfly curve")
    print(code)

    # or generate AND write straight to a file:
    generate_and_save("a mini rule-based chatbot", "chatbot.py")
"""

import os
import re
from openai import OpenAI

MODEL = "gpt-4o-mini"

SYSTEM_PROMPT = (
    "You are Nitron's code generation module. Given a description of a "
    "Python script, write complete, working, well-commented Python code "
    "that accomplishes it. Prefer standard library and common packages "
    "(numpy, pandas, matplotlib, requests) over obscure dependencies. "
    "Respond with ONLY the code -- no explanation, no markdown fences, "
    "just the raw Python source, ready to save directly to a .py file. "
    "Refuse only if the request is for malware, credential theft, "
    "unauthorized network intrusion, or attacking systems the user "
    "doesn't own -- in that case respond with a single line starting "
    "with 'REFUSED:' explaining why."
)


def _client() -> OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY not set. Run: export OPENAI_API_KEY='your-key-here'"
        )
    return OpenAI(api_key=api_key)


def _strip_markdown_fences(text: str) -> str:
    """In case the model wraps output in ```python ... ``` anyway."""
    text = re.sub(r"^```(?:python)?\n", "", text.strip())
    text = re.sub(r"\n```$", "", text)
    return text


def generate_code(description: str) -> str:
    """Ask the AI to write a Python script for the given description.
    Returns the raw source code as a string, or raises if refused."""
    client = _client()
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Write a Python script that does the following:\n{description}"},
        ],
    )
    code = response.choices[0].message.content.strip()

    if code.startswith("REFUSED:"):
        raise ValueError(code)

    return _strip_markdown_fences(code)


def generate_and_save(description: str, filename: str) -> str:
    """Generate code and write it directly to a file. Returns the filepath."""
    code = generate_code(description)
    with open(filename, "w") as f:
        f.write(code)
    print(f"Saved generated script to {filename}")
    return filename


if __name__ == "__main__":
    desc = input("Describe the script you want Nitron to write: ")
    filename = input("Save as (filename.py): ").strip() or "generated_script.py"
    try:
        generate_and_save(desc, filename)
    except ValueError as e:
        print(f"Nitron declined: {e}")
