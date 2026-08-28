"""
Nitron Utility Functions
"""

from datetime import datetime
import os
import json


def clean_text(text):
    """Normalize user input."""
    return str(text).strip().lower()


def current_time():
    """Return the current time."""
    return datetime.now().strftime("%H:%M:%S")


def current_date():
    """Return the current date."""
    return datetime.now().strftime("%Y-%m-%d")


def file_exists(path):
    """Check if a file exists."""
    return os.path.exists(path)


def ensure_folder(path):
    """Create a folder if it doesn't exist."""
    os.makedirs(path, exist_ok=True)


def load_json(filename, default=None):
    """Load JSON safely."""
    if default is None:
        default = {}

    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def save_json(filename, data):
    """Save data as JSON."""
    ensure_folder(os.path.dirname(filename) or ".")

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def banner():
    return """
==================================
        N I T R O N
 Advanced AI Assistant Engine
==================================
"""
