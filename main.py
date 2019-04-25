"""Traffic Occurrence Analyzer main method."""

# System imports
import argparse

# Local imports
from constants import MAIN_DESC, INPUT_DESC, POPULATE_DESC
from models import DB
from utils import populate


def main():
    """Responsible for main control."""
    parser = argparse.ArgumentParser(description=MAIN_DESC)
    parser.add_argument('-i', '--input', help=INPUT_DESC)
    parser.add_argument('-p', '--populate', help=POPULATE_DESC)
    args = parser.parse_args()
    try:
        db = DB()
        if args.populate and args.input:
            populate(args.populate, args.input, db)
    except Exception as e:
        print(e)
        parser.print_help()


if __name__ == "__main__":
    main()
