import sys
from prime import is_prime


def main() -> None:
    """Simple CLI to test the *is_prime* function.

    Usage:
        python main.py <integer>
    """
    if len(sys.argv) != 2:
        print("Usage: python main.py <integer>")
        sys.exit(1)
    try:
        number = int(sys.argv[1])
    except ValueError:
        print("Error: argument must be an integer.")
        sys.exit(1)

    if is_prime(number):
        print(f"{number} is a prime number.")
    else:
        print(f"{number} is not a prime number.")


if __name__ == "__main__":
    main()
