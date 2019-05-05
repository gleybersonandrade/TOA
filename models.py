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


### METODO 1 ###
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


### METODO 2 ###
# class Graph():
#     """Class to manage Graph model."""

#     def __init__(self):
#         """Create a new Graph Instance."""
#         self.brs = []

#     def find_br(self, id):
#         """Find a BR node in brs array."""
#         for br in self.brs:
#             if id == br.id:
#                 return br
#         return None

#     def add_br(self, id):
#         """Insert a BR node in brs array."""
#         br = self.find_br(id)
#         if br is None:
#             br = BR(id)
#             self.brs.append(br)
#         return br

# class Node():
#     """Class to manage Node model."""

#     def __init__(self, id):
#         """Create a new Node Instance."""
#         self.id = id

# class BR(Node):
#     """Class to manage BR Node model."""

#     def __init__(self, id):
#         """Create a new BR Node Instance."""
#         super().__init__(id)
#         self.kms = []

#     def find_km(self, id):
#         """Find a KM node in kms array."""
#         for km in self.kms:
#             if id == km.id:
#                 return km
#         return None

#     def add_km(self, id):
#         """Insert a KM node in kms array."""
#         km = self.find_km(id)
#         if km is None:
#             km = KM(id)
#             self.kms.append(km)
#         return km

# class KM(Node):
#     """Class to manage KM Node model."""

#     def __init__(self, id):
#         """Create a new KM Node Instance."""
#         super().__init__(id)
