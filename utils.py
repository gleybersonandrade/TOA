"""Traffic Occurrence Analyzer utils."""

# System imports
import codecs
import csv
import sys


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
