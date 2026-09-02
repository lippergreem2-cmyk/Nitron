import argparse
from reverse_string import reverse_string

def main() -> None:
    parser = argparse.ArgumentParser(description='Reverse a given string.')
    parser.add_argument('input', help='String to reverse')
    args = parser.parse_args()
    result = reverse_string(args.input)
    print(result)

if __name__ == '__main__':
    main()
