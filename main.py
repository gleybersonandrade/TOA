"""Traffic Occurrence Analyzer main method."""

# System imports
import argparse

# Local imports
from constants import MAIN_DESC, METHOD_DESC
from utils import run


def main():
    """Responsible for main control."""
    parser = argparse.ArgumentParser(description=MAIN_DESC)
    parser.add_argument('-m', '--method', help=METHOD_DESC)
    args = parser.parse_args()
    try:
        if args.method:
            run(args.method)
    except Exception as e:
        print(e)
        parser.print_help()


if __name__ == "__main__":
    main()
