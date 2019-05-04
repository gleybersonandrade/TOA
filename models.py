"""Traffic Occurrence Analyzer models."""

# Third-party imports
from pymongo import MongoClient

# Local imports
from config import DB_HOST, DB_NAME, DB_PORT


class DB():
    """Class to manage DB model."""

    def __init__(self):
        """Create a new DB Instance."""
        self.client = MongoClient(DB_HOST, DB_PORT)
        self.db = self.client[DB_NAME]

    def insert(self, data, collection):
        """Insert data."""
        if isinstance(data, list):
            self.db[collection].insert_many(data)
        else:
            self.db[collection].insert_one(data)
 
    def find(self, query, fields, collection):
        """Find data."""
        return self.db[collection].find(query, fields)

class Graph():
    """Class to manage Graph model."""

    def __init__(self):
        """Create a new Graph Instance."""
        self.nodes = {}

    def add_node(self, br, km, node):
        """Insert a node in nodes array."""
        if not br in self.nodes:
            self.nodes[br] = {}
        self.nodes[br].update({km: node})

class Node():
    """Class to manage Node model."""

    def __init__(self):
        """Create a new Node Instance."""
