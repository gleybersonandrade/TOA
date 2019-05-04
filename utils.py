"""Traffic Occurrence Analyzer utils."""

# System imports
import codecs
import csv
import sys

# Local imports
from config import DB_COLLECTIONS
from models import Graph, Node


def read_csv(file_path):
    """Read CSV file."""
    with codecs.open(file_path, 'r', encoding="utf-8", errors="ignore") as file:
        reader = csv.reader(file)
        header = next(reader, None)
        lines = [line for line in reader]
        file.close()
    return header, lines


def populate(collection, file_path, db):
    """Populate database with a file."""
    header, lines = read_csv(file_path)    
    data = []
    for line in lines:
        document = {}
        for index in range(0, len(header)):
            document.update({header[index]: line[index]})
        data.append(document)
    db.insert(data, collection)


def make_graph(graph, db):
    data = {}
    for key, values in DB_COLLECTIONS.items():
        data[key] = db.find({}, values, key)
    for accident in data["accidents"]:
        graph.add_node(accident["br"], accident["km"], Node())
    # for infraction in data["infractions"]:
    #     graph.add_node(infraction["num_br_infracao"], infraction["num_km_infracao"], Node())
    # print(graph.nodes)