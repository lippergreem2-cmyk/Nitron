"""Command‑line interface for the Nitron Project.

Provides a simple way to reverse a string from the terminal.
"""
import argparse
from .reverse_string import reverse_string

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Reverse a string using Nitron Project.')
    parser.add_argument('string', help='The string to be reversed')
    return parser

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    reversed_str = reverse_string(args.string)
    print(reversed_str)

if __name__ == '__main__':
    main()
