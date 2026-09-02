# Simple command‑line interface for the reverse_string function
"""Command‑line interface for reversing strings.

Run the script with a single positional argument to see the reversed result.
Example:
    python -m nitron_project.main "hello"
"""

import argparse
from nitron_project import reverse_string


def main() -> None:
    parser = argparse.ArgumentParser(description="Reverse a given string.")
    parser.add_argument("text", help="The text to reverse.")
    args = parser.parse_args()
    result = reverse_string(args.text)
    print(result)


if __name__ == "__main__":
    main()
