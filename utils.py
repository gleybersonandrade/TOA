"""Traffic Occurrence Analyzer utils."""

# System imports
import codecs
import csv
import os
import sys

# Local imports
from config import DB_COLLECTIONS, DB_SEPARATOR, FILES_FOLDER, FILES_SEPARATOR
from models import Event


def read_csv(file_path):
    """Read CSV file."""
    with codecs.open(file_path, 'r', encoding="utf-8", errors="ignore") as file:
        reader = csv.reader(file)
        header = next(reader, None)
        lines = [line for line in reader]
        file.close()
    return header, lines


def populate(year, db):
    """Populate database with a file."""
    for key, values in DB_COLLECTIONS.items():
        path = FILES_FOLDER + year + FILES_SEPARATOR + key
        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        for file in files:
            header, lines = read_csv(path + FILES_SEPARATOR + file)
            data = []
            for line in lines:
                document = {}
                for index in range(0, len(header)):
                    document.update({header[index]: line[index]})
                data.append(document)
            db.insert(data, year+DB_SEPARATOR+key)


def construct(year, db):
    """Make traffic occurrence graph."""

    def add(events, br, km, event):
        """Insert an event in events dict."""
        if not br in events:
            events[br] = {}
        if not km in events[br]:
            events[br][km] = {}
        for key, values in event.items():
            if not key in events[br][km]:
                events[br][km][key] = 0
            value = events[br][km][key] + event[key]
            events[br][km].update({key: value})

    data = {}
    events = {}
    for key, values in DB_COLLECTIONS.items():
        data[key] = db.find({}, values, year+DB_SEPARATOR+key)
    for accident in data["accidents"]:
        event = {"accidents": 1,
                 "deaths": int(accident["mortos"])}
        add(events, accident["br"], accident["km"].split(".")[0], event)
    for infraction in data["infractions"]:
        event = {"infractions": 1}
        add(events, infraction["num_br_infracao"], infraction["num_km_infracao"].split(".")[0], event)
    db.insert(events, year+DB_SEPARATOR+"data")


def run(method, year, db):
    """Run method."""
    switcher = {
        "populate": lambda: populate(year, db),
        "construct": lambda: construct(year, db)
    }
    return switcher.get(method)()
