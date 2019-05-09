"""Traffic Occurrence Analyzer models."""

# Third-party imports
from pymongo import MongoClient

# Local imports
from config import DB_HOST, DB_NAME, DB_PORT


class Database():
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

class Event():
    """Class to manage Event model."""

    def __init__(self):
        """Create a new Event Instance."""
