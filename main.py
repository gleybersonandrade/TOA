"""Traffic Occurrence Analyzer main method."""

# System imports
import argparse

# Local imports
from constants import MAIN_DESC, METHOD_DESC, YEAR_DESC
from models import Database
from utils import run


def main():
    """Responsible for main control."""
    parser = argparse.ArgumentParser(description=MAIN_DESC)
    parser.add_argument('-m', '--method', help=METHOD_DESC)
    parser.add_argument('-y', '--year', help=YEAR_DESC)
    args = parser.parse_args()
    try:
        db = Database()
        if args.method and args.year:
            run(args.method, args.year, db)
    except Exception as e:
        print(e)
        parser.print_help()


if __name__ == "__main__":
    main()
