"""Traffic Occurrence Analyzer utils."""

# System imports
import codecs
import csv
import os
import re

# Local imports
from config import DB_COLLECTIONS, FILES_FOLDER, FILES_SEPARATOR, YEARS


def populate(db):
    """Populate database."""
    def add(events, br, km, event):
        """Insert an event in events dict."""
        if br not in events:
            events[br] = {}
        if km not in events[br]:
            events[br][km] = {}
        for key in event:
            if key not in events[br][km]:
                events[br][km][key] = 0
            value = events[br][km][key] + event[key]
            events[br][km].update({key: value})

    def get_data(year):
        """Get data from CSV files."""
        def read_csv(path):
            """Read CSV file."""
            with codecs.open(path, 'r', encoding="utf-8",
                             errors="ignore") as file:
                reader = csv.reader(file, delimiter=';')
                header = next(reader, None)
                lines = [line for line in reader]
                file.close()
            return header, lines

        data = {}
        for key, values in DB_COLLECTIONS.items():
            path = FILES_FOLDER + year + FILES_SEPARATOR + key
            files = [f for f in os.listdir(path)
                     if os.path.isfile(os.path.join(path, f))]
            file_data = []
            for file in files:
                header, lines = read_csv(path + FILES_SEPARATOR + file)
                for line in lines:
                    document = {}
                    for index, field in enumerate(header):
                        if field in values:
                            document.update({field: line[index]})
                    file_data.append(document)
            data[key] = file_data
        return data

    for year in YEARS:
        events = {}
        data = get_data(year)
        for accident in data["accidents"]:
            event = {"accidents": 1,
                     "deaths": int(accident["mortos"])}
            add(events, re.split('[,|.]', accident["br"])[0],
                re.split('[,|.]', accident["km"])[0], event)
        for infraction in data["infractions"]:
            event = {"infractions": 1}
            add(events, re.split('[,|.]', infraction["num_br_infracao"])[0],
                re.split('[,|.]', infraction["num_km_infracao"])[0], event)
        db.insert(events, year)


def construct(db):
    """Make traffic occurrence graph."""


def run(method, db):
    """Run method."""
    switcher = {
        "populate": lambda: populate(db),
        "construct": lambda: construct(db)
    }
    return switcher.get(method)()
