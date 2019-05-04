"""Traffic Occurrence Analyzer main method."""

# System imports
import argparse

# Local imports
from constants import MAIN_DESC, INPUT_DESC, POPULATE_DESC
from models import DB, Graph
from utils import make_graph, populate


def main():
    """Responsible for main control."""
    parser = argparse.ArgumentParser(description=MAIN_DESC)
    parser.add_argument('-i', '--input', help=INPUT_DESC)
    parser.add_argument('-p', '--populate', help=POPULATE_DESC)
    args = parser.parse_args()
    try:
        db = DB()
        graph = Graph()
        if args.populate and args.input:
            populate(args.populate, args.input, db)
        make_graph(graph, db)
    except Exception as e:
        print(e)
        parser.print_help()


if __name__ == "__main__":
    main()
